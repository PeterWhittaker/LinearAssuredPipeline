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

    def init(self):
        self.message = 'This class does nothing yet.'

