import base64
import struct
from io import BytesIO

import grpc
from PIL import Image

import numpy as np

from deepface import DeepFace

from mapper import fetch_feature_by_id, insert_feature_transaction, delete_feature_transaction
from face_pb2 import FaceFeatureResponse, MatchFaceFeatureResponse, VerifyFaceFeatureResponse, \
    ExtractFaceFeatureResponse, DetectFaceResponse, InsertFaceFeatureRequest, DeleteFaceFeatureRequest, \
    MatchFaceFeatureRequest, VerifyFaceFeatureRequest, ExtractFaceFeatureRequest, DetectFaceRequest

from logger_factory import LoggerFactory
from config import ServerConfig
from feature_mngr import FeatureManager

logger = LoggerFactory.get_logger(__name__)


class FaceService:
    def __init__(self, cfg: ServerConfig, fm: FeatureManager):
        self.cfg = cfg
        self.fm = fm

    async def InsertFaceFeature(self, request: InsertFaceFeatureRequest, context) -> FaceFeatureResponse:
        byte_feature = base64.b64decode(request.b64Feature)
        feature_id, _ = await insert_feature_transaction(request.personId, byte_feature)
        logger.info("Inserted feature to DB (personId=%s, featureId=%s)" % (request.personId, feature_id))
        return FaceFeatureResponse(featureId=feature_id, b64Feature=request.b64Feature)

    async def DeleteFaceFeature(self, request: DeleteFaceFeatureRequest, context) -> FaceFeatureResponse:
        feature = await fetch_feature_by_id(feature_id=request.featureId)
        if feature is None:
            context.set_details("No such feature")
            context.set_code(grpc.StatusCode.NOT_FOUND)
            return FaceFeatureResponse()
        b64_feature_data = base64.b64encode(feature.feature_data)
        feature_id, operation_id = await delete_feature_transaction(feature_id=request.featureId)
        logger.info("Deleted feature from DB (featureId=%s)" % feature_id)
        return FaceFeatureResponse(featureId=feature_id, b64Feature=b64_feature_data)

    async def MatchFaceFeature(self, request: MatchFaceFeatureRequest, context) -> MatchFaceFeatureResponse:
        b64_feature = request.b64Feature
        byte_feature = base64.b64decode(b64_feature)
        input_feature = [e[0] for e in struct.iter_unpack('<f', byte_feature)]

        mt = self.cfg.similarity_metrics
        cur_sim = mt.get_min_sim()
        matched, person_id, feature_id = False, -1, -1

        for loaded_feature_id, loaded_feature in self.fm.loaded_features.items():
            new_sim = mt.get_sim(input_feature, loaded_feature['feature_data'])
            if mt.is_more_sim(cur_sim=cur_sim, new_sim=new_sim):
                cur_sim, person_id, feature_id = new_sim, loaded_feature['person_id'], loaded_feature_id
                if not matched and mt.is_more_sim(cur_sim=self.cfg.similarity_threshold, new_sim=cur_sim):
                    matched = True

        if matched:
            logger.info("Matched feature (personId=%s, featureId=%s, similarity=%s)" % (person_id, feature_id, cur_sim))
        else:
            print("No matched feature (personId=%s, featureId=%s, similarity=%s)" % (person_id, feature_id, cur_sim))

        return MatchFaceFeatureResponse(
            matched=matched,
            personId=person_id,
            featureId=feature_id,
            similarityMetrics=self.cfg.similarity_metrics.value,
            similarity=cur_sim
        )

    async def VerifyFaceFeature(self, request: VerifyFaceFeatureRequest, context) -> VerifyFaceFeatureResponse:
        b64_feature1 = request.b64Feature1
        b64_feature2 = request.b64Feature2
        byte_feature1 = base64.b64decode(b64_feature1)
        byte_feature2 = base64.b64decode(b64_feature2)
        embedding1 = [e[0] for e in struct.iter_unpack('<f', byte_feature1)]
        embedding2 = [e[0] for e in struct.iter_unpack('<f', byte_feature2)]
        sim = self.cfg.similarity_metrics.get_sim(embedding1, embedding2)
        logger.info("Verified feature (similarity=%s)" % sim)
        return VerifyFaceFeatureResponse(similarityMetrics=self.cfg.similarity_metrics.value, similarity=sim)

    async def ExtractFaceFeature(self, request: ExtractFaceFeatureRequest, context) -> ExtractFaceFeatureResponse:
        b64_jpeg = request.b64Jpeg
        embedding = DeepFace.represent('data:image/jpeg;base64,' + b64_jpeg,
                                       model_name=self.cfg.feature_model.value,
                                       detector_backend=self.cfg.detector_backend.value)
        byte_feature = b''.join([struct.pack('<f', e) for e in embedding])
        logger.info("Extracted feature")
        return ExtractFaceFeatureResponse(b64Feature=base64.b64encode(byte_feature))

    async def DetectFace(self, request: DetectFaceRequest, context) -> DetectFaceResponse:
        b64_jpeg = request.b64Jpeg
        img_array = DeepFace.detectFace('data:image/jpeg;base64,' + b64_jpeg, detector_backend=self.cfg.detector_backend.value)
        img_array = (255.0 / img_array.max() * (img_array - img_array.min())).astype(np.uint8)
        im = Image.fromarray(img_array, 'RGB')
        buffer = BytesIO()
        im.save(buffer, format='JPEG')
        logger.info("Detected face")
        return DetectFaceResponse(b64Jpeg=base64.b64encode(buffer.getvalue()))
