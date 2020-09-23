import logging

def buildPipeline(pipeline):
    myLogger = logging.getLogger('buildPipeline')

    def _linkEntryToFilters(entryObj, filterList):
        entryProcName = entryObj.myDict['procname']
        entryProcPath = entryObj.myDict['procpath']
        firstFilter = filterList[1]
        filterProcName = firstFilter.myDict['procname']
        filterProcPath = firstFilter.myDict['procpath']

        if logging.INFO >= logging.root.level:
            message = "This will link '"
            message += entryProcName
            message += "' ("
            message += entryProcPath
            message += ") to '"
            message += filterProcName
            message += "' ("
            message += filterProcPath
            message += ")"

            myLogger.info(message)

    def _linkFiltersToExit(filterList, exitObj):
        exitProcName = exitObj.myDict['procname']
        exitProcPath = exitObj.myDict['procpath']
        lastFilterIndex = len(filterList)
        lastFilter = filterList[lastFilterIndex]
        filterProcName = lastFilter.myDict['procname']
        filterProcPath = lastFilter.myDict['procpath']

        if logging.INFO >= logging.root.level:
            message = "This will link '"
            message += filterProcName
            message += "' ("
            message += filterProcPath
            message += ") to '"
            message += exitProcName
            message += "' ("
            message += exitProcPath
            message += ")"

            myLogger.info(message)

    def _linkFilterPair(filterLeft, filterRight):
        filterLeftProcName = filterLeft.myDict['procname']
        filterLeftProcPath = filterLeft.myDict['procpath']
        filterRightProcName = filterRight.myDict['procname']
        filterRightProcPath = filterRight.myDict['procpath']

        if logging.INFO >= logging.root.level:
            message = "This will link '"
            message += filterLeftProcName
            message += "' ("
            message += filterLeftProcPath
            message += ") to '"
            message += filterRightProcName
            message += "' ("
            message += filterRightProcPath
            message += ")"

            myLogger.info(message)

    def _linkFilters(filterList):
        numFilters = len(filterList)
        for i in range(numFilters):
            filterLeftIndex = i + 1
            if filterLeftIndex == numFilters:
                return
            filterRightIndex = i + 2
            myLogger.debug("linking filters '%s' and '%s'" % (filterLeftIndex, filterRightIndex) )
            _linkFilterPair(filterList[filterLeftIndex], filterList[filterRightIndex])

    try:
        myLogger.debug("extracting 'entry'")
        entryObj   = pipeline['entry']
        myLogger.debug("extracting 'filters'")
        filterList = pipeline['filters']
        myLogger.debug("extracting 'exit'")
        exitObj    = pipeline['exit']

        myLogger.debug("linking 'entry' to first filter")
        _linkEntryToFilters(entryObj, filterList)
        myLogger.debug("linking filters")
        _linkFilters(filterList)
        myLogger.debug("linking last filter to 'exit'")
        _linkFiltersToExit(filterList, exitObj)

    except Exception as err:
        raise ValueError("Could not access pipeline elements in 'buildPipeline'. Exception message was '%s'" % err)


