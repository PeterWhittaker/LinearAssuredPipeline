class Filter(object):
    def __init__(self, aFilter):
        self.message = 'This filter does nothing yet.'
        self.startdby= 'startedBy'
        # if this was replaced by a series of properties, we would have more
        # control over raising NotImplementedError for parts not yet supported,
        # e.g., folderTypes - for now we will autogenerate them
        self.myDict = {
            'order': aFilter['order'],
            'name': aFilter['processInfo']['name'],
            'processType': aFilter['processInfo']['processType'],
            self.startdby: aFilter['processInfo'][self.startdby],
            'inFolderPath':aFilter['in']['path'],
            #'inFolderType':aFilter['in']['folderType'],
            'outFolderPath':aFilter['out']['path'],
            #'outFolderType':aFilter['out']['folderType'],
            'errFolderPath':aFilter['err']['path'] #,
            #'errFolderType':aFilter['err']['folderType']
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

def _filterFactory(aFilter):
    try:
        order = aFilter['order']
    except:
        raise TypeError('filterFactory(): Unsupported type  - no "order" in map.')

    if not isinstance(order, int):
        raise TypeError('filterFactory(): "order" is not an integer.')

    myObj = Filter(aFilter)
    return myObj

def filterFactory(myFilters):
    filterList = {}
    for myFilter in myFilters:
        myFilterObj = _filterFactory(myFilter)
        filterList.setdefault(myFilterObj.order, myFilterObj)

    numFilters = len(filterList)
    try:
        for i in range(numFilters):
            key = i+1 # lists start at 0, filters at 1
            try:
                order = filterList[key]
            except:
                raise ValueError('Could not find filter#%s, is the list monotonic starting at 1?' % key)
    except ValueError:
        keys = ''
        for i in sorted (filterList.keys()):
            if not keys == '':
                keys += ', '
            keys += '%i' % i
        message1 = 'Unable to initialize the filter list: non-monotonic orders.\n'
        message2 = 'Filter "order" must start at "1" and increase monotonically by 1.\n'
        message3 = 'Filter "order" values are "%s".' % keys
        message = message1 + message2 + message3
        raise ValueError(message)
    except Exception as err:
        print('Unknown exception initializing the filter list: %s' % err)
    else:
        return filterList
    # if we get here, we were unable to return the actual list
    # and we should NEVER be able to get here....
    return ''

