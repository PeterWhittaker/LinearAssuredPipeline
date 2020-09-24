import io
import logging
from ruamel.yaml import YAML
from .endpoint.endpointFactory import endpointFactory
from .filters.filterFactory import filterFactory

class Pipeline(object):
    def __init__(self, pipelineName, pipelineFile):
        self.pipelineName = pipelineName
        self.pipelineFile = pipelineFile
        self.myLogger = logging.getLogger('Pipeline')

        self.rawPipeline = self._readPipelineFromFile()

        self.pipeline = self._extractPipeline()

        if logging.DEBUG >= logging.root.level:
            self._viewPipeline()

    def build(self):
        self._buildPipeline()

    def _readPipelineFromFile(self):
        try:
            myFile = io.open(self.pipelineFile, 'r')
        except Exception as err:
            raise FileNotFoundError("Unable to read from '%s'. Exception message '%s'" % (self.pipelineFile, err))

        try:
            myYaml = YAML()
        except Exception as err:
            raise RuntimeError("Unable to create myYaml object. Exception message '%s'" % err)

        try:
            myObj = myYaml.load(myFile)
        except Exception as err:
            raise SyntaxError("Unable to get YAML from '%s'. Exception message '%s'" % (self.pipelineFile, err))

        try:
            myPipelineObject = myObj[self.pipelineName]
        except Exception as err:
            raise ValueError("No pipeline '%s' in file '%s'. Exception message '%s'" % (self.pipelineName, self.pipelineFile, err))

        return myPipelineObject

    def _extractPipeline(self):
        extractedPipeline = {}

        try:
            myEntry = self.rawPipeline['entry']
        except Exception as err:
            raise ValueError('Unable to extract entry element from pipeline: "%s"' % err)
            
        try:
            myFilters = self.rawPipeline['filters']
        except Exception as err:
            raise ValueError('Unable to extract filter element(s) from pipeline: "%s"' % err)
            
        try:
            myExit = self.rawPipeline['exit']
        except Exception as err:
            raise ValueError('Unable to extract exit element from pipeline: "%s"' % err)
            
        try:
            myEntryObj = endpointFactory(myEntry)
        except Exception as err:
            raise ValueError('Unable to convert "entry" element to endpoint object: "%s"' % err)

        extractedPipeline.setdefault('entry', myEntryObj)

        try:
            myFilterList = filterFactory(myFilters)
        except Exception as err:
            raise ValueError('Unable to convert "filter" element(s) to filter list: "%s"' % err)

        extractedPipeline.setdefault('filters', myFilterList)

        try:
            myExitObj = endpointFactory(myExit)
        except Exception as err:
            raise ValueError('Unable to convert "exit" element to endpoint object: "%s"' % err)

        extractedPipeline.setdefault('exit', myExitObj)

        # we only get here if the pipeline is good
        return extractedPipeline

    def _viewPipeline(self):
        myLogger = logging.getLogger('Pipeline:_viewPipeline')

        def _viewEntry(myEntryObj):
            myLogger.debug("in _viewEntry")
            myLogger.info(myEntryObj.getMsg)
            myEntryObj.cycleThrough()
            myLogger.info("")

        def _viewExit(myExitObj):
            myLogger.info(myExitObj.getMsg)
            myExitObj.cycleThrough()
            myLogger.info("")

        def _viewFilters(myFilterList):
            numFilters = len(myFilterList)
            myLogger.info('%s filters' % numFilters)
            for i in range(numFilters):
                key = i + 1
                myLogger.info(myFilterList[key].getMsg)
                myFilterList[key].cycleThrough()
                myLogger.info("")

        try:
            myLogger.debug("extracting 'entry'")
            entryObj   = self.pipeline['entry']
            myLogger.debug("extracting 'filters'")
            filterList = self.pipeline['filters']
            myLogger.debug("extracting 'exit'")
            exitObj    = self.pipeline['exit']

            myLogger.debug("viewing 'entry'")
            _viewEntry(entryObj)
            myLogger.debug("viewing filters")
            _viewFilters(filterList)
            myLogger.debug("viewing 'exit'")
            _viewExit(exitObj)

        except Exception as err:
            raise ValueError("Could not access pipeline elements in 'viewPipeline'. Exception message was '%s'" % err)


    def _buildPipeline(self):
        myLogger = logging.getLogger('Pipeline:_buildPipeline')

        def _linkEntryToFilters(entryObj, filterList):
            entryProcName = entryObj.myDict['procname']
            entryProcPath = entryObj.myDict['procpath']
            firstFilter = filterList[1]
            filterProcName = firstFilter.myDict['procname']
            filterProcPath = firstFilter.myDict['procpath']

            if logging.INFO >= logging.root.level:
                message = "This will link '"
                message += entryProcName
                message += "' ("
                message += entryProcPath
                message += ") to '"
                message += filterProcName
                message += "' ("
                message += filterProcPath
                message += ")"

                myLogger.info(message)

        def _linkFiltersToExit(filterList, exitObj):
            exitProcName = exitObj.myDict['procname']
            exitProcPath = exitObj.myDict['procpath']
            lastFilterIndex = len(filterList)
            lastFilter = filterList[lastFilterIndex]
            filterProcName = lastFilter.myDict['procname']
            filterProcPath = lastFilter.myDict['procpath']

            if logging.INFO >= logging.root.level:
                message = "This will link '"
                message += filterProcName
                message += "' ("
                message += filterProcPath
                message += ") to '"
                message += exitProcName
                message += "' ("
                message += exitProcPath
                message += ")"

                myLogger.info(message)

        def _linkFilterPair(filterLeft, filterRight):
            filterLeftProcName = filterLeft.myDict['procname']
            filterLeftProcPath = filterLeft.myDict['procpath']
            filterRightProcName = filterRight.myDict['procname']
            filterRightProcPath = filterRight.myDict['procpath']

            if logging.INFO >= logging.root.level:
                message = "This will link '"
                message += filterLeftProcName
                message += "' ("
                message += filterLeftProcPath
                message += ") to '"
                message += filterRightProcName
                message += "' ("
                message += filterRightProcPath
                message += ")"

                myLogger.info(message)

        def _linkFilters(filterList):
            numFilters = len(filterList)
            for i in range(numFilters):
                filterLeftIndex = i + 1
                if filterLeftIndex == numFilters:
                    return
                filterRightIndex = i + 2
                myLogger.debug("linking filters '%s' and '%s'" % (filterLeftIndex, filterRightIndex) )
                _linkFilterPair(filterList[filterLeftIndex], filterList[filterRightIndex])

        try:
            myLogger.debug("extracting 'entry'")
            entryObj   = self.pipeline['entry']
            myLogger.debug("extracting 'filters'")
            filterList = self.pipeline['filters']
            myLogger.debug("extracting 'exit'")
            exitObj    = self.pipeline['exit']

            myLogger.debug("linking 'entry' to first filter")
            _linkEntryToFilters(entryObj, filterList)
            myLogger.debug("linking filters")
            _linkFilters(filterList)
            myLogger.debug("linking last filter to 'exit'")
            _linkFiltersToExit(filterList, exitObj)

        except Exception as err:
            raise ValueError("Could not access pipeline elements in 'buildPipeline'. Exception message was '%s'" % err)

