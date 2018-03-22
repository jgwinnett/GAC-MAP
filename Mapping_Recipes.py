import dfClassConstructor as map

def firstRun():

    mapBot = map.CORDIS_Mapping()
    mapBot.buildDFSafe()
    mapBot.getCSV()
    mapBot.goSearch()
    mapBot = map.GTR_Mapping()
    mapBot.goSearch()
    mapBot.datarefine()
    mapBot.unifyGTR()

def updateMapping():

    mapBot = map.CORDIS_Mapping()
    mapBot.getCSV()
    mapBot.goSearch()
    mapBot = map.GTR_Mapping()
    mapBot.goSearch()
    mapBot.datarefine()
    mapBot.unifyGTR()

def classifyResults():

    mapBot = map.mappingUnified()
    mapBot.DFClassiCheck()
    mapBot.pickleDeleter(self.unifiedDFPath)

def exportUnified():

    mapBot = map.mappingUnified()

    mapBot.exportDF_CSV()
    mapBot.exportDF_excel()

firstRun()
#updateMapping()
#exportUnified()
#classifyResults()
