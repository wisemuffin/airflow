#!/usr/bin/env python3

import json
import sys

from dags.tweet_analyzer.python.components.data_processing import preprocess

input = sys.argv[1]
output = sys.argv[2]


print("Starting data cleaning...")
print(f'input: {input}')
print(f'output: {output}')
preprocess(input, output)
print("Completed data cleaning!")
