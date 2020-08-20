#!/usr/bin/env python
import io
import sys
from ruamel.yaml import YAML
from pipeline.extractPipeline import extractPipeline, viewPipeline

myYaml = YAML()

pipelineName = 'pipelineTest'
filename = 'tests/pipelineTest.yml'
try:
    myFile = io.open(filename, 'r')
except:
    print('Unable to read from "%s". Exiting.' % filename)
    sys.exit(1)

try:
    myObj = myYaml.load(myFile)
except:
    print('Unable to get YAML from "%s". Exiting.' % filename)
    sys.exit(3)

try:
    myPipelineObject = myObj['pipelineTest']
except:
    print('No such pipeline "%s" in file "%s". Exiting.' % (pipelineName, filename))
    sys.exit(5)

try:
    myPipeline = extractPipeline(myPipelineObject)
except:
    print('Unable to encode "%s" for further processing. Exiting.' % pipelineName)
    sys.exit(7)
else:
    try:
        viewPipeline(myPipeline)
    except:
        print('Unable to view pipeline details. Odd. Exiting.')
        sys.exit(9)

