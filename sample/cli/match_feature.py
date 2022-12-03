#!/usr/bin/env python3

import grpc
from face_pb2 import *
import face_pb2_grpc
import argparse

parser = argparse.ArgumentParser(description='Match face feature.')
parser.add_argument('host', type=str, help='Host of face service server.')
parser.add_argument('feature', type=str, help='Path of face feature file.')
args = parser.parse_args()

with open(args.feature, 'rb') as f:
    feature_data = f.readline()

with grpc.insecure_channel(args.host) as channel:
    stub = face_pb2_grpc.FaceServiceStub(channel=channel)
    req = MatchFaceFeatureRequest(b64Feature=feature_data)
    res = stub.MatchFaceFeature(req)
    print(res)
