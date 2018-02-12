import pandas as pd
import numpy as np
import GTR_API_access as ea
import datetime
import os.path

"""This module allows users to identify projects that are relevant to them from two sources - GTR's 'Gateway To Research' and CORDIS' Horizon 2020 Projects.
    The user must idenfy applicable keywords and storethem in 'Trawl Keywords.txt'.
    Once done they may run one of the basic recipes in Mapping_Recipes to receive a unified list of applicable projects from both sources.
    These are exportable to both .CSV and .xlsx. If new keywords are desired they need only to be added and the list will be updated.

    TO-DO:
        Allow users a 'confirmation of applicability' list & feed that into the refinement loop
"""

class mappingUnified():

    def __init__(self):
        self.projName = None
        self.projDesc = None
        self.projLead = None
        self.projCollab = None
        self.projFunding = None
        self.projGrouping = None
        self.projSource = None
        self.unifiedDF = None
        self.classifiedDF= None
        self.searchTerms = None
        self.Response = None
        self.classiDFExists = False

        self.dfUnifiedPath = "Pickles/unifiedDF.pickle"
        self.dfClassiPath = "Pickles/classifiedDF.pickle"
        self.excelImportPath = "Excel/classifiedProjects.xlsx"
        self.csvImportPath = "CSV/classifiedProjects.csv"
        self.excelExportPath = "Excel/unifiedProjects.xlsx"
        self.csvExportPath = "CSV/unifiedProjects.csv"

        self.Columns = ["projName", "projDesc", "projLead", "projCollab", "projFunding", "projGrouping", "projSource", "projApplic" ]

        self.getTrawlKeywords()
        self.DFClassiFlagCheck()


    def buildDF(self):

        """ Blind build a new DataFrame using appropriate columns, use buildDFSafe() to avoid accidental overwrites"""

        df = pd.DataFrame(columns= self.Columns, dtype='str')
        self.checkFolder('Pickles')
        df.to_pickle(self.dfUnifiedPath)
        try:
            pickleDeleter("Pickles/GTR_raw.pickle")
        except:
            KeyError
        try:
            pickleDeleter("Pickles/GTR_refined.pickle")
        except:
            KeyError
        print("New DataFrame created and pickled!")
        self.unifiedDF= df

    def pickleDeleter(self, picklePath):
        os.remove(picklePath)

    def buildDFSafe(self):

        """Check if DF exists, if not build an empty DataFrame with appropriate columns and pickle it"""

        # check if a pickle file with name unifiedDF.pickle is an existing file
        if os.path.isfile(self.dfUnifiedPath):
            print("A unified DataFrame already exists for this project. Creating a new DataFrame will result in all previously stored data being lost")
            print("If you wish to continue, please type 'Yes', else the existing DataFrame will be opened instead.")
            yesNo = input('Confirm over-write:   ').lower()

            if yesNo == "yes":
                self.buildDF()
            else:
                self.openDF()

        else:
            self.buildDF()

    def buildDFClassi(self):

        ### TBI - what if a user previously used excel then this time used CSV?

        if os.path.exists(self.excelImportPath):
            self.classifiedDF = pd.read_excel(self.excelImportPath)
            self.DFClassiClose()
            print("Excel sheet imported")
        elif os.path.exists(self.csvImportPath):
            self.classifiedDF = pd.read_csv(self.csvImportPath)
            self.DFClassiClose()
        else:
            print("No classified CSV or Excel file found - terminating program.")
            quit()

    def DFClassiCheck(self):

        if not os.path.exists(self.dfClassiPath):
            self.buildDFClassi()
        else:
            self.classifiedDF = pd.read_pickle(self.dfClassiPath)
            self.classiDFUpdate()

    def DFClassiFlagCheck(self):

        if os.path.exists(self.dfClassiPath):
            self.classiDFExists = True
            self.classifiedDF = pd.read_pickle(self.dfClassiPath)

    def classiDFUpdate(self):

        if os.path.exists(excelImportPath):
            print("Excel sheet imported")
            tempDF = pd.read_excel(self.excelImportPath)

        elif os.path.exists(csvImportPath):
            tempDF = pd.read_csv(self.csvImportPath)
        else:
            print("No classified CSV or Excel file found - terminating program.")
            quit()


        self.classifiedDF = self.classifiedDF.append(tempDF)
        self.DFClassiClose()

    def DFClassiClose(self):

        """Pickles the open unified DataFrame """
        self.classifiedDF.to_pickle(self.dfClassiPath)
        print('Classified DataFrame successfully pickled!')


    def checkFolder (self,folder):

        """ Checks if requisite folder has been created. If not, create them """

        if not os.path.exists(folder):
            os.makedirs(folder)


    def openDF(self):

        """ Open the existing unified DataFrame pickle and return it """

        self.checkFolder('Pickles')
        df = pd.read_pickle(self.dfUnifiedPath)
        self.unifiedDF= df

    def closeDF_UNIFIED(self):

        """Pickles the open unified DataFrame """
        self.unifiedDF.to_pickle(self.dfUnifiedPath)
        print('Unified DataFrame successfully pickled!')

    def exportDF_CSV(self):

        """Exports the DataFrame to a .csv file"""
        self.openDF()
        self.checkFolder('CSV')
        self.unifiedDF.to_csv(self.csvExportPath, sep=",", header = self.Columns, index=False)
        print("DataFrame exported successfully to CSV/unifiedProjects.csv")

    def exportDF_excel(self):

        """ Exports the DataFrame to a .xlsx file"""
        self.openDF()
        self.checkFolder('Excel')
        self.unifiedDF.to_excel(self.excelExportPath, sheet_name = 'All Projects', header = self.Columns, index=False)
        print("DataFrame exported successfully to Excel/unifiedProjects.xlsx")

    def getTrawlKeywords(self):

        """ Opens the Keyword document - currently assumes a static location in the working folder - and returns a list of the values within """

        # TBD - add checking of file existence / error handling
        with open('Trawl Keywords.txt') as f:
            searchTerms = f.readlines()
        searchTerms = [x.strip() for x in searchTerms]
        self.searchTerms = searchTerms

    def dropDuplicates(self):

        """ Checks if a project is already in the unified dataframe"""
        self.openDF()
        self.unifiedDF.drop_duplicates(subset='projName',keep='first', inplace=True)
        self.unifiedDF['projName'].replace('', np.nan, inplace=True)
        self.unifiedDF.dropna(subset=['projName'], inplace=True)
        self.closeDF_UNIFIED()

class GTR_Mapping(mappingUnified):



    def __init__(self):
        self.columns = ["Project ID", "Project Title", "Abstract","Lead Org ID","Lead Org Name", "Department Name", "Participant Org ID", "Participant Org Name","Project Partner ID","Project Partner Name", "Principle Investigator", "Grant Category","Funding Value","Funding Start Date", "Funding End Date", "Searched Term"]
        self.GTR_DF_RAW = None
        self.GTR_DF_REF = None

        self.GTR_DF_RAW_PATH = "Pickles/GTR_raw.pickle"
        self.GTR_DF_REF_PATH = "Pickles/GTR_refined.pickle"
        self.getTrawlKeywords()
        super(GTR_Mapping, self).__init__()

    def buildDFRaw(self):
        tempDF = pd.DataFrame(columns= self.columns, dtype='str')
        self.GTR_DF_RAW = tempDF
        self.closeGTR_DF_RAW(tempDF)

    def buildDFRef(self):
        tempDF = pd.DataFrame(columns= self.columns, dtype='str')
        self.GTR_DF_REF = tempDF
        self.closeGTR_DF_REF(tempDF)

    def checkDF_Raw_PreExists(self):

        """ Autonomous checking whether the GTR Raw DF exists and loads it, if not creates it
            For now it's assumed that you don't want the ability to over-write / re-create the dataframe.
            This is probably short sighted (Surprise, it was!)
        """


        if os.path.isfile(self.GTR_DF_RAW_PATH):
            self.GTR_DF_RAW = pd.read_pickle(self.GTR_DF_RAW_PATH)
        else:
            self.buildDFRaw()

    def closeGTR_DF_RAW(self, df):
        df.to_pickle(self.GTR_DF_RAW_PATH)
        print('Raw Dataframe successfully pickled!')

    def checkDF_REF_PreExists(self):

        """ Autonomous checking whether the GTR Refined DF exists and loads it, if not creates it
            For now it's assumed that you don't want the ability to over-write / re-create the dataframe.
            This is probably short sighted.
        """


        if os.path.isfile(self.GTR_DF_REF_PATH):
            self.GTR_DF_REF = pd.read_pickle(self.GTR_DF_REF_PATH)
        else:
            self.buildDFRef()

    def closeGTR_DF_REF(self, df):
        df.to_pickle(self.GTR_DF_REF_PATH)
        print('Refined Dataframe successfully pickled!')

    def goSearch(self):

        """ This is the head function for requesting and storing data from the GTR gateway.
            Data is stored in its 'raw' form - the way GTR stores its data means that full details of projects are often spread around multiple responses.
            Duplicates must be determined only by the Project ID, any attempts to drop duplicates on other values will end in lost data
        """

        # make lambda functgions for pretty-ness?
        def noSuchData():
            print ("No Data found for requested resource, skipping")

        def noSuchLink(linkType):
            print ("Program does not currently import link type: " + linkType + " - skipping")

        ### Obnoxious case declaring because if/elseif statements are ugly ###

        """ The following functions (labeled 'cases' just to confuse you) are methods for returning specific elements of data from the URL response
         The response should be in .json format. This means we need to intuit the exact positioning of data based on the number of projects returned and the number of links in the project
         The naming convention for following functions is 'case' + 'dataPoint being returned'
        """

        def caseLeadOrg(linkNum, indNum):
            url = queryData['project'][indNum]['links']['link'][linkNum]['href']
            leadOrg = ea.explicitPostRequest(url)
            leadOrgName = leadOrg['name']
            leadOrgID = leadOrg['id']
            return leadOrgID, leadOrgName

        def caseFund(linkNum, indNum):
            url = queryData['project'][indNum]['links']['link'][linkNum]['href']
            fundFUND = ea.explicitPostRequest(url)
            fundValue = fundFUND['valuePounds']['amount']
            timeStart = fundFUND['start'] / 1000 # goddamn time stuff won't work
            timeStart2 = datetime.datetime.fromtimestamp(timeStart).strftime('%Y-%m-%d')
            try:
                timeEnd = fundFUND['end'] / 1000
                timeEnd2 = datetime.datetime.fromtimestamp(timeEnd).strftime('%Y-%m-%d')
            except KeyError:
                noSuchData()
                timeEnd2 = None
            return fundValue, timeStart2, timeEnd2

        def casePP(linkNum, indNum):
            url = queryData['project'][indNum]['links']['link'][linkNum]['href']
            PP = ea.explicitPostRequest(url)
            PPName = PP['name']
            PPID = PP['id'] # not gonna work
            return PPID, PPName

        def caseP_ORG(linkNum, indNum):
            url = queryData['project'][indNum]['links']['link'][linkNum]['href']
            P_Org = ea.explicitPostRequest(url)
            P_OrgName = P_Org['name']
            P_OrgID = P_Org['id']  #betcha this wont work either
            return P_OrgID, P_OrgName

        def casePI_PER(linkNum, indNum):
            url = queryData['project'][indNum]['links']['link'][linkNum]['href']
            PI_PER = ea.explicitPostRequest(url)
            PI_PER_First = PI_PER['firstName']
            PI_PER_Last = PI_PER['surname']
            PI_PER = PI_PER_First + " " + PI_PER_Last
            return PI_PER

        newCount = 0

        self.checkDF_Raw_PreExists()
        # this is a workaround to allow the duplicate checking to function - you can't use column names with pandas iloc
        self.GTR_DF_RAW.columns = range(self.GTR_DF_RAW.shape[1])

        self.response = ea.getInput()

        # probably need to put some input sanitization

        """ This is the main working loop of the function.
            In text terms it:
                submits a search request using a single search term
                loops through each project in the response
                loops through each 'link' in the project'
            If a project's ID is already in the dataframe the project is skipped.
            The link type is found (using JSON  / Python Dictionary references) and the function for that type called.
            Data for each link type is stored in the appropriate variable.
            Once all links are exhausted a pandas series is constructed and appended to a dataframe.
        """

        for terms in self.searchTerms:

            API = ea.GTR_API(terms, self.response)
            API.inputHandler()
            API.URLConstructor()
            queryData = API.PostRequest()

            #queryURL = ea.URLConstructor(terms, response)  #sends the WGET request
            # = ea.CallAPI(queryURL)            # parses the data into JSON format

            numProjects = len(queryData['project'])
            print(str(numProjects) + " projects returned from GTR")
            for ind in range(numProjects):

                ProjID = None
                ProjTitle = None
                Abs = None
                leadOrgID = None
                leadOrgName = None
                DepName = None
                POrgID = []
                POrgName = []
                PPID = []
                PPName = []
                PI_PER = None
                grantCat = None
                fundValue = None
                fundStart = None
                fundEnd = None
                searchedTerm = terms
                # gather info not found in links
                ProjID = queryData['project'][ind]['id']
                ProjTitle = str(queryData['project'][ind]['title'])

                if(
                (self.classiDFExists == True
                and ProjTitle not in self.classifiedDF['projName'].values
                and ProjID not in self.GTR_DF_RAW.iloc[:,[0]].values)
                or self.classiDFExists == False
                and ProjID not in self.GTR_DF_RAW.iloc[:,[0]].values):

                    ProjTitle = str(queryData['project'][ind]['title'])
                    Abs = queryData['project'][ind]['abstractText'] #updates abstractText
                    try:
                        DepName = queryData['project'][ind]['leadOrganisationDepartment'] #updates department (if recorded)
                    except KeyError:
                        noSuchData()
                        DepName = None

                    grantCat = queryData['project'][ind]['grantCategory']

                    ### identify number of links ###
                    numLinks = len(queryData['project'][ind]['links']['link'])
                    ### Grab data from links ###

                    for link in range(numLinks):
                        linkType = queryData['project'][ind]['links']['link'][link]['rel']

                        if linkType == 'LEAD_ORG':     # Lead Org info
                            leadOrgTuple = caseLeadOrg(link,ind)
                            leadOrgID = leadOrgTuple[0]
                            leadOrgName = leadOrgTuple[1]

                        elif linkType == 'PARTICIPANT_ORG': # particiipant org info
                            partOrgTuple = caseP_ORG(link,ind)
                            # construct participant org IDs string
                            POrgID.append(partOrgTuple[0])
                            # construct participant org title strings

                            POrgName.append(partOrgTuple[1])

                        elif linkType == 'PP_ORG': # project partner inf
                            PPTuple = casePP(link,ind)
                            # construct project partner org IDs string
                            PPID.append(PPTuple[0])
                            # construct project partner org title strings
                            PPName.append(PPTuple[1])

                        elif linkType == 'FUND': # Fund info

                            fundTuple = caseFund(link,ind)
                            fundValue = fundTuple[0]
                            fundStart = fundTuple[1]
                            fundEnd = fundTuple[2]

                        elif linkType == 'PI_PER':
                            PI_PER = casePI_PER(link,ind)

                    series = pd.Series([ProjID, str(ProjTitle), Abs, leadOrgID, leadOrgName, DepName, POrgID, POrgName, PPID, PPName, PI_PER,grantCat, fundValue, fundStart, fundEnd, searchedTerm])

                    self.GTR_DF_RAW = self.GTR_DF_RAW.append(series, ignore_index=True)
                    newCount = newCount + 1
                else:
                    print('Duplicate entry found... skipping')

        print(str(newCount) + " new projects were added.")
        self.GTR_DF_RAW.columns = self.columns
        self.closeGTR_DF_RAW(self.GTR_DF_RAW)

    def datarefine(self):

        """ GTR stores the same project multiple times, depending on who is claiming to be the lead / who is receiving funding.
            This means that the data needs to be intelligently joined, avoiding duplicate values and resulting in a single row descring all facets of a project.

            We do this by using pandas groupby function to cluster projects which share the same title.
            We then identify a unique set of values from all of the projects, convert to a list and store in a dataframe series.
            The series are then appended back onto the main dataframe (so that we have the 'only once' projects and the 'multiple value' projects' in the same instance)
        """

        self.checkDF_Raw_PreExists()
        self.checkDF_REF_PreExists()

        self.GTR_DF_RAW.set_index('Project ID', inplace = True)
        df = self.GTR_DF_RAW[~self.GTR_DF_RAW.index.duplicated(keep='first')]

        groupedDF = df.groupby('Project Title').filter(lambda x: len(x) > 1)

        df.drop_duplicates(subset='Project Title', keep=False, inplace=True)

        grouped = groupedDF.groupby('Project Title')

        df.reset_index(inplace=True)

        for name, group in grouped: # for each group
            gg = grouped.get_group(name).reset_index()

            tempDF = pd.DataFrame(columns=self.columns)

            for col in gg: # for each column in the group

                lilDict = {}

                for n in range(len(gg)): # for each row in each column in each group

                    lilDict[n] = gg.loc[n, col]

                valueList = []

                if col == "Funding Value" or col == "Funding Start Date" or col == "Funding End Date" or col== "Research Grant":
                # some columns may have "duplicate" info that is actually unique in the sense that it needs to stand separate, even if the same value
                    for vals in lilDict:
                        valueList.append(lilDict[vals])

                    if valueList:
                        tempDF.loc[0,col] = valueList

                elif col != "Project Title" or col !="Abstract" or  col != "Searched Term":
                # the groups typically share the same partners but these are ingested in different orders so
                    masterList = []

                    for vals in lilDict:

                        if lilDict[vals] == None:
                            break
                        elif type((lilDict[vals])) == list:
                            listy = lilDict[vals]
                            #print(len(listy))
                            if (len(listy)) == 0:
                                break
                            else:
                                for y in range(len(listy)):
                                    masterList.append(listy[y])
                        else:
                            masterList.append(lilDict[vals])


                    masterList = [x.strip(' ') for x in masterList]

                    masterTuple = tuple(masterList)

                    uniqueSet = set()

                    for i in masterTuple:
                        uniqueSet.add(i)
                    #print(uniqueSet)
                    uniqueSet = sorted(set(uniqueSet), key=lambda x: masterList.index(x))
                    #print(uniqueSet)
                    for vals in uniqueSet:
                        valueList.append(vals)

                    if valueList:
                        tempDF.loc[0,col] = valueList
                else:
                    uniqueDictVals = set(lilDict.values())

                    for vals in uniqueDictVals:
                            if vals != None:
                                valueList.append(vals)
                    if valueList:
                        tempDF.loc[0,col] = valueList

                if col == "Participant Org Name":
                    pass

            df = df.append(tempDF, ignore_index = True)

        self.GTR_DF_REF = df
        self.closeGTR_DF_REF(self.GTR_DF_REF)

    def unifyGTR(self):

        """ Transports the GTR data into the unified Dataframe.
            Have to undertake a bit of data-wangling to make the data compliant - GTR distinguishes between inter-institution relationships while the unifiedDF only cares about connections generally
        """

        self.openDF()
        self.checkDF_REF_PreExists()

        subDF = self.GTR_DF_REF[['Project Title','Abstract','Lead Org Name','Participant Org Name','Project Partner Name', 'Funding Value','Searched Term']]
        subDF['projSource'] = 'GTR'
        subDF['projApplic'] = ''
        subDF = subDF.reset_index()
        subDF['collab'] = subDF[['Participant Org Name', 'Project Partner Name']].apply(lambda x: x[0] + x[1], axis = 1).values

        for col in subDF:
            subDF[col] = subDF[col].apply(lambda x: x if x else '')
        subDF.drop(columns=['Participant Org Name','Project Partner Name'], inplace=True)
        subDF = subDF[['Project Title','Abstract','Lead Org Name','collab', 'Funding Value','Searched Term','projSource', 'projApplic']]

        subDF.columns = range(subDF.shape[1])
        self.unifiedDF.columns = range(self.unifiedDF.shape[1])
        self.unifiedDF = self.unifiedDF.append(subDF, ignore_index=True)

        self.unifiedDF.columns = self.Columns

        self.closeDF_UNIFIED()

class CORDIS_Mapping(mappingUnified):


    def __init__(self):
        super(CORDIS_Mapping, self).__init__()
        self.columns = ["Project ID", "Project Title", "Abstract","Lead Org ID","Lead Org Name", "Department Name", "Participant Org ID", "Participant Org Name","Project Partner ID","Project Partner Name", "Grant Category","Funding Value","Funding Start Date", "Funding End Date", "Searched Term"]
        self.CORDIS_DF = None
        self.csvDownloadURL = "http://cordis.europa.eu/data/cordis-h2020projects.csv"
        self.cordisURL = "https://data.europa.eu/euodp/data/dataset/cordisH2020projects/resource/010f269b-9ee3-45a0-afea-c43aa1ef61ac"
        self.csvPath = 'CSV/cordis-h2020projects.csv'
        self.csvMetaPath = 'CSV/CORDISmeta.json'

        self.getTrawlKeywords()

    def getCSV(self):

        """ Function for downloading the CORDIS dataset and creating a dataframe from it.
            To avoid wasted bandwidth the dataset should only be downloaded if a newer verison is available.

            CORDIS publish this information on their website - we use webscraping to get the date modified information and compare it to metadata created by our previous downloads'
            If no file exists or a newer version is available we use requests to download and store the CSV file.
        """

        import requests

        import json

        if os.path.isfile(self.csvPath):

            modDate = self.checkCSVDate()
            meta = json.load(open(self.csvMetaPath))

            if meta["modDate"] != modDate:
                print("Newer CSV version detected, downloading...")
                self.downloadCSV()
                print("CSV file saved...")
                self.makeMetaData()
                print("MetaData file saved...")
                self.createDF_CORDIS()

            else:
                print("Latest CSV file already on disk")
                self.makeMetaData()
        else:
            print("CSV file not found on disk, downloading...")
            self.downloadCSV()
            print("CSV file saved...")
            self.makeMetaData()
            print("MetaData file saved...")
            self.createDF_CORDIS()




    def downloadCSV(self):

        """ Uses Requests to post get requests from CORDIS, storing the response on disk as  """

        import requests

        self.checkFolder('CSV')
        r = requests.get(self.csvDownloadURL, stream=False)
        with open('CSV/cordis-h2020projects.csv', 'wb') as f:
            f.write(r.content)
        self.makeMetaData()

    def checkCSVDate(self):

        """ Uses lxml and requests to scrape the 'modified date' and compare it to our locally stored metadata which is created on first download. """
        from lxml import html
        import requests

        page = requests.get(self.cordisURL)
        tree = html.fromstring(page.content)

        modDate = tree.xpath('//*[@id="less-meta"]/dl[3]/dd/text()')
        modDate = str(modDate[0]).strip()

        return modDate

    def makeMetaData(self):

        """ Creates a JSON file for storing metaData about the CSV download process"""

        import json
        import datetime

        now = datetime.datetime.now()

        modDate = self.checkCSVDate()
        d = {
            'name':'cordisH2020projects',
            'modDate': modDate,
            'lastCheckDate': now.strftime("%Y-%m-%d")
        }
        with open(self.csvMetaPath, 'w') as outfile:
            json.dump(d, outfile)

    def createDF_CORDIS(self):

        """ Creates the DataFrame from stored CSV file and stores it as local variable """
        self.CORDIS_DF = pd.read_csv(self.csvPath, sep=';')
        self.closeDF_CORDIS()

    def closeDF_CORDIS(self):

        """ Pickles the CORDIS DataFrame """

        self.CORDIS_DF.to_pickle('Pickles/CORDIS_DF.pickle')
        print('CORDIS DataFrame pickled!')

    def loadDF_CORDIS(self):

        """ Loads the CORDIS DataFrame """

        self.CORDIS_DF = pd.read_pickle('Pickles/CORDIS_DF.pickle')

    def goSearch(self):

        """ Responsible for searching through the CORDIS dataset and returning results.
            Projects where the UK is a coordinatorCountry and participantCountries are conidered in scope. This requires two different passthroughs of main dataframe.
            Search terms from the list are checked against the 'objective' descriptor for each project with matches being stored in a search results dataframe.
            The unifier is automatically called, transporting the search results into the unified dataframe,.
        """



        # pandas is throwing up chained_assignment warnings without tracing which line actually triggers it, supressing for now...

        pd.options.mode.chained_assignment = None

        if os.path.isfile('Pickles/CORDIS_DF.pickle'):
            self.loadDF_CORDIS()
        else:
            self.createDF_CORDIS()

        ukScope = ["participantCountries", "coordinatorCountry"]
        dfSearchResult = pd.DataFrame()

        for scope in ukScope:
            self.loadDF_CORDIS()
            CORDIS_DF = self.CORDIS_DF.dropna(subset=[scope])
            ukDF = CORDIS_DF[CORDIS_DF[scope].str.contains("UK")]

            for n in range(len(self.searchTerms)):

                term = self.searchTerms[n].replace('"',"").strip()
                searchDF = ukDF[ukDF["objective"].str.contains(term, case=False)]
                try:
                    searchDF.loc[:,"searchedTerm"] = str(term)
                    dfSearchResult = dfSearchResult.append(searchDF,ignore_index=True)
                except:
                    KeyError

        dfSearchResult.drop_duplicates(subset="title",inplace=True, keep='first')
        self.unifyCORDIS(dfSearchResult)


    def unifyCORDIS(self, df):

        """ Transports the search results from CORDIS into the unified DF. """

        self.openDF()
        subDF = df[['title','objective','coordinator','participants','totalCost', 'searchedTerm']]
        subDF['participants'] = subDF['participants'].apply(lambda x: x.split(';'))
        subDF.loc[:,'projSource'] = 'CORDIS'
        subDF.loc[:,'projApplic'] = ''
        subDF = subDF[['title','objective','coordinator','participants','totalCost', 'searchedTerm','projSource', 'projApplic']]
        subDF.columns = range(subDF.shape[1])
        self.unifiedDF.columns = range(self.unifiedDF.shape[1])
        self.unifiedDF = self.unifiedDF.append(subDF, ignore_index=True)
        self.unifiedDF.columns = self.Columns
        self.closeDF_UNIFIED()
        self.dropDuplicates()
