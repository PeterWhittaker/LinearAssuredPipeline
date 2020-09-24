import logging
from .processLoggingCommon import ProcessLogging
from .startedByCommon import StartedBy

class ProcessInfo(object):

    # Mandatory input elements:
    #   name            Name of the process. More for user-friendliness
    #                   than anything else.
    #
    #   path            Required for FC definitions
    #
    #   startedBy       How this process is started. Represented by the
    #                   class StartedBy.
    #
    # Optional or generated elements:
    #   description     Optional. Human-intended description of the process
    #
    #   processType     The SELinux type associated with the process.
    #                   Can be obtained from YAML or generated herein
    #                   Default for this version: Generation; reading
    #                   from YAML not yet supported.
    #
    #   logging         Optional. How this process logs. Represented by
    #                   the ProcessLogging class.

    def __init__(self, aMap):
        self.myLogger = logging.getLogger('ProcessInfo')
        self.myLogger.warning(aMap)
        try:
            self._name = aMap['name']
        except:
            self.myLogger.warning("This 'ProcessInfo' has no 'name'. Were you expecting that?")
            self._name = ""

        try:
            self._path = aMap['path']
        except:
            raise ValueError("No 'path' for this 'ProcessInfo'.")

        try:
            self._description = aMap['description']
        except:
            self.myLogger.warning("This 'ProcessInfo' has no 'description'. Were you expecting that?")
            self._description = ""

        try:
            self._processType = aMap['processType']
        except:
            # this is expected
            self._processType = ""
        else:
            raise NotImplementedError("'ProcessInfo' does not (yet) support reading 'processType'.")

        try:
            startedBy = aMap['startedBy']
        except:
            raise ValueError("No 'startedBy' for this 'ProcessInfo'.")
        else:
            self._startedBy = StartedBy(startedBy)

# we still need to figure out some details of logging
#        try:
#            processLogging = aMap['logging']
#        except:
#            self.myLogger.warning("This 'ProcessInfo' has no 'logging'. Were you expecting that?")
#            self.logging = ""
#        else
#            self.startedBy = StartedBy(processLogging)

    def setProcessType(self, aType):
        self._processType = aType

    @property
    def name(self):
        return self._name
    @property
    def description(self):
        return self._description
    @property
    def path(self):
        return self._path
    @property
    def processType(self):
        return self._processType
    @property
    def startedByUser(self):
        return self._startedBy.byUser
    @property
    def userRole(self):
        return self._startedBy.userRole
    @property
    def processTransition(self):
        return self._startedBy.processTransition
    @property
    def startedBySystem(self):
        return self._startedBy.bySystem


