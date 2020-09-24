import logging
from ..commonClasses.processInfoCommon import ProcessInfo

class Endpoint(object):
    def __init__(self, anEndpoint):
        self.myLogger = logging.getLogger('Endpoint')
        common   = 'common'
        endpttyp = 'type'
        protocol = 'protocol'
        infctype = 'interfaceType'
        procinfo = 'processInfo'
        self.processInfo = ProcessInfo(anEndpoint[common][procinfo])
        self.myDict = {
            endpttyp: anEndpoint[endpttyp],
            protocol: anEndpoint[protocol],
            infctype: anEndpoint[common][infctype],
            'procname': self.processInfo.name,
            'procpath': self.processInfo.path,
            'procStartedByUser'   : self.processInfo.startedByUser,
            'procUserRole'        : self.processInfo.userRole,
            'procTransition'      : self.processInfo.processTransition,
            'procStartedBySystem' : self.processInfo.startedBySystem,
        }

    def cycleThrough(self):
        for key, value in self.myDict.items():
            self.myLogger.info("%s: '%s'" % (key, value))

class Entry(Endpoint):
    def __init__(self, anEndpoint):
        super().__init__(anEndpoint)
        foldpath = 'path'
        self.myDict.setdefault('foldpath', anEndpoint['folder'][foldpath])

class Receiver(Entry):
    def __init__(self, anEndpoint):
        super().__init__(anEndpoint)
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

class Exit(Endpoint):
    def __init__(self, anEndpoint):
        super().__init__(anEndpoint)

class Sender(Exit):
    def __init__(self, anEndpoint):
        super().__init__(anEndpoint)

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

