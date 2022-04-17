
**Megascans batch processor v1.14**

This is the PDF guide for the megascans batch processor script for autodesk maya.
The megascans batch processor is a maya script that imports all the specified assets into maya, gives them a vertex gradient in the specified direction and exports them to a chosen destination folder.
  
**Adding the script to maya**
To add the script to maya open the script editor and click:
File>Open script..
Now select the MegaScansBatchProcessor.py file
You can save the script to your shelf by clicking:
File>Save Script to Shelf…

**Using the script and navigating the UI**
The UI consists of 3 parts, importing, vertex coloring and exporting.


_Help button_

When clicking the help button you will automatically open the github page with descriptions.


_Importing_

Using the checkboxes select which type of assets you want to import into maya. It is possible to select both 3D assets and foliage.
Click the browser to find your quixel bridge download folder.
Important! : select the right folder. The folder should be the /Downloaded folder from your quixel bridge application. If the wrong folder is selected the import button will be grayed out.
Example:  D:\Work\quixel bridge\Downloaded
Click the import button to import the selected objects from the selected import folder.



_Vertex gradient_

Select the assets in your scene that you want to give a vertex gradient. Use the radio buttons to specify in which direction the gradient should be.
Warning!: The vertex gradient process can take a bit of time depending on the fidelity and amount of the assets. 



_Exporting_

With the browser you can select the export path, all assets in your scene will be exported to this location using the original imported folder structure. Click export to export the assets.
Tip!: in the windows file explorer, copy the exported path /Downloaded folder into the /quixel bridge folder and overwrite the old assets to replace them with the processed ones. 

