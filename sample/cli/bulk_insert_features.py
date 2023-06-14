#!/usr/bin/env python3

import argparse
import subprocess

parser = argparse.ArgumentParser(description='Insert face feature.')
parser.add_argument('host', type=str, help='Host of face service server.')
parser.add_argument('num', type=int, help='Number of features.')
parser.add_argument('feature', type=str, help='Path of face feature file.')
args = parser.parse_args()

for i in range(args.num):
    subprocess.call(["./insert_feature.py", args.host, str(i), args.feature])
print("Done")
