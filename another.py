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
    myEntry   = pipeline[name]['entry']
    myExit    = pipeline[name]['exit']
    myFilters = pipeline[name]['filters']

    myEntryObj = endpointFactory(myEntry)
    print(myEntryObj.getMsg)
    myEntryObj.cycleThrough()
    print()

    myExitObj = endpointFactory(myExit)
    print(myExitObj.getMsg)
    myExitObj.cycleThrough()
    print()

    for myFilter in myFilters:
        myFilterObj = filterFactory(myFilter)
        print(myFilterObj.getMsg)
        myFilterObj.cycleThrough()
        print()
    #myBogusObj = endpointFactory({'type': 'fred'})
    #myBogusObj = endpointFactory(myEntry, 'type')

extractPipeline('pipelineTest', myObj)
