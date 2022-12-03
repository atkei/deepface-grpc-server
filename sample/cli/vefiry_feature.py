#!/usr/bin/env python3

import grpc
from face_pb2 import *
import face_pb2_grpc
import argparse

parser = argparse.ArgumentParser(description='Verify face feature.')
parser.add_argument('host', type=str, help='Host of face service server.')
parser.add_argument('feature1', type=str, help='Path of first face feature file.')
parser.add_argument('feature2', type=str, help='Path of second face feature file.')
args = parser.parse_args()

with open(args.feature1, 'rb') as f:
    feature_data1 = f.readline()

with open(args.feature2, 'rb') as f:
    feature_data2 = f.readline()

with grpc.insecure_channel(args.host) as channel:
    stub = face_pb2_grpc.FaceServiceStub(channel=channel)
    req = VerifyFaceFeatureRequest(b64Feature1=feature_data1, b64Feature2=feature_data2)
    res = stub.VerifyFaceFeature(req)
    print(res)
