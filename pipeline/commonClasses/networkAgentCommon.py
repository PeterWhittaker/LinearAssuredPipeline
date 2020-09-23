class NetworkAgent(object):

    # Mandatory input elements
    #   interfaceType   The SELinux type associated with the network interface
    #                   accessed by this network agent. Mandatory. Utility TBD.
    #
    #   processInfo     Common process elements, specified in class ProcessInfo
    #
    # Optional or generated elements:
    #   none

    def init(self):
        self.message = 'This class does nothing yet.'

