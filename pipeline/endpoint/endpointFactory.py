import logging
from ..commonClasses.processInfoCommon import ProcessInfo

class Endpoint(object):
    def __init__(self, anEndpoint):
        self.message = 'This does nothing yet.'
        self.myLogger = logging.getLogger('Endpoint')
        endpttyp = 'type'
        protocol = 'protocol'
        infctype = 'interfaceType'
        procpath = 'procpath'
        self.startdby = 'startedBy'
        self.processInfo = ProcessInfo(anEndpoint['common']['processInfo'])
        self.myDict = {
            endpttyp: anEndpoint[endpttyp],
            protocol: anEndpoint[protocol],
            infctype: anEndpoint['common'][infctype],
            'procname': self.processInfo.name,
            'procpath': self.processInfo.path,
        }

    def cycleThrough(self):
        for key, value in self.myDict.items():
            if key is not self.startdby:
                self.myLogger.info("%s%s" % (key, value))
            else:
                for key, value in self.myDict[self.startdby].items():
                    self.myLogger.info("%s%s" % (key, value))

    @property
    def getMsg(self):
        return self.message

class Entry(Endpoint):
    def __init__(self, anEndpoint):
        super().__init__(anEndpoint)
        foldpath = 'path'
        self.myDict.setdefault('foldpath', anEndpoint['folder'][foldpath])
        self.message = 'This entry does nothing yet.'

class Receiver(Entry):
    def __init__(self, anEndpoint):
        super().__init__(anEndpoint)
        self.message = 'This receiver does nothing yet.'
        try:
            thePort = anEndpoint['port']
        except:
            raise TypeError('Receiver expects a port, was missing from YAML file')
        if not isinstance(thePort, int):
            raise TypeError('Value for "port" in YAML was not of type "int"')
        self.myDict.setdefault('port', thePort)

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
        raise TypeError("endpointFactory(): Invalid map or other data element passed as endpoint: 'type' is missing.")

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

