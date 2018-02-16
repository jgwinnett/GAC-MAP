GAC-MAP Overview
####################

Project Description
=====================

GAC-MAP (GtR and CORDIS Mapping) is a project created to simplify the process of finding details about UK based academic projects in the <target> field.

This project processes large batches of keywords against the GtR and CORDIS datasets and returns projects where these keywords are present.

As GtR & CORDIS store their data differently we also 'unify' the data so that we finish with a set of common data-points.

Intended use case
=======================
The intended use of this tool is to enable a quick and easy way to 'map' UK activity in <target> research field. This provides immediately usable results and also preps the data for further analytics and visualization.

It can also just be used as an easier way to access data from the
:doc:`GTR_API <GTR_API>`
or avoid having to search through CORDIS'
`large .CSV file <https://data.europa.eu/euodp/data/dataset/cordisH2020projects/resource/010f269b-9ee3-45a0-afea-c43aa1ef61ac>`_
manually.


What Data is currently stored?
================================

The following is a breakdown of what data is stored by default.

Each data type (Unified, GtR, CORDIS) is stored in its own file but only Unified is used in further processing.

Unified Data
----------------------------

Unified data refers to the commonly shared datapoints between the GtR and CORDIS sources.

+-------------+------------------------------------------------------------+
| Data Name   |     Data Description                                       |
+=============+============================================================+
| projName    |     The Name of the project                                |
+-------------+------------------------------------------------------------+
| projDesc    |     The Project's Description of the work being done       |
+-------------+------------------------------------------------------------+
| projLead    |     The Lead Organisation of the project                   |
+-------------+------------------------------------------------------------+
| projCollab  |     The Collaborators working on the project               |
+-------------+------------------------------------------------------------+
| projFunding |     The funding amount received for the project            |
+-------------+------------------------------------------------------------+
| projGrouping|     The Search Term(s) that returned the given project     |
+-------------+------------------------------------------------------------+
| projSource  |     Lists the data source point, GtR or CORDIS             |
+-------------+------------------------------------------------------------+

GtR Data
----------------------
The following data is stored from GtR queries:

+----------------------+------------------------------------------------------------+
| Data Name            |     Data Description                                       |
+======================+============================================================+
| Project ID           |     The project's GtR ID                                   |
+----------------------+------------------------------------------------------------+
| Project Title        |     The project's Title                                    |
+----------------------+------------------------------------------------------------+
| Abstract             |     The Description of the project                         |
+----------------------+------------------------------------------------------------+
| Lead Org ID          |     The GtR ID of the Lead organisation                    |
+----------------------+------------------------------------------------------------+
| Lead Org Name        |     The Name of the Lead organisation                      |
+----------------------+------------------------------------------------------------+
| Department Name      |     The Department Name (subset of the Lead Organisation)  |
+----------------------+------------------------------------------------------------+
| Participant Org ID   |     The GtR ID of a Participant Organisation               |
+----------------------+------------------------------------------------------------+
| Participant Org Name |     The Name of a Participant Organisation.                |
+----------------------+------------------------------------------------------------+
| Project Partner ID   |     The GtR ID of a Project Partner                        |
+----------------------+------------------------------------------------------------+
| Project Partner Name |     The Name of a Project Partner                          |
+----------------------+------------------------------------------------------------+
| Grant Category       |     The Category of Grant that money was awarded under     |
+----------------------+------------------------------------------------------------+
| Funding Value        |     The amount of Funding awarded to the project           |
+----------------------+------------------------------------------------------------+
| Funding Start Date   |     The Date from which funding began                      |
+----------------------+------------------------------------------------------------+
| Funding End Date     |     The Date when funding ends.                            |
+----------------------+------------------------------------------------------------+
| Searched Term        |     The search term(s) that returned the given project.    |
+----------------------+------------------------------------------------------------+

CORDIS Data
-------------------
CORDIS data is extracted from the full .CSV so all the data is available. The following, most useful, datapoints are retained.


+----------------------+------------------------------------------------------------+
| Data Name            |     Data Description                                       |
+======================+============================================================+
| id                   |     The CORDIS ID of the project.                          |
+----------------------+------------------------------------------------------------+
| title                |     The project's Title.                                   |
+----------------------+------------------------------------------------------------+
| startDate            |     The start Date of the H2020 funding.                   |
+----------------------+------------------------------------------------------------+
| endDate              |     The end Date of the H2020 funding.                     |
+----------------------+------------------------------------------------------------+
| projectUrl           |     The URL (web-access) of the project.                   |
+----------------------+------------------------------------------------------------+
| objective            |     The Description of the project's goals.                |
+----------------------+------------------------------------------------------------+
| totalCost            |     The Total Value of spending on the project.            |
+----------------------+------------------------------------------------------------+
| coordinator          |     The Name of the Lead Organisation.                     |
+----------------------+------------------------------------------------------------+
| coordinatorCountry   |     The Country of the Lead Organisation.                  |
+----------------------+------------------------------------------------------------+
| participants         |     The Name(s) of Participant Organisations.              |
+----------------------+------------------------------------------------------------+
| participantCountries |     The Countries where Participant Organisations reside.  |
+----------------------+------------------------------------------------------------+
| subjects             |     The search term(s) that returned the given project.    |
+----------------------+------------------------------------------------------------+

Licensing
==========================

This module is released under XYZ license.
If you're using this outside of personal use please credit as below:
Blah blah, something.
