GTR API Access
########################

Purpose
========

This module is used to query the Gateway To Research (GTR) API. Queries are done by posting GET requests with specifically crafted URLs.
As such there are two main elements: constructing the URL based on user input and posting/processing the request.

Dependencies
=============

From other modules:
----------------------
	- requests
	- json

Module Class, Methods and Functions
======================================

API Access Class
------------------

This class, when passed a search term, will construct a 'search URL', send off a HTTP Get request (with appropriate headers), and return the response.

.. autoclass:: GTR_API_access.GTR_API
	:members:

Stand-Alone Functions
----------------------------

.. autofunction:: GTR_API_access.getInput

.. autofunction:: GTR_API_access.explicitPostRequest

Notes on the GTR API
========================

This is an explanatory section which breaks down the syntax needed when constructing the necessary URLs for querying the GTR API.

URL Construction
---------------------

The base URL, which must always be the starting point is

.. code-block:: html

	http://gtr.rcuk.ac.uk/gtr/api/

You then select the resource type you're enquiring after from the following list:

* organisation
* person
* project
* outcome
* fund

To submit queries you will need to pluralise the resource (add an "s") and end with a question mark (?) - e.g.

.. code-block:: html

	http://gtr.rcuk.ac.uk/gtr/api/projects?

Then, based on your desired search results, append the relevant text to the URL.
All query parameters are separated by an ampersand (&). The order of terms in the URL does not appear to matter.

+---------------+------+----------------------------------------+--------------------------------------------------------+
| Query         |  URL |  Valid Values                          | Explanation                                            |
+===============+======+========================================+========================================================+
| Search Term   |  q=  |  Any String                            | The Search Term you wish to find results related to    |
+---------------+------+----------------------------------------+--------------------------------------------------------+
| Page Result   |  p=  |  Integer                               | The page number of the search results returned         |
+---------------+------+----------------------------------------+--------------------------------------------------------+
| Size          |  s=  |  Integer between 10 and 100            | How many results to display, per page                  |
+---------------+------+----------------------------------------+--------------------------------------------------------+
| Fields        |  f=  |  See 'Fields' below                    | What field(s) the Search Term should be queried against|
+---------------+------+----------------------------------------+--------------------------------------------------------+
| Sort Fields   |  sf= |  See 'Fields' below                    | What field(s) the results should be sorted by.         |
+---------------+------+----------------------------------------+--------------------------------------------------------+
| Sort Order    |  so= |  'A' for ascending, 'D' for descending | Whether results should be sorted in ascending or       |
|               |      |                                        | descending  order                                      |
+---------------+------+----------------------------------------+--------------------------------------------------------+

e.g. to state that the number of results per page should be 100 and you want the 2nd page you would type

.. code-block:: html

	http://gtr.rcuk.ac.uk/gtr/api/projects?s=100&p=2

Fields are special in that you will have to dig into the GTR configs to find out what fields may be searched against.
To do this navigate in your browser of choice to http://gtr.rcuk.ac.uk/gtr/api/configs/<resource>  (be sure to add the 's') e.g.

.. code-block:: html

	http://gtr.rcuk.ac.uk/gtr/api/configs/projects

Tells you that the following fields are searchable:

* pro.gr - Project Reference
* pro.t - Project Title
* pro.a - Project Abstract
* pro.orcidID - Project's ORCID ID

e.g. to search the 'Project Title' field you would use the following example:

.. code-block:: html

	http://gtr.rcuk.ac.uk/gtr/api/projects?f=pro.t

Putting it all together - example, you wanted to find:

* Projects
	* where 'fish' (q=fish)
	* is in the 'Project Title' (f=pro.t)
	* or the 'Project Abstract' (f=pro.a)
	* on the second page (p=2)
		* where a page is size 10 (s=10)

You would construct the following URL:

.. code-block:: html

	http://gtr.rcuk.ac.uk/gtr/api/projects?q=fish&f=pro.t&f=pro.a&p=2&s=10

This URL can be used in a browser (results are displayed in XML) or sent via a py:requests HTTP-GET

Notes on sending HTTP GET requests
-------------------------------------

GTR requires that GET requests are accompanied with headers specifying the format the data is returned in.
This is sent as a dictionary object.

.. code-block:: json

 	key:'accept'
	value: application/vnd.rcuk.gtr.<RequestedSchema>

These are already hard-coded into the request class as :

.. code-block:: python

	GTR_API.headerJSON = {'accept': 'application/vnd.rcuk.gtr.json-v6'}

and

.. code-block:: python

	GTR_API.headerXML = {'accept': 'application/vnd.rcuk.gtr.xml-v6'}

This module by default requests the data in JSON format.

Accessing the JSON data via Python
-----------------------------------

The query data is returned as a JSON object. JSON objects store their data in key pairs, where another JSON object can be nested as the pair value.

e.g. for a JSON object named Y

- head
	- thing 0
		- property 1
			- value
		- property 2
			- value
	- thing 1
		- property 1
			- value
		- property 3
			- sub-property 1
					- value
			- sub-property 2
					- value

Where there are multiples of the same key (e.g. 'thing' in the above example) the target is referenced by its numerical position (starting from 0).

In order to return the value of property 2 for thing 0 you must provide python with the full key:pair path.

.. code-block:: Python

	value = Y['thing'][0]['property 2']

Or for the value of sub-property 1 of thing 1's property 3:

.. code-block:: Python

	value = Y['thing'][1]['property 3']['sub-property 2']

GTR-API Source Documentation
------------------------------

GTR's documentation is a bit threadbare (so far as I could find). The above was deduced from the `GTR technical summary <http://gtr.rcuk.ac.uk/resources/GtR-2-API-v1.7.1.pdf>`_.
All info copyright GTR.


Disclaimers
============
Queries are currently limited to Projects (there's no programmatic reason, just have had no need to use other elements). This code can easily be expanded to allow wider queries.
