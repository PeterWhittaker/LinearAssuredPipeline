
def _linkEntryToFilters(entryObj, filterList):
    entryProcName = entryObj.myDict['procname']
    entryProcPath = entryObj.myDict['procpath']
    firstFilter = filterList[1]
    filterProcName = firstFilter.myDict['procname']
    filterProcPath = firstFilter.myDict['procpath']
    message = "This will link '"
    message += entryProcName
    message += "' ("
    message += entryProcPath
    message += ") to '"
    message += filterProcName
    message += "' ("
    message += filterProcPath
    message += ")"

    print(message)

def _linkFiltersToExit(filterList, exitObj):
    exitProcName = exitObj.myDict['procname']
    exitProcPath = exitObj.myDict['procpath']
    lastFilterIndex = len(filterList)
    lastFilter = filterList[lastFilterIndex]
    filterProcName = lastFilter.myDict['procname']
    filterProcPath = lastFilter.myDict['procpath']
    message = "This will link '"
    message += filterProcName
    message += "' ("
    message += filterProcPath
    message += ") to '"
    message += exitProcName
    message += "' ("
    message += exitProcPath
    message += ")"

    print(message)

def _linkFilterPair(filterLeft, filterRight):
    filterLeftProcName = filterLeft.myDict['procname']
    filterLeftProcPath = filterLeft.myDict['procpath']
    filterRightProcName = filterRight.myDict['procname']
    filterRightProcPath = filterRight.myDict['procpath']
    message = "This will link '"
    message += filterLeftProcName
    message += "' ("
    message += filterLeftProcPath
    message += ") to '"
    message += filterRightProcName
    message += "' ("
    message += filterRightProcPath
    message += ")"

    print(message)

def _linkFilters(filterList):
    numFilters = len(filterList)
    for i in range(numFilters):
        filterLeftIndex = i + 1
        if filterLeftIndex == numFilters:
            return
        filterRightIndex = i + 2
        _linkFilterPair(filterList[filterLeftIndex], filterList[filterRightIndex])

def buildPipeline(pipeline):
    entryObj   = pipeline['entry']
    filterList = pipeline['filters']
    exitObj    = pipeline['exit']

    _linkEntryToFilters(entryObj, filterList)
    _linkFilters(filterList)
    _linkFiltersToExit(filterList, exitObj)

