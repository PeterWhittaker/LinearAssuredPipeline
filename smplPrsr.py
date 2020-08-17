#!/usr/bin/env python
import io
import sys
from ruamel.yaml import YAML

myYaml = YAML()

filename = 'tests/pipelineTest.yml'
myFile = io.open(filename, 'r')

myObj = myYaml.load(myFile)

def _iterateOverMap(mapObj, space=""):
    try:
        for key, value in mapObj.items():
            print('%s%s:' % (space, key))
            space += " "
            _iterateOverMap(value, space)
    except:
        print('%s%s:' % (space, mapObj))

def _readCommon(common, space=""):
    part = 'interfaceType'
    print('%s%s is "%s"' % (space, part, common[part]))
    
def _readEndpoint(endpoint, space=""):
    protocol = 'protocol'
    infctype = 'interfaceType'
    foldpath = 'path'
    foldtype = 'folderType'
    procname = 'name'
    proctype = 'processType'
    startdby = 'startedBy'
    myDict = {
        protocol: endpoint[protocol],
        infctype: endpoint['common'][infctype],
        foldpath: endpoint['common']['folder'][foldpath],
        foldtype: endpoint['common']['folder'][foldtype],
        procname: endpoint['common']['processInfo'][procname],
        proctype: endpoint['common']['processInfo'][proctype],
        startdby: endpoint['common']['processInfo'][startdby]
    }
    for key, value in myDict.items():
        if key is not startdby:
            print(key, value)
        else:
            for key, value in myDict[startdby].items():
                print(key, value)

    return
    print('%s%s is "%s"' % (space, part, endpoint[part]))
    space += '  '
    part='common'
    _readCommon(endpoint[part], space)

def extractPipeline(name, pipeline, space=""):
    myEntry = pipeline[name]['entry']
    myExit  = pipeline[name]['exit']
    myFilters = pipeline[name]['filters']
    _readEndpoint(myEntry)
    print()
    _readEndpoint(myExit)
    return
    _iterateOverMap(myEntry, "   ")
    print()
    _iterateOverMap(myExit, "   ")
    return
#    elif thisThing == "<class 'ruamel.yaml.comments.CommentedSeq'>":
#        space += " "
#        for i in value:
#            _iterateOverPipeline(i, space)
#    elif thisThing == "<class 'str'>" or thisThing == "<class 'int'>":
#        print('%s%s: "%s"' % (space, key, value))
#    else:
#        print('What is this thing? "%s"' % od.items)
#
extractPipeline('pipelineTest', myObj)
#myYaml.dump(myObj, sys.stdout)
