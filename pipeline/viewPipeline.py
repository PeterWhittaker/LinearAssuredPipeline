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

