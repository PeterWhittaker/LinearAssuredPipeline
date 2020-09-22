#!/usr/bin/env python
import sys
import argparse
import logging

from pipeline.readPipelineFromFile import readPipelineFromFile
from pipeline.extractPipeline import extractPipeline
from pipeline.viewPipeline import viewPipeline
from pipeline.buildPipeline import buildPipeline

def processPipeline(pipelineName, filename):
    try:
        myPipelineObject = readPipelineFromFile(pipelineName, filename)
    except Exception as err:
        print('Unable to get "%s" from file "%s". Exiting.' % (pipelineName, filename))
        print('    (Exception message was: "%s")' % err)
        return 1

    try:
        myPipeline = extractPipeline(myPipelineObject)
    except Exception as err:
        print('Unable to encode "%s" for further processing. Exiting.' % pipelineName)
        print('    (Exception message was: "%s")' % err)
        return 3

    if logging.DEBUG >= logging.root.level:
        try:
            viewPipeline(myPipeline)
        except Exception as err:
            print('Unable to view pipeline details. Odd. Exiting.')
            print('    (Exception message was: "%s")' % err)
            return 5

    try:
        buildPipeline(myPipeline)
    except Exception as err:
        print('Unable to build pipeline. Exiting.')
        print('    (Exception message was: "%s")' % err)
        return 7

    return 0

if __name__ == '__main__':
    myArgsParser = argparse.ArgumentParser()
    myArgsParser.add_argument("--filename", required=True)
    myArgsParser.add_argument("--pipelinename", required=True)
    myArgsParser.add_argument("--loglevel", default="WARNING")

    myArgs = myArgsParser.parse_args()
    pipelineName = myArgs.pipelinename
    filename = myArgs.filename
    loglevel = myArgs.loglevel

    loggingLevel = getattr(logging, loglevel.upper())
    if not isinstance(loggingLevel, int):
        raise ValueError("Invalid log level '%s'", loggingLevel)

    logging.basicConfig(level=loggingLevel)

    myLogger = logging.getLogger('processPipeline')
    myLogger.debug('Logging enabled.')

    myLogger.debug("Calling 'processPipeline' with pipeline '%s' and file '%s'" % (pipelineName, filename) )
    exitCode = processPipeline(pipelineName, filename)

    myLogger.debug("Exiting with return code '%s'." % exitCode)
    sys.exit(exitCode)
