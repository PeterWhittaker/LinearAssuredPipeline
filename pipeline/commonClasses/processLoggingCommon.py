class ProcessLogging(object):

    # Mandatory input elements:
    #   none            Logging info, if provided, is essentially a union
    #                   of either writing to a folder or writing to the
    #                   network, e.g., rsyslog - neither is mandatory.
    #
    #                   For simplicity at this point, both will be checked
    #                   and it will be acceptable for both to be empty.
    #                   Some mechanism for graceful behaviour is required.
    #

    ######
    #
    # NOTE: This needs more thought. Logging is likely to be done using
    #       existing facilities, so we will be consuming existing types
    #       rather than setting policy. It may be simpler to define logging
    #       merely as a series of types - but networking...?

    # Optional elements: Either logFolder or logNetwork
    #
    #   logFolder is made up of a required 'folder' and an optional 'file':
    # 
    #   folder          The folder to which the process logs. Represented
    #                   by the Folder class. See notes therein. Mandatory.
    #                   SHOULD IT BE A FOLDER? Or merely a type to which it
    #                   gets create/write/append access?
    #
    #   file            The specific file - or file type, TBD - to which
    #                   the process may write, if different from the folder.
    #                   Optional.
    #
    #   logNetwork is made up of three optional elements:
    #
    #   interfaceType   The SELinux type associated with the network interface
    #                   accessed for logging. Optional.
    #
    #   port            An optional network port used for logging. Not sure
    #                   whether this is needed.
    #
    #   protocol        An optional value taken from one of 'udp', 'tcp',
    #                   'syslog', and 'ssh'. Exists in case additional
    #                   permissions are needed based on protocol used.

    def __init__(self):
        self.message = 'This class does nothing yet.'

