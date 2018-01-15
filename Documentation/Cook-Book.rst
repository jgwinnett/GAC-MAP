GAC-MAP Recipes
########################

Purpose
========
For ease of use I've compiled some 'recipes' that can be used out of the box to start grabbing data from GTR and CORDIS.

In order for these to work you will need to have created a 'Trawl Keywords.txt' file and stored it in the same directory as the .py files.

These are stored in Mapping_Recipes.py and reproduced here for clarities sake.

Dependencies
=============

From this module:
-------------------
- EPSRC_API_access
- dfClassConstructor

External Dependencies:
------------------------
- requests
- json
- pandas
- numpy
- datetime

Recipes
=========

FirstRun
------------
FirstRun should be used the first time you are instantiating a project's search. It will safely create fresh DataFrames, download the latest CSV files and unify the data once searching is done.

.. code-block:: python

  def firstRun():

      import dfClassConstructor as map

      mapBot = map.CORDIS_Mapping()

      mapBot.buildDFSafe()
      mapBot.getCSV()
      mapBot.goSearch()

      mapBot = map.EPSRC_Mapping()

      mapBot.goSearch()
      mapBot.datarefine()
      mapBot.unifyEPSRC()

updateMapping
-----------------

updateMapping should be used anytime you are performing further searches on a pre-existing project (i.e. you have run firstRun before and since modified the Trawl Keywords or are checking for updates on the same set of words).

It will check whether the CORDIS CSV has been updated and if so download the latest file.
Instead of creating fresh dataframes updateMapping will look for the pre-existing pickled ones. If these are not found it will crash (TBF).
It will then run the search as before, skipping any duplicate values and storing the results.

.. code-block:: python

  def updateMapping():

      import dfClassConstructor as map

      mapBot = map.CORDIS_Mapping()

      mapBot.getCSV()
      mapBot.goSearch()

      mapBot = map.EPSRC_Mapping()

      mapBot.goSearch()
      mapBot.datarefine()
      mapBot.unifyEPSRC()

exportUnified
----------------

This is a lazy recipe for when you just want to quickly export the unified DataFrame. Currently it exports into both CSV and .xlsx.

.. code-block:: python

  def exportUnified():

      import dfClassConstructor as map

      mapBot = map.mappingUnified()

      mapBot.exportDF_CSV()
      mapBot.exportDF_excel()
