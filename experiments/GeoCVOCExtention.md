Geographical CVOC Extension
===========================

Extend with improved 'CVOC' funcionalities for the dataset metadata input of a location by the placename as text. 
Instead of just free text we use Geonames service to retrieve the name and it's ID. 

__NOTE__ The geonames services can do a lot more than lookup names and also has coordinates of places. 

The 'static' example is  based on the code for Orcid in the gdcc Github repository for CVOC support: https://github.com/gdcc/dataverse-external-vocab-support/blob/main/examples/staticOrcidAndRorExample.html

The example will only work if the geonames username (of an API enabled account) is inserted in the code. 

The [stand alone (static) geonames as CVOC example html file](./staticgeonamesExample.html).

It's main purpose is to develop the client code (Javascript) without the need of a Dataverse application and its configuration. 

The jQuery Select2 component is used to implement the autocomplete dropdown. 
The folowing geonames endpoints (or pages) are being used: 

- A landing page for a place using the geonames id or the URI: 
  `https://sws.geonames.org/{id}`
- An API endpoint to retrieve JSON with the name given the 'id': 
  `http://api.geonames.org/getJSON?formatted=true&geonameId={id}&username={username}&style=full`
- An API endpoint to retrieve JSON for the matching places using the first characters:
  `http://api.geonames.org/searchJSON?q=*&name_startsWith={chars}&maxRows=710&username={username}`
