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
4. Set the custom footer to point to that `/vagrant/shared` folder. 

When you edit that custom footer file in the `shared` director just a browser page reload would be enough to see the difference. Use the browser debugger/inspection tool to see those console messages and or any errors occurring. 


## Separate 'view page', which could be embedded via an iframe

A stand-alone html file. 
At this point just hardcoded to get search results from the Archaeology production Datastation. 
Also no code that is looking ino it's 'parent' URL from the iframe point of view.  

**TODO:** add that file



