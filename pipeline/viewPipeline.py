import logging

def viewPipeline(pipeline):

    myLogger = logging.getLogger('viewPipeline')

    def _viewEntry(myEntryObj):
        myLogger.debug("in _viewEntry")
        myLogger.info(myEntryObj.getMsg)
        myEntryObj.cycleThrough()
        myLogger.info("")

    def _viewExit(myExitObj):
        myLogger.info(myExitObj.getMsg)
        myExitObj.cycleThrough()
        myLogger.info("")

    def _viewFilters(myFilterList):
        numFilters = len(myFilterList)
        myLogger.info('%s filters' % numFilters)
        for i in range(numFilters):
            key = i + 1
            myLogger.info(myFilterList[key].getMsg)
            myFilterList[key].cycleThrough()
            myLogger.info("")

    try:
        myLogger.debug("extracting 'entry'")
        entryObj   = pipeline['entry']
        myLogger.debug("extracting 'filters'")
        filterList = pipeline['filters']
        myLogger.debug("extracting 'exit'")
        exitObj    = pipeline['exit']

        myLogger.debug("viewing 'entry'")
        _viewEntry(entryObj)
        myLogger.debug("viewing filters")
        _viewFilters(filterList)
        myLogger.debug("viewing 'exit'")
        _viewExit(exitObj)

    except Exception as err:
        raise ValueError("Could not access pipeline elements in 'viewPipeline'. Exception message was '%s'" % err)

