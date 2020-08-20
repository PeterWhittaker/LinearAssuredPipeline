class Filter(object):
    def __init__(self, aFilter):
        self.message = 'This filter does nothing yet.'
        self.startdby= 'startedBy'
        self.myDict = {
            'order': aFilter['order'],
            'name': aFilter['processInfo']['name'],
            'processType': aFilter['processInfo']['processType'],
            self.startdby: aFilter['processInfo'][self.startdby],
            'inFolderPath':aFilter['in']['path'],
            'inFolderType':aFilter['in']['folderType'],
            'outFolderPath':aFilter['out']['path'],
            'outFolderType':aFilter['out']['folderType'],
            'errFolderPath':aFilter['err']['path'],
            'errFolderType':aFilter['err']['folderType']
        }

    def cycleThrough(self):
        for key, value in self.myDict.items():
            if key is not self.startdby:
                print(key, value)
            else:
                for key, value in self.myDict[self.startdby].items():
                    print(key, value)

    def validateNext(self, nextFilter):
        try:
            nextOne = nextFilter.order
        except:
            raise TypeError('validateNext(): was passed something other than a valid filter.')

        if not isinstance(nextOne, int):
            raise TypeError('validateNext(): "order" is not an integer.')

        expectedOrder = self.order + 1
        if not expectedOrder == nextOne:
            raise ValueError('validateNext(): filter passed is not next in line; expected "%s", got "%s".' %s (expectedOrder, nextOne))

    @property
    def order(self):
        return self.myDict['order']

    @property
    def getMsg(self):
        return self.message

def filterFactory(aFilter):
    try:
        order = aFilter['order']
    except:
        raise TypeError('filterFactory(): Unsupported type  - no "order" in map.')

    if not isinstance(order, int):
        raise TypeError('filterFactory(): "order" is not an integer.')

    myObj = Filter(aFilter)
    return myObj

