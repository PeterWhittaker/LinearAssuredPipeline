#!/usr/bin/env python
import sys
import argparse
from pipeline.readPipelineFromFile import readPipelineFromFile
from pipeline.extractPipeline import extractPipeline, viewPipeline

def processPipeline(pipelineName, filename):
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

if __name__ == '__main__':
    myArgsParser = argparse.ArgumentParser()
    myArgsParser.add_argument("--filename", required=True)
    myArgsParser.add_argument("--pipelinename", required=True)

    myArgs = myArgsParser.parse_args()

    processPipeline(myArgs.pipelinename, myArgs.filename)
