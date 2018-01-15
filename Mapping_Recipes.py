import dfClassConstructor as map

def firstRun():

    mapBot = map.CORDIS_Mapping()
    mapBot.buildDFSafe()
    mapBot.getCSV()
    mapBot.goSearch()
    mapBot = map.EPSRC_Mapping()
    mapBot.goSearch()
    mapBot.datarefine()
    mapBot.unifyEPSRC()

def updateMapping():

    mapBot = map.CORDIS_Mapping()
    mapBot.getCSV()
    mapBot.goSearch()
    mapBot = map.EPSRC_Mapping()
    mapBot.goSearch()
    mapBot.datarefine()
    mapBot.unifyEPSRC()

def exportUnified():

    mapBot = map.mappingUnified()

    mapBot.exportDF_CSV()
    mapBot.exportDF_excel()


firstRun()
exportUnified()
