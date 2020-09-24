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
        myLogger = logging.getLogger('Pipeline:_extractPipeline')

        try:
            myEntry = self.rawPipeline['entry']
        except Exception as err:
            raise ValueError('Unable to extract entry element from pipeline: "%s"' % err)
        else:
            try:
                self.entryObj = endpointFactory(myEntry)
            except Exception as err:
                raise ValueError('Unable to convert "entry" element to endpoint object: "%s"' % err)

        # set a default value
        self.hasFilters = False
        try:
            myFilters = self.rawPipeline['filters']
        #except Exception as err:
        except:
            #raise ValueError('Unable to extract filter element(s) from pipeline: "%s"' % err)
            myLogger.warning("There are no filters in '%s', was that expected?" % self.pipelineName)
        else:
            try:
                self.filterList = filterFactory(myFilters)
            except Exception as err:
                raise ValueError('Unable to convert "filter" element(s) to filter list: "%s"' % err)
            else:
                self.hasFilters = True

        try:
            myExit = self.rawPipeline['exit']
        except Exception as err:
            raise ValueError('Unable to extract exit element from pipeline: "%s"' % err)
        else:
            try:
                self.exitObj = endpointFactory(myExit)
            except Exception as err:
                raise ValueError('Unable to convert "exit" element to endpoint object: "%s"' % err)

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
            myLogger.debug("viewing 'entry'")
            _viewEntry(self.entryObj)
            if self.hasFilters:
                myLogger.debug("viewing filters")
                _viewFilters(self.filterList)
            myLogger.debug("viewing 'exit'")
            _viewExit(self.exitObj)
        except Exception as err:
            raise ValueError("Could not access pipeline elements in 'viewPipeline'. Exception message was '%s'" % err)


    def _buildPipeline(self):
        myLogger = logging.getLogger('Pipeline:_buildPipeline')

        def _linkEntryToExit(entryObj, exitObj):
            entryProcName = entryObj.myDict['procname']
            entryProcPath = entryObj.myDict['procpath']
            exitProcName = exitObj.myDict['procname']
            exitProcPath = exitObj.myDict['procpath']

            myLogger.info("This will link '%s' (%s) to '%s' (%s)" % (entryProcName, entryProcPath, exitProcName, exitProcPath) )

        def _linkEntryToFilters(entryObj, filterList):
            entryProcName = entryObj.myDict['procname']
            entryProcPath = entryObj.myDict['procpath']
            firstFilter = filterList[1]
            filterProcName = firstFilter.myDict['procname']
            filterProcPath = firstFilter.myDict['procpath']

            myLogger.info("This will link '%s' (%s) to '%s' (%s)" % (entryProcName, entryProcPath, filterProcName, filterProcPath) )

        def _linkFiltersToExit(filterList, exitObj):
            exitProcName = exitObj.myDict['procname']
            exitProcPath = exitObj.myDict['procpath']
            lastFilterIndex = len(filterList)
            lastFilter = filterList[lastFilterIndex]
            filterProcName = lastFilter.myDict['procname']
            filterProcPath = lastFilter.myDict['procpath']

            myLogger.info("This will link '%s' (%s) to '%s' (%s)" % (filterProcName, filterProcPath, exitProcName, exitProcPath) )

        def _linkFilterPair(filterLeft, filterRight):
            filterLeftProcName = filterLeft.myDict['procname']
            filterLeftProcPath = filterLeft.myDict['procpath']
            filterRightProcName = filterRight.myDict['procname']
            filterRightProcPath = filterRight.myDict['procpath']

            myLogger.info("This will link '%s' (%s) to '%s' (%s)" % (filterLeftProcName, filterLeftProcPath, filterRightProcName, filterRightProcPath) )

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
            if self.hasFilters:
                myLogger.debug("linking 'entry' to first filter")
                _linkEntryToFilters(self.entryObj, self.filterList)
                myLogger.debug("linking filters")
                _linkFilters(self.filterList)
                myLogger.debug("linking last filter to 'exit'")
                _linkFiltersToExit(self.filterList, self.exitObj)
            else:
                myLogger.debug("linking 'entry' to 'exit'")
                _linkEntryToExit(self.entryObj, self.exitObj)
        except Exception as err:
            raise ValueError("Could not access pipeline elements in 'buildPipeline'. Exception message was '%s'" % err)

