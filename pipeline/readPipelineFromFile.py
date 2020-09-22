import io
from ruamel.yaml import YAML

def readPipelineFromFile(pipelineName, filename):

    try:
        myFile = io.open(filename, 'r')
    except:
        raise FileNotFoundError('Unable to read from "%s".' % filename)

    try:
        myYaml = YAML()
    except:
        raise RuntimeError('Unable to create myYaml object.')

    try:
        myObj = myYaml.load(myFile)
    except:
        raise SyntaxError('Unable to get YAML from "%s".' % filename)

    try:
        myPipelineObject = myObj[pipelineName]
    except:
        raise ValueError('No pipeline "%s" in file "%s".' % (pipelineName, filename))

    return myPipelineObject
