
## Query Constructor for use with GTR API ###

### Constructing Queries ###
#   q=searchterm - search term
#   p=pageresult - page of result set, starting at 1
#   s=size - size of page, between 10 and 100
#   f=fields - search specific fields (have to check each types config for a list of fields...)
#   sf = sort fields - sort by a certain fields
#   so = sort order - sort order = A for ascending, =D for descending

# Build the base URL (projects only for now)

class GTR_API():


    def __init__(self, query, userResponse):
        self.query = query
        self.userResponse = userResponse

        self.headerJSON = {'accept': 'application/vnd.rcuk.gtr.json-v6'}
        self.headerXML = {'accept': 'application/vnd.rcuk.gtr.xml-v6'}
        self.baseURL = "http://gtr.rcuk.ac.uk:80/gtr/api/projects?"
        self.URL = ""
        self.fields = ""
        self.multiField = []

        self.projectCases = {
        '1': lambda fields: self.caseRef(),
        '2': lambda fields: self.caseTitle(),
        '3': lambda fields: self.caseAbstract()
        }

    # Case Actions
    def caseRef (self):
        """ Inserts the appropriate query string when the user wishes to search against a project reference number """
        ProRef = "f=pro.gr"
        self.fields += ProRef


    def caseTitle(self):
        """ Inserts the appropriate query string when the user wishes to search against an Title """

        ProTitle = 'f=pro.t'
        self.fields += ProTitle

    def caseAbstract(self):
        """ Inserts the appropriate query string when the user wishes to search against an Abstract """
        ProAbstract = "f=pro.a"
        self.fields += ProAbstract


    # Exceptions
    def incorrectFieldChoice():

        """ Called  when the lazy sanity check in inputHandler detects an erroneous user input """
        print ('You entered an invalid field choice, halting operation')
        quit()

    def inputHandler(self):

        """ Handles the users field choices by appending correct string values and connectors to the class' field variable
        """
        self.baseURL += 'q='

        if len(self.userResponse) == 1:  # if length is one assume it's a number choice and proceed
            try:
                self.projectCases[self.userResponse](self.fields)
                self.fields += "&"
            except KeyError:        # low effort catching of incorrect field entries
                self.incorrectFieldChoice()

        else:
            self.multiField = self.userResponse.split(",")   # split responses - will error if user ends with a comma // TO-FIX

            try:
                for choices in range(len(self.multiField)):    # loop through multiple responses and append
                    self.projectCases[self.multiField[choices]](self.fields)
                    self.fields += "&"
            except KeyError:            # lazy catching again
                    self.incorrectFieldChoice()

        self.baseURL += '"' + self.query + '"' + '&'

    def URLConstructor(self):

        """ Combines 'base' URL with field selection. """
        self.URL = self.baseURL + self.fields + 's=100'
        print(self.URL)

    def PostRequest(self):

        """Posts a HTML GET request using the constructed query URL and stored JSON headers."""
        import requests
        import json
        r = requests.get(self.URL, headers=self.headerJSON)
        j = r.json()
        return j

def getInput():



    """ A generic input request from the user - the user is prompted to select from 3 possible fields to search against. Supports selection of multiple fields in an easily breakable way (comma seperated input)
    """

    # This is excluded from the main class as a lazy way to avoid the user being repeatedly prompted when a list of terms is passed
    print ('')
    print ('The following fields may be searched against:')
    print ('1) Project Reference')
    print ('2) Project Title')
    print ('3) Project Abstract')
    print ('')

    print ('Please type the number(s) that you wish to search against, separated by commas')
    response = input()
    return response

def explicitPostRequest(URL):

    """ Uses the `requests module <http://docs.python-requests.org/en/master/>`_ to post a request to the GTR API.
    This must be passed a complete GTR query URL and uses a hardcoded JSON header
    """

    import requests
    import json

    headerJSON = headerJSON = {'accept': 'application/vnd.rcuk.gtr.json-v6'}
    r = requests.get(URL, headers=headerJSON)
    j = r.json()
    return j



####### How to Access links ##########
# print len(y['project'][0]['links']['link'])
# pp.pprint(y['project'][0]['links']['link'][5])



# Constructing Queries
#   q=searchterm - search term
#   p=pageresult - page of result set, starting at 1
#   s=size - size of page, between 10 and 100
#   f=fields - search specific fields (have to check each types config for a list of fields...)
#   sf = sort fields - sort by a certain fields
#   so = sort order - sort order = A for ascending, =D for descending
