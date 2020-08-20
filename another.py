#!/usr/bin/env python
import io
import sys
from ruamel.yaml import YAML
from pipeline.extractPipeline import extractPipeline

myYaml = YAML()

filename = 'tests/pipelineTest.yml'
myFile = io.open(filename, 'r')

myObj = myYaml.load(myFile)

extractPipeline('pipelineTest', myObj)
