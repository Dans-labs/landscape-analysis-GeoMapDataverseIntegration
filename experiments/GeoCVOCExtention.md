Geographical CVOC Extension
===========================

Extend with improved 'CVOC' funcionalities for the dataset metadata input of a location by the placename as text. 
Instead of just free text we use Geonames service to retrieve the name and it's ID. 

__NOTE__: The geonames services can do a lot more than lookup names and also has coordinates of places. 

__NOTE__: The GeoNames API limits users to a maximum of 10000 credits per day and 1000 credits per hour. See here for a list of how many credits a request to each endpoint uses.

## Static demonstator

The 'static' example is  based on the code for Orcid in the gdcc Github repository for CVOC support: https://github.com/gdcc/dataverse-external-vocab-support/blob/main/examples/staticOrcidAndRorExample.html

The example will only work if the geonames username (of an API enabled account) is inserted in the code. 

The [stand alone (static) geonames as CVOC example html file](./staticgeonamesExample.html).

It's main purpose is to develop the client code (Javascript) without the need of a Dataverse application and its configuration. 

The ‘Input’ and ‘Display’ sections mimic the way that Dataverse will render the HTML when configured for this geonames CVOC connection. The ‘Input’ section allows to enter a name of a location and there will be autocomplete functionality resulting in a Geonames ID, instead of free text.

The ‘Display’ section has element that contain the Geonames ID and the script will insert an icon with a link to the Geonames landingpage of that location. 


The next screenshot was taken after 'Ams' was entered and then the correct value (Amsterdam) was selected from the autocomplete dropdown. 

![Screenshot-Static-Geonames-Demonstator](./images/ScreenshotStaticGeonamesDemonstator.png)


The jQuery Select2 component is used to implement the autocomplete dropdown. 
The following geonames endpoints (or pages) are being used: 

- A landing page for a place using the geonames id or the URI: 
  `https://sws.geonames.org/{id}`
- An API endpoint to retrieve JSON with the name given the 'id': 
  `http://api.geonames.org/getJSON?formatted=true&geonameId={id}&username={username}&style=full`
- An API endpoint to retrieve JSON for the matching places using the first characters:
  `http://api.geonames.org/searchJSON?q=*&name_startsWith={chars}&maxRows=710&username={username}`

The script is now producing similar behavior as for the other autocomplete input fields (via Skosmos), which is good because the user will understand the UI better if it is consistent. THe script code could also do other things, like filling in other fields or display other means of input besides that select2 jQuery component. 

The geonames service has some downsides: 

- The free API use is restricted to 1000 requests per hour, this might not be enough if the archive is used a lot with simultaneous dataset creation or metadata editing. We could pay for it and get more allowed requests if this is happening. 

- The API needs a username (like an API key). 
If we put that in the client code anyone could use that for their own purpose. We could create our own service that uses the geonames in turn on the server side. That 'proxy' service should restrict access to the browser and have CORS set to only allow XHR from our own pages. 


## Demonstation with Dataverse development server

To get the CVOC working in an actual Dataverse instance the script must be placed in a separate file and the Dataverse configuration must be adapted to include the geonames CVOC. 

The other scripts; `ror.js` and `skosmos.js` are avaiable to the web application by placing them in the `/var/www/html/custom` directory. So we need to copy [`geonames.js`](./geonames.js).into the same directory ad make sure the permissions allow the application to read it. 
Then edit the file and assign the correct 'username' to the `geonamesUsername` variable. 

Add the configuration JSON in the `geonames.json` file to the exitsing config. Firts get the existing config into a file:
```
curl http://localhost:8080/api/admin/settings/:CVocConf | jq -r '.data.message' | jq > cvoc-conf.json

```

Then  add that geo part to the end, but inside those brackets and do not forget to set the correct `username` in that `retrieval-uri` property. 
Finally set the configuration it with curl:
```
curl -X PUT --upload-file cvoc-conf.json http://localhost:8080/api/admin/settings/:CVocConf

```

In order to demonstrate you have to login and edit the metadata of an existing dataset (or first create a new one). The CVOC is enabled on the `Spatial Coverage (Free Text)` field of the `Temporal and Spatial Coverage` block. Just click on it and start typing. The following screenshot shows the interface when a vew characters where typed.  
![Screenshot-Geonames-Entering-Name](./images/ScreenshotGeonamesEnteringName.png)

After finishing entering and saving the dataset we can have a look at the metadata display. Both the name and the ID (URI) are available to the application. The next screenshot shows that the Geonames icon next to the placename links to the Geonames landingpage. 

![Screenshot-Geonames-Display-Name](./images/ScreenshotGeonamesDisplayName.png)

What information is available on that Dataverse instance after a name has been entered using the geonames CVOC?

The following fragment shows what is available in the Dataset JSON we can obtain via the API. 
The curl call
```
curl "https://dev.archaeology.datastations.nl/api/datasets/:persistentId/?persistentId=doi:10.5072/DAR/BWCEAC" | jq .data
```

The JSON result fragment

```
{
  "typeName": "dansSpatialCoverageText",
  "multiple": true,
  "typeClass": "primitive",
  "value": [
    "https://sws.geonames.org/2759794"
  ],
  "expandedvalue": [
    {
      "scheme": "GEONAMES",
      "placeName": "Amsterdam",
      "@id": "https://sws.geonames.org/2759794",
      "@type": "https://schema.org/Place"
    }
  ]
}
```
The field contains the URI, but there is an `expandedvalue` that also has the 'human readable' name. 

The Solr search index however does not have that 'human readable' name. 

The curl call
```
curl "http://localhost:8983/solr/collection1/select?q=identifier:doi:10.5072/DAR/BWCEAC" | jq
```

The JSON result fragment

```
"dansSpatialCoverageText": [
  "https://sws.geonames.org/2759794"
],
```

So that is only the URI. This means that the 'human readable' name is not indexed and thus the dataset can not be found by this name if it is only in that field. Entering an obscure placename that is not in any other metadata or file data (because full-text indexing might pick it up) confirmed this. 

How can this be fixed, if we wanted to?
