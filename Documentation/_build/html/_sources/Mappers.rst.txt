CORDIS & EPSRC Mapping
########################

Purpose
========

This module allows users to identify projects that are relevant to them from two sources - EPSRC's 'Gateway To Research' and CORDIS' Horizon 2020 Projects.
The user must idenfy applicable keywords and storethem in 'Trawl Keywords.txt'.
Once done they may run one of the basic recipes in Mapping_Recipes to receive a unified list of applicable projects from both sources.
These are exportable to both .CSV and .xlsx. If new keywords are desired they need only to be added and the list will be updated.

Dependencies
=============

From this project:
--------------------
	- EPSRC_API_access

From other modules:
----------------------
	- pandas
	- numpy
	- datetime
	- openpxl

Module Classes and Methods
===========================

Mapping Unifier
--------------------

This class is responsible for building the baseline dataframe of unified data. It is inherited by CORDIS_Mapping and EPSRC_Mapping


.. autoclass:: dfClassConstructor.mappingUnified
	:members:

EPSRC Mapping
-----------------
This class is responsible for the ingesting, refinement and transportation of information from the EPSRC gateway.

The data is pulled by constructing request URLs (see :doc:`API Access <EPSRC_API>` for more details) and sending off WGET requests"

The responses are stored in a temporary dataframe which is preserved for future pass throughs.

This 'raw' data is then refined / transformed to condense a project's information into a single row and kill off duplicates.

Refined data is then preserved and relevant parts pushed into the the unified dataframe.

.. autoclass:: dfClassConstructor.EPSRC_Mapping
		:members:

CORDIS Mapping
-----------------

This class is responsible for the ingestion, processing and storage of data from the CORDIS database.

Unfortunately CORDIS does not have an API, they release their data monthly via downloadable CSV files.

Once downloaded these CSV files can be imported as dataframes and quickly proccessed using pandas groupby function.

Countries with UK leading AND/OR participating are considered in scope.

.. autoclass:: dfClassConstructor.CORDIS_Mapping
		:members:
