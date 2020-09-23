class Folder(object):

    # Mandatory input elements:
    #   path            Required, both for FC definitions in the pipeline
    #                   and for setting permissions appropriately when used
    #                   in logging.
    #
    # Optional or generated elements:
    #   folderType      The SELinux type associated with the folder
    #                   Can be obtained from YAML or generated herein.
    #                   Implementation details vary by use: For folders
    #                   used in the pipeline, types are generated; reading
    #                   from the YAML not yet supported. For folders used
    #                   in logging, reading is the only supported option.
    #
    #   fileTransition  An SELinux type to which files created in this
    #                   folder should be transitioned. Optional. Not yet
    #                   supported. Applicable to the pipeline only and not
    #                   to logging (right)?

    def init(self):
        self.message = 'This class does nothing yet.'

