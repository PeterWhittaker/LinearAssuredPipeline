#!/usr/bin/env python
import sys
import argparse
from pipeline.readPipelineFromFile import readPipelineFromFile
from pipeline.extractPipeline import extractPipeline
from pipeline.viewPipeline import viewPipeline
from pipeline.buildPipeline import buildPipeline

def pipelineTest(pipelineName, filename):
    try:
        myPipelineObject = readPipelineFromFile(pipelineName, filename)
    except Exception as err:
        print('Unable to get "%s" from file "%s". Exiting.' % (pipelineName, filename))
        print('    (Exception message was: "%s")' % err)
        sys.exit(1)

    try:
        myPipeline = extractPipeline(myPipelineObject)
    except Exception as err:
        print('Unable to encode "%s" for further processing. Exiting.' % pipelineName)
        print('    (Exception message was: "%s")' % err)
        sys.exit(3)

    try:
        viewPipeline(myPipeline)
    except Exception as err:
        print('Unable to view pipeline details. Odd. Exiting.')
        print('    (Exception message was: "%s")' % err)
        sys.exit(5)

    try:
        buildPipeline(myPipeline)
    except Exception as err:
        print('Unable to build the pipeline. Exiting.')
        print('    (Exception message was: "%s")' % err)
        sys.exit(7)

    sys.exit(0)

if __name__ == '__main__':
    myArgsParser = argparse.ArgumentParser(description='Linear Pipeline testing tool')
    myArgsParser.add_argument("--filename", required=True)
    myArgsParser.add_argument("--pipelinename", required=True)

    myArgs = myArgsParser.parse_args()

    pipelineTest(myArgs.pipelinename, myArgs.filename)

