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

    filterList = {}
    for myFilter in myFilters:
        myFilterObj = filterFactory(myFilter)
        filterList.setdefault(myFilterObj.order, myFilterObj)

    numFilters = len(filterList)
    print('%s filters' % numFilters)
    try:
        for i in range(numFilters):
            key = i+1
            try:
                order = filterList[key]
            except:
                print('Could not find filter#%s, is the list monotonic starting at 1?' % key)
                raise ValueError()
            else:
                print(filterList[key].getMsg)
                filterList[key].cycleThrough()
                print()
    except ValueError:
            keys = ''
            for i in sorted (filterList.keys()):
                if not keys == '':
                    keys += ', '
                keys += '%i' % i
            print('Filter "order" values are "%s".' % keys)
            print('Filter "order" must start at "1" and increase monotonically by 1.')
            print()

    myExitObj = endpointFactory(myExit)
    print(myExitObj.getMsg)
    myExitObj.cycleThrough()
    print()

extractPipeline('pipelineTest', myObj)
