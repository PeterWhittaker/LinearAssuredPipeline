class Endpoint(object):
    def __init__(self, anEndpoint):
        self.message = 'This does nothing yet.'
        endpttyp = 'type'
        protocol = 'protocol'
        infctype = 'interfaceType'
        foldpath = 'path'
        foldtype = 'folderType'
        procname = 'name'
        proctype = 'processType'
        self.startdby = 'startedBy'
        self.myDict = {
            endpttyp: anEndpoint[endpttyp],
            protocol: anEndpoint[protocol],
            infctype: anEndpoint['common'][infctype],
            foldpath: anEndpoint['common']['folder'][foldpath],
            foldtype: anEndpoint['common']['folder'][foldtype],
            procname: anEndpoint['common']['processInfo'][procname],
            proctype: anEndpoint['common']['processInfo'][proctype],
            self.startdby: anEndpoint['common']['processInfo'][self.startdby]
        }

    def cycleThrough(self):
        for key, value in self.myDict.items():
            if key is not self.startdby:
                print(key, value)
            else:
                for key, value in self.myDict[self.startdby].items():
                    print(key, value)

    @property
    def getMsg(self):
        return self.message

class Entry(Endpoint):
    def __init__(self, anEndpoint):
        super().__init__(anEndpoint)
        self.message = 'This entry does nothing yet.'

class Receiver(Entry):
    def __init__(self, anEndpoint):
        super().__init__(anEndpoint)
        self.message = 'This receiver does nothing yet.'
        self.myDict.setdefault('port', anEndpoint['port'])

class Getter(Entry):
    def __init__(self, anEndpoint):
        super().__init__(anEndpoint)
        self.message = 'This getter does nothing yet.'

class Exit(Endpoint):
    def __init__(self, anEndpoint):
        super().__init__(anEndpoint)
        self.message = 'This exit does nothing yet.'

class Sender(Exit):
    def __init__(self, anEndpoint):
        super().__init__(anEndpoint)
        self.message = 'This sender does nothing yet.'

def endpointFactory(myEndpoint):
    try:
        theType = myEndpoint['type']
    except:
        raise TypeError('endpointFactory(): Invalid map or other data element passed as endpoint.')

    if  theType == 'receiver':
        myObj = Receiver(myEndpoint)
        return myObj
    elif theType == 'getter':
        myObj = Getter(myEndpoint)
        return myObj
    elif theType == 'sender':
        myObj = Sender(myEndpoint)
        return myObj
    else:
        raise TypeError('endpointFactory(): Unsupported endpoint type "%s".' % theType)

