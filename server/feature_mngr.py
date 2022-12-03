import asyncio
import struct
from collections import defaultdict
from datetime import datetime

from mapper import fetch_last_operation_id, load_pending_operations, fetch_feature_by_id, fetch_features
from enums import FeatureOperationType
from logger_factory import LoggerFactory
from sig_handler import SignalHandler

logger = LoggerFactory.get_logger(__name__)


class FeatureManager:
    def __init__(self):
        logger.info("inited")
        self.loaded_features = defaultdict(dict)

    async def sync_features(self, sig_handler: SignalHandler):
        await self.init_load_features(sig_handler)
        last_operation_id = await fetch_last_operation_id(datetime.now())

        while sig_handler.KEEP_PROCESSING:
            try:
                pending_operations = await load_pending_operations(last_operation_id=last_operation_id, limit=10)
            except Exception as e:
                logger.error("Failed to load pending operations: " + repr(e))
                await asyncio.sleep(2)
                continue
            for po in pending_operations:
                operation_id = po.operation_id
                operation_type = po.operation_type
                feature_id = po.feature_id
                if operation_type == FeatureOperationType.ADD:
                    # Add feature.
                    try:
                        feature = await fetch_feature_by_id(feature_id=feature_id)
                    except Exception as e:
                        logger.error("Failed to load feature: " + repr(e))
                        await asyncio.sleep(2)
                        continue
                    if feature is not None:
                        embedding = [e[0] for e in struct.iter_unpack('<f', feature.feature_data)]
                        self.loaded_features[feature.feature_id]['person_id'] = feature.person_id
                        self.loaded_features[feature.feature_id]['feature_data'] = embedding
                        logger.info("Added feature (featureId=%s). Number of loaded features=%s" % (
                            feature_id, len(self.loaded_features)))
                else:
                    # Remove feature.
                    self.loaded_features.pop(feature_id)
                    logger.info("Removed feature (featureId=%s). Number of loaded features=%s" % (
                        feature_id, len(self.loaded_features)))
                last_operation_id = operation_id
            await asyncio.sleep(0.5)

    async def init_load_features(self, sig_handler: SignalHandler):
        logger.info("Started initial features loading")
        offset = 0
        limit = 100
        while sig_handler.KEEP_PROCESSING:
            try:
                loaded_features = await fetch_features(offset=offset, limit=limit)
            except Exception as e:
                logger.error("Failed to load features: " + repr(e))
                await asyncio.sleep(2)
                continue
            if len(loaded_features) == 0:
                logger.info(
                    "Completed initial features loading. Number of loaded features=%s" % len(self.loaded_features))
                return
            for feature in loaded_features:
                embedding = [e[0] for e in struct.iter_unpack('<f', feature.feature_data)]
                self.loaded_features[feature.feature_id]['person_id'] = feature.person_id
                self.loaded_features[feature.feature_id]['feature_data'] = embedding
            offset += 100
