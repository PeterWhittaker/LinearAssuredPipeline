import io
from ruamel.yaml import YAML

def readPipelineFromFile(pipelineName, filename):

    try:
        myFile = io.open(filename, 'r')
    except Exception as err:
        raise FileNotFoundError("Unable to read from '%s'. Exception message '%s'" % (filename, err))

    try:
        myYaml = YAML()
    except Exception as err:
        raise RuntimeError("Unable to create myYaml object. Exception message '%s'" % err)

    try:
        myObj = myYaml.load(myFile)
    except Exception as err:
        raise SyntaxError("Unable to get YAML from '%s'. Exception message '%s'" % (filename, err))

    try:
        myPipelineObject = myObj[pipelineName]
    except Exception as err:
        raise ValueError("No pipeline '%s' in file '%s'. Exception message '%s'" % (pipelineName, filename, err))

    return myPipelineObject
