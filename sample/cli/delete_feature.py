#!/usr/bin/env python3

import grpc
from face_pb2 import *
import face_pb2_grpc
import argparse

parser = argparse.ArgumentParser(description='Delete face feature.')
parser.add_argument('host', type=str, help='Host of face service server.')
parser.add_argument('feature_id', type=int, help='Target feature ID.')
args = parser.parse_args()

with grpc.insecure_channel(args.host) as channel:
    stub = face_pb2_grpc.FaceServiceStub(channel=channel)
    req = DeleteFaceFeatureRequest(featureId=args.feature_id)
    res = stub.DeleteFaceFeature(req)
    print(res)
