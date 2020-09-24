import logging

class StartedBy(object):

    # Mandatory input elements:
    #   none            Well, not really: StartedBy is a union of user,
    #                   system, or process.
    #
    #                   NOTE: Only system and user are currently supported. 
    #
    #                   To be useful, one of the two supported options MUST
    #                   be present - with neither, proper permissions cannot
    #                   be set.
    #
    #                   User means that the process is started by a user:
    #                   appropriate user permissions and transitions must
    #                   be defined.
    #
    #                   System means that the process is started by the OS
    #                   itself, e.g., via init or systemd - the appropriate
    #                   transition from systemd, e.g., must be defined.
    #
    #   user consists of two components:
    #
    #   userRole        The SELinux role allowed to start this process
    #                   (permission based on the generated type of the
    #                   process). Mandatory if user is specified.
    #
    #   processTransition
    #                   Whether the process type should transition when
    #                   the process is invoked. Optional. May not make
    #                   much sense - transitioning is likely always required,
    #                   at least in the current implementation.
    #
    #  system consists of a single component:
    #
    #  systemTransition
    #                   If present, it simply means that the transition
    #                   from system process type to the process's actual
    #                   process type must be defined; the value provided
    #                   is irrelevant, a place holder, really.

    def __init__(self, aMap):
        self.myLogger = logging.getLogger('StartedBy')
        try:
            self._userRole = aMap['userRole']
        except:
            # this is fine - could be system
            self.byUser = False
        else:
            self.byUser = True
            try:
                self._processTransition = aMap['processTransition']
            except:
                self.myLogger.warning("This 'StartedBy' contains a 'userRole' but no 'processTransition'; is this expected?")
                self._processTransition = ""

        try:
            system = aMap['systemTransition']
        except:
            # this is fine - could be user
            self.bySystem = False
        else:
            self.bySystem = True
            self._userRole = ""
            self._processTransition = ""

        if self.byUser and self.bySystem:
            raise ValueError("'StartedBy' must contain EITHER 'userRole' or 'systemTransition'; both are present.")

        if not self.byUser and not self.bySystem:
            if self.byUser:
                byUserSnip = "userRole is present"
            else:
                byUserSnip = "userRole is absent"
            if self.bySystem:
                bySystemSnip = "systemTransition is present"
            else:
                bySystemSnip = "systemTransition is absent"
            raise ValueError("'StartedBy' must contain EITHER 'userRole' or 'systemTransition'; %s and %s." % (byUserSnip, bySystemSnip) )

    @property
    def userRole(self):
        return self._userRole
    @property
    def processTransition(self):
        return self._processTransition


