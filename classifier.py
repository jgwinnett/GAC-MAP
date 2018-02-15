import dfClassConstructor as map
import pandas as pd
#### one off ####

class EPSRC_CLASSIFYING(map.EPSRC_Mapping):

    def __init__(self):

        super(EPSRC_CLASSIFYING, self).__init__()
        self.dfMainPath = "Pickles/classifiedUnified.pickle"
        self.excelExportPath = "Excel/classifiedProjects.xlsx"
        self.csvExportPath = "CSV/classifiedProjects.csv"
        self.EPSRC_DF_REF_PATH = "Classified/EPSRC_applicable_only.pickle"

    def tempOpen(self):

        df = pd.read_csv('Classified/EPSRC_applicable_only.csv', sep=",")
        df['Participant Org Name'] = df['Participant Org Name'].apply(lambda x: "" if type(x) == float else x)
        df['Project Partner Name'] = df['Project Partner Name'].apply(lambda x: "" if type(x) == float else x)
        df['Participant Org Name'] = df['Participant Org Name'].apply(lambda x: "" if '[]' in x else x)
        df['Project Partner Name'] = df['Project Partner Name'].apply(lambda x: "" if '[]' in x else x)

        df.to_pickle(self.EPSRC_DF_REF_PATH)

    def unifyEPSRC_fix(self):

        """ Transports the EPSRC data into the unified Dataframe.
            Have to undertake a bit of data-wangling to make the data compliant - EPSRC distinguishes between inter-institution relationships while the unifiedDF only cares about connections generally
        """

        self.openDF()
        self.checkDF_REF_PreExists()

        subDF = self.EPSRC_DF_REF[['Project Title','Abstract','Lead Org Name','Participant Org Name','Project Partner Name', 'Funding Value','Searched Term']]
        subDF['projSource'] = 'EPSRC'
        subDF = subDF.reset_index()
        subDF['collab'] = subDF[['Participant Org Name', 'Project Partner Name']].apply(lambda x: x[0] + x[1], axis = 1).values
        subDF['collab'] = subDF['collab'].apply(lambda x: x.strip('['))
        subDF['collab'] = subDF['collab'].apply(lambda x: x.strip(']'))
        subDF['collab'] = subDF['collab'].apply(lambda x: x.split(','))
        print(subDF['collab'])

        subDF.drop(columns=['Participant Org Name','Project Partner Name'], inplace=True)
        subDF = subDF[['Project Title','Abstract','Lead Org Name','collab', 'Funding Value','Searched Term','projSource']]

        subDF.columns = range(subDF.shape[1])
        self.unifiedDF.columns = range(self.unifiedDF.shape[1])
        self.unifiedDF = self.unifiedDF.append(subDF, ignore_index=True)

        self.unifiedDF.columns = self.Columns

        self.closeDF_UNIFIED()

class KOSTAS_CLASSIFYING(map.mappingUnified):

    def __init__(self):

        super(KOSTAS_CLASSIFYING, self).__init__()
        self.dfMainPath = "Pickles/classifiedUnified.pickle"
        self.excelExportPath = "Excel/classifiedProjects.xlsx"
        self.csvExportPath = "CSV/classifiedProjects.csv"
        self.Kostas_Path = "Classified/Kostas_applicable_only.pickle"

    def tempOpen(self):

        df = pd.read_excel('Classified/Academia_Mapping.xlsx', sheet_name = "Universities - projects", header = 0)
        df.to_pickle(self.Kostas_Path)


    def unifyKostas(self):

        # University Name Project Name	Partners	Funding	Summary/Key Points	Classification
        self.openDF()
        df = pd.read_pickle(self.Kostas_Path)

        df.Partners = df.Partners.apply(lambda x: str(x))
        df.Partners = df.Partners.apply(lambda x: "" if x == "nan" else x)

        subDF = df[["Project Name", "Summary/Key Points","University Name", "Partners", "Funding", "Classification"]]
        subDF['Partners'] = subDF['Partners'].apply(lambda x: x.split(','))
        subDF.loc[:,'projSource'] = 'KOSTAS'
        subDF = subDF[["Project Name", "Summary/Key Points","University Name", "Partners", "Funding", "Classification", 'projSource']]
        subDF.columns = range(subDF.shape[1])
        self.unifiedDF.columns = range(self.unifiedDF.shape[1])
        self.unifiedDF = self.unifiedDF.append(subDF, ignore_index=True)
        self.unifiedDF.columns = self.Columns
        self.closeDF_UNIFIED()
        self.dropDuplicates()




mappoo = EPSRC_CLASSIFYING()
mappoo.buildDF()
mappoo.tempOpen()
mappoo.unifyEPSRC_fix()
#
mappoo = KOSTAS_CLASSIFYING()
mappoo.tempOpen()
mappoo.unifyKostas()
mappoo.exportDF_excel()
