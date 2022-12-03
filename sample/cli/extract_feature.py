#!/usr/bin/env python3

import grpc
from face_pb2 import *
import face_pb2_grpc
import argparse
import base64

parser = argparse.ArgumentParser(description='Extract face feature.')
parser.add_argument('host', type=str, help='Host of face service.')
parser.add_argument('jpeg', type=str, help='Path of jpeg detected face file.')
args = parser.parse_args()

with open(args.jpeg, 'rb') as f:
    image_string = base64.b64encode(f.read()).decode('utf-8')

with grpc.insecure_channel(args.host) as channel:
    stub = face_pb2_grpc.FaceServiceStub(channel=channel)
    req = ExtractFaceFeatureRequest(b64Jpeg=image_string)
    res = stub.ExtractFaceFeature(req)
    print(res)
