# LinearAssuredPipeline

Summary
-------

Tools and YAML schema for defining a Linear Pipeline and generating SELinux policy sufficient to make this pipeline assured.

Background
----------

A *linear assured pipeline* provides a verifiable, tamper-proof, and non-bypassable mechanism
for transferring information between information domains, e.g., between two isolated networks.

For example, a *data diode* used in a [Unidirectional network](https://en.wikipedia.org/wiki/Unidirectional_network) might consist of three processes:

1. A reading process that
   1. Connects to a server in one network domain, and
   2. Copies files from that server to the folder 'incoming' on the diode;
2. An antivirus filter that
   1. Reads files from 'incoming', and, if they pass its checks
   2. Moves the files to the 'outgoing' folder on the diode; and
3. A writing process that
   1. Monitors the 'outgoing' folder for new files,
   2. Writes these files to a server in another network domain, and
   3. Deletes these files from 'outgoing'.

These three processes represent a linear pipeline:

1. Files move from the source network to the diode via the reading process;
2. Files move from the incoming folder to the outgoing folder via the AV process;
3. Files move from the diode to the destination network via the writing process.

In order to be an assured pipeline, appropriate security mechanisms must be in place to ensure that:

- Only the reader process can read files from the source network
- Only the reader process can write files to 'incoming'
- Only the AV process can read files from 'incoming'
- Only the AV process can delete files from 'incoming'
- Only the AV process can write files to 'outgoing'
- Only the writer process can read files from 'outgoing'
- Only the writer process can delete files from 'outgoing'
- Only the writer process can write files to the destination network

Mandatory Access Controls (MAC) specified in an immutable system-wide security policy can provide
the necessary security mechanisms. [SELinux](https://selinuxproject.org/page/Main_Page) Type Enforcement (TE) 
provides a workable scheme for specifying the MAC necessary to a linear assured pipeline,
e.g., by associating distinct SELinux types with each network interface and with each of the transit folders.

Workable, but not necessarily straightforward: Defining SELinux policy can be both complex and errorprone.

What this repo is about
-----------------------

Common techniques when generating SELinux policy are to borrow from existing policies for
comparable services and to generate as much of the policy as possible using SELinux macros.
While one could jump directly into developing policy for a linear assured pipeline, borrowing
and tweaking along the way, the question is begged as to whether or not the pipeline is itself
well defined.

The approach taken in this repo is to
1. Start with pipeline definition,
2. Validate that the pipeline is well-defined, with all steps and all transitions documented, and
3. Generate SELinux policy statements that will themselves be used to generate SELinux policy, i.e., necessary *.te, *.if, and *fc files.

Some familiarity with SELinux is assumed.

How it works
------------

1. A general schema has been defined to specify all pipeline elements; a pipeline is assumed to consist of
   1. An entry process that receives (listening server) or reads (polling or other client) files from one domain,
   2. Zero or more filters that move files as they process them, and
   3. An exit process that writes files to another domain.
2. This schema is used to validate pipeline definitions
3. Once a pipeline definition has been validated, a generator process cycles through the
definition and generates SELinux policy statements, making any necessary connections between
steps, e.g., only filter1 can write to folderA but not read from or delete from it, while only
filter2 can read from and delete from folderA, but it cannot not write to it.

(With a bit of work, the pipeline schema could be extended to streaming protocols as well. Well, I think it's a bit of work. I may find out.)

Where we are, what's next
-------------------------

"How it works" steps 1 and 2 are complete:
1. `schema.yaml` defines all pipeline properties and elements relevant from an SELinux perspective
2. there is a sample pipeline definition, `testSchema.yml`, that appears to be correct and validates according to `schema.yaml`

[Yamale](https://github.com/23andMe/Yamale) is used for schema specification and validation.

Step 3 is one of the next steps, among others, in no particular order:
- The generator needs to be written; this will probably be in Python, because
   - Yamale and a few other tools are in Python, so I can borrow code where necessary
   - SELinux uses a lot of Python in policy generation, so I can borrow code...
   - It's about time I learned Python....
- The toolchain is, uh, well, it's not.
   - schema.yaml should be created by a utility that takes as its argument(s) what's/re being defined
   (the schema contains other things pertinent to my current work) and generates the actual
   schema file using what's being defined and a schema template.
   - The Makefile is pretty weak, it was mostly a way of capturing what I was doing to install dependencies
   - There is virtually no testing, and none of it automated; tests are needed for
      - pipelines
      - processes
      - and all the other things defined in the schema
- the schema itself could use a second or third set of eyes to make sure it is correct
   - as noted above, it defines more than pipelines, because I have a few other things on the go
- this README could use a few examples
   - more than a few
   - and maybe some images
- every *what's next* item needs an issue
