#!/usr/bin/env python
import io
import sys
from ruamel.yaml import YAML
from pipeline.endpoint.endpointFactory import endpointFactory
from pipeline.filters.filterFactory import filterFactory

myYaml = YAML()

filename = 'tests/pipelineTest.yml'
myFile = io.open(filename, 'r')

myObj = myYaml.load(myFile)

def extractPipeline(name, pipeline):
    try:
        myEntry   = pipeline[name]['entry']
        myExit    = pipeline[name]['exit']
        myFilters = pipeline[name]['filters']
    except:
        print('Unable to extract elements from pipeline.')
        print()
        return

    try:
        myEntryObj = endpointFactory(myEntry)
    except:
        print('Unable to convert "entry" element to endpoint object.')
        print()
        return
    else:
        print(myEntryObj.getMsg)
        myEntryObj.cycleThrough()
        print()

    try:
        myFilterList = filterFactory(myFilters)
    except:
        print('Unable to convert "filter" element(s) to filter list.')
        print()
    else:
        numFilters = len(myFilterList)
        print('%s filters' % numFilters)
        for i in range(numFilters):
            key = i + 1
            print(myFilterList[key].getMsg)
            myFilterList[key].cycleThrough()
            print()
    try:
        myExitObj = endpointFactory(myExit)
    except:
        print('Unable to convert "exit" element to endpoint object.')
        print()
        return
    else:
        print(myExitObj.getMsg)
        myExitObj.cycleThrough()
        print()

extractPipeline('pipelineTest', myObj)
