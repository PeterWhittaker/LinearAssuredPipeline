#!/usr/bin/env python
import sys
import argparse
import logging

from pipeline.Pipeline import Pipeline

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

    myLogger.debug("Creating pipeline '%s' from file '%s'" % (pipelineName, filename) )
    myPipeline = Pipeline(pipelineName, filename)

    myPipeline.build()

