from pipeline.endpoint.endpointFactory import endpointFactory
from pipeline.filters.filterFactory import filterFactory

def _viewEntry(myEntryObj):
    print(myEntryObj.getMsg)
    myEntryObj.cycleThrough()
    print()

def _viewExit(myExitObj):
    print(myExitObj.getMsg)
    myExitObj.cycleThrough()
    print()

def _viewFilters(myFilterList):
    numFilters = len(myFilterList)
    print('%s filters' % numFilters)
    for i in range(numFilters):
        key = i + 1
        print(myFilterList[key].getMsg)
        myFilterList[key].cycleThrough()
        print()

def viewPipeline(pipeline):
    entryObj   = pipeline['entry']
    filterList = pipeline['filters']
    exitObj    = pipeline['exit']

    _viewEntry(entryObj)
    _viewFilters(filterList)
    _viewExit(exitObj)

def extractPipeline(pipeline):

    extractedPipeline = {}

    try:
        myEntry = pipeline['entry']
    except:
        raise ValueError('Unable to extract entry element from pipeline.')
        
    try:
        myFilters = pipeline['filters']
    except:
        raise ValueError('Unable to extract filter element(s) from pipeline.')
        
    try:
        myExit = pipeline['exit']
    except:
        raise ValueError('Unable to extract exit element from pipeline.')
        
    try:
        myEntryObj = endpointFactory(myEntry)
    except:
        raise ValueError('Unable to convert "entry" element to endpoint object.')
    else:
        extractedPipeline.setdefault('entry', myEntryObj)

    try:
        myFilterList = filterFactory(myFilters)
    except:
        raise ValueError('Unable to convert "filter" element(s) to filter list.')
    else:
        extractedPipeline.setdefault('filters', myFilterList)

    try:
        myExitObj = endpointFactory(myExit)
    except:
        raise ValueError('Unable to convert "exit" element to endpoint object.')
    else:
        extractedPipeline.setdefault('exit', myExitObj)

    # we only get here if the pipeline is good
    return extractedPipeline

