Adding a geospatial map of dataset search result to Dataverse
=============================================================
*A 'landscape' analysis*
========================

Version 0.1 - Concept/Draft, November 2024. 


Introduction
------------

This document will give a brief description of the Dataverse software architecture and how DANS can extend its functionality to provide geographical capabilities, like showing locations on a map and possibly search using this location information. 
Effort is being done to prevent to much technical detail, but it is inevitable that some technical knowledge is needed to be able to understand the software terms and concepts mentioned here. 


Existing geospatial functionality in Dataverse
----------------------------------------------
- Preview of files (geojson for example) in a dataset
- Search API and indexing of the custom `Geospatial Metadata` block in Solr is 'hardcoded' and assumes WGS84. Note that it is not displayed on a map in Dataverse. 


The Dataverse architecture in a nutshell
----------------------------------------

### The current architecture

Dataverse as a single web application (sometimes referred to as a monolith), although internally it is 'modular'. 
Note that it uses other services, like Postgres and Solr and DANS has 'micro' services connected to it. 

- Using Java Server Pages (JSP and in case of Dataverse it is Primefaces) we have the page (GUI) in XHTML templates and Java classes (EJB) at the backend, all compiled into a singe web application . 
- It does have an extensive API on that backend, which is being extend even further because of the movement to the new SPA architecture (see next section). 
- The metadata (containing the location information like names and coordinates) is stored in a Postgres database. For searching the Solr indexing service is being used. The indexing via Solr is configured with a schema XML file. 

### The new architecture

Dataverse frontend as a Single Page Application (SPA). The main change is the separation of frontend (GUI) and backend. The idea is that it would make it easier for us (and others) to create our own frontend on top of the 'standard' backend. 

- backend will be kept, but the API will extended to support the new frontend
- frontend will be done with the React framework

It is uncertain when it will be in a state that DANS is able to have it replace the 'old' frontend. 


Different ways to extend the functionality
------------------------------------------

### The current architecture

- Change the code (also GUI) via an Issue and accompanying Pull request on IQSS's Github repository. 

- Custom homepage, header and footers and CSS can be configured
  HTML (optional with JavaScript) fragments can be specified and the Dataverse application will 'inject' those into its web pages. 
  We have used this, also to 'inject' some other code like the Freshdesk 'widget' shown at the bottom of the DataverseNL site. 
  Analytic code (SJ) can be 'injected' as well, we use this with the Matomo statistics service. 

- External tools and previewers
  For files, not for search results!

- Controlled vocabularies (Cvocs), configure external service to retrieve metadata terms (via Skosmos for example) that is used in autocomplete and for using URI's in the metadata and still show the readable 'labels' in the GUI. 
'. This is now also done with JavaScript. 

- External service can be hooked to specific archival 'events' like publication of a dataset. 
  These services are passed information about the dataset in question and can change the dataset metadata. 

- Plugins
  Plugins could be developed in their own software project and do not have to be 'compiled ' into the application code. 
  Extending the backend, but could in principal also be used to extend the frontend if it is JSP. 
  In several location in the code there are SPI's (interface specifications for a plugin), but only for the export metadata functionality Dataverse is 'scanning' and loading jar files at run-time startup. 

### The new architecture

The new architecture has the front end as a Single Page Application (SPA). It keeps the backend, which is now allowing the configuration of the extendabilities mentioned before. It therefore seems likely that those features will be supported, but it is not certain!


Different ways we could add the geospatial functionality
--------------------------------------------------------

Some non functional requirement will play a role in choosing one of the options. 
- we have a limited timeframe to realize at least the minimal requirements. Not sure it is clear what they are, but the absolute bottemline would be to show these dataset locations on an interactive map similar to what we had in EASY. 
- we want  this to be maintainable and thus to make it a community effort as much as possible avoiding that DANS has to maintain its 'forked' Github code repository for a long time. The functionality should be relatively simple to adapt or configure to make it useful for others, that is; with other coordinate systems and or from other custom metadatablocks. For DANS this would be for instance supporting the DCCD metadata in DataverseNL. For the community that should at least be that custom `Geospatial Metadata` block supplied by IQSS. 

The change of the Dataverse architecture and our wish to change frontend code is a complicating coincidence, so we should try minimize the differences of what we will add and what will be needed in that new SPA. 

### Change of frontend

- Using JavaScript 'injection'; via the custom footer for example. 
  This cannot be done with React code, we could use JavaScript with the jQuery library already in Dataverse frontend. This is a quick way of testing some basics without changing any of the Dataverse code.

- Using a mechanism similar to the previewer/external tools. However some code changes in Dataverse are needed because now tools/previewers are on files and not on search results. The 'map' should be optional and in an 'iframe' in the GUI where we can configure that content from another source (could be on same server) will be shown. 
 This could be React code, so we have better reusable when migrating to the new SPA system. 

 - Change the JSP code 
   Use a Primefaces (leaflet) map tool and 'connect ' this to the search results handing in the Java code. Some Dataverse configuration is needed, because we want it to be optional and we need to specify how the coordinates must be extracted from the metadata. 
It looks like this is difficult to do without more changes on the backend code. 


The options above are limited to display locations. The JavaScript  code contains the logic that extract the coordinates from the metadata and convert them into coordinates that can easily be displayed on the map (WGS84). 
The Dataverse application (backend) is not aware of the geographical nature of the metadata fields. If we want to be able to do Geo searches, like limiting results to a bounding box, or sorting with the distance t a location for example, we would need to index them as coordinate.
 
Solr can do this. ? Somewhere it is done for that custom block DANS does not use... ?
Converting all coordinates to one standard (WGS84) which allows for comparing. The original coordinates must be stored, but for indexing these 'standard' coordinates should be indexed. 

This will also allow us to search for dataset that have coordinates in the first place, instead of filtering all search results on the frontend. 
At DANS this might not be a big problem, in our Archaeology archive almost all datasets have coordinates. But for others (and we want to have the community with us). datasets with coordinates might be sparse. 

### Options for change on backend

 - Add a new 'coordinate'  field types for latitude longitude and the 'coordinate system' (EPSG code). 
   Specification is done via the TSV files. 
   Dataverse will use a library to convert these coordinates to WGS84 and index them in Solr. 
   The Dataverse search interface must be adapted somehow allow to specify bounding boxes, 
   sorting etc. via the API. 

 - Use a plugin approach to extend the indexing of a custom metadata block, which then would do the coordinate extraction and transformation in Java code. 
   This has major consequences for the search logic which I can not oversee. 
   But this might be something that will replace those TSV files base customization, because it is cumbersome. Using plugins would possibly also allow for custom metadata with special UI behavior and or validation, which is now much limited. 


References
----------
TODO add lots of links here


Appendix
--------
TODO add screenshots
