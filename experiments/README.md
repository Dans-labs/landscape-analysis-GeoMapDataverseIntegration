# Experiments for extending

The goal of these experiments is to try if we can extend the Dataverse functionality with a search results display showing the geographical locations on an interactive map. 

Using the 'old' Dataverse version 6.2+, with JavaScript (jQuery) and the Leaflet geographical map library. 


## Direct injection (in the custom footer)

Using the development setup we have at DANS for our Archaeology Datastation, with vagrant and VirtualBox VM's. 
However this code/html fragment could be inserted into the custom footer file of the `test` or `demo` servers of `archaeology.datastations.nl`. 

The experimental [custom footer file](./custom-footer.html) is in this repo. 

Instructions for DANS developers with access to on the `dans-core-systems` repo:
1. Get into the repo directory (assuming you have everything in place for the standard development). 
2. Copy the custom footer file into the `shared` dir. 
3. SSH into the dev box with vagrant
4. Set the custom footer to point to that `/vagrant/shared` folder: `curl -X PUT -d '/vagrant/shared/custom-footer.html' http://localhost:8080/api/admin/settings/:FooterCustomizationFile`. 

When you edit that custom footer file in the `shared` directory just a browser page reload would be enough to see the difference. If you edit it in this git repo, then copy it to that shared directory after every change. Use the browser debugger/inspection tool to see those console messages and or any errors occurring. 

### Short description of the solution: 

The script in that custom footer (fragment) is kicking in with a search results page load (default the homepage). 

Map display: 
 - Initially the script extracts search parameters from the page URL. 
 - It uses that to get results from the (public) API, but then also requests to include the location information. 
 - It will transform it to markers with pop-ups on the map. 
   When markers are selected the popup appears with the datasets title as a link to the dataset landing page. 

With tabs it also does the following: 
 - Initially the script tries to get the previously stored Tab selection. 
   Default is the List tab, showing the list of paged results. 
 - When the Map tab is selected it will show the map and hide the list results. 
 - If the List tab is selected it will hide the map and show te list. 
 - The selection is stored, so when the page is reloaded because of a search change, the map stays selected if it was, or the list stays selected. 

### Evaluation of this approach

Pros: 

No DV code changes needed; makes it great for prototyping and demonstrating functionality

Cons:

  - Not everything is possible, depends on available API and content of the html page as rendered. Backend changes are not possible this way, so only if it is available on the front end. 
  - Sometimes difficult to achieve the same look-and-feel as the existing components. 
  - Not easy to maintain; DV development is not aware of our dependencies and might change things in a way that breaks our code. 


## Separate 'view page', which could be embedded via an iframe

A stand-alone html file. 
At this point just hardcoded to get search results from the Archaeology production Datastation or the dev VM. 
Also no code yet that is looking into it's 'parent' URL from the iframe point of view.  

The [stand alone mapview html file](./experiments/mapview.html).

