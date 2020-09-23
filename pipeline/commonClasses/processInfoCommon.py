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

    def init(self):
        self.message = 'This class does nothing yet.'

