from pipeline.endpoint.endpointFactory import endpointFactory
from pipeline.filters.filterFactory import filterFactory

def extractPipeline(pipeline):

    extractedPipeline = {}

    try:
        myEntry = pipeline['entry']
    except Exception as err:
        raise ValueError('Unable to extract entry element from pipeline: "%s"' % err)
        
    try:
        myFilters = pipeline['filters']
    except Exception as err:
        raise ValueError('Unable to extract filter element(s) from pipeline: "%s"' % err)
        
    try:
        myExit = pipeline['exit']
    except Exception as err:
        raise ValueError('Unable to extract exit element from pipeline: "%s"' % err)
        
    try:
        myEntryObj = endpointFactory(myEntry)
    except Exception as err:
        raise ValueError('Unable to convert "entry" element to endpoint object: "%s"' % err)
    else:
        extractedPipeline.setdefault('entry', myEntryObj)

    try:
        myFilterList = filterFactory(myFilters)
    except Exception as err:
        raise ValueError('Unable to convert "filter" element(s) to filter list: "%s"' % err)
    else:
        extractedPipeline.setdefault('filters', myFilterList)

    try:
        myExitObj = endpointFactory(myExit)
    except Exception as err:
        raise ValueError('Unable to convert "exit" element to endpoint object: "%s"' % err)
    else:
        extractedPipeline.setdefault('exit', myExitObj)

    # we only get here if the pipeline is good
    return extractedPipeline

