# EGM722_Project
Programming project for Module EGM722
1. Introduction

The aim of this program is to estimate the impact of a flooding event on the surrounding environment and infrastructure using the example of a 2m flood of the Lower Lough Erne in County Fermanagh, Northern Ireland (Fig 1). The program is made  of three different parts. The intent of the first section is to import the modules and the different data files as well as create a function to subset the different datasets using the flood model. The second part will assess the impact of the flood on the surrounding land and create a map showing the landcover of county Fermanagh. Finally, the last part will estimate the impact of the flood on the roads, buildings as well as examine the population density and the vulnerability of the population (percentage of elderly and children) located in the flooded area.  

2. Using the program

The user can fork the repository by ‘Fork’ in the upper right corner. To save the repository on their computer, the user can open the GitHub Desktop and go to ‘Your Repositories’ and finally choose the option ‘Clone a repository from the Internet’.

The repository contains the data files necessary to run the program. It is advisable to use the same files when running the program since most of the datasets were modified to make it easier to use. For example, the ‘CLASSIFICA’ attribute for the buildings shapefile was simplified to only include 5 different classes. The water class was removed from the landcover shapefile as it would be irrelevant for the analyses. It should also be possible to use the program using a different scenario with different datasets.

3. Results

3.1.	Landcover map and analyses

The first part of the second section, until the line of code, should produce a landcover map of Fermanagh County as well as a polygon, with a fifty percent transparency,  representing the 2m flood model (figure 2). The map should be zoomed to the flood polygon extent and should contain a legend in the lower left corner, a scale in the upper left corner and finally gridlines on the upper and right side of the map border. The last part of the code in this section should calculate the amount of flooded land (in sqm²) for each of the landcover impacted by the potential flood. 

3.2	Infrastructure and population analyses and map

As with the landcover map, the first part of the code, until the line of code 26, should produce a map with the 2m flood polygon model. This map should include the buildings, with a different marker for each class, the roads, the small area outlines and finally the population density of County Fermanagh. The map should also include a legend in the lower left corner, a scale in the upper left corner and gridlines in the upper and right edge of the map. One extra bar representing the population density should also be present along the right side of the map. 

The first spatial analyses, after clipping the data, should give the amount, in km, of roads as well as  A class road that would be under water in the event of a 2m flood. The results should be 2.35km for all roads and 1.18km for A class road. The following line of code should produce the number of flooded buildings, sorted by their ‘CLASSIFICA’. Finally, the three last line of code should return the Small Areas which fulfil the criteria of the data query. The first query should return the Small Area with the highest population density which should be the N00003042 Small Area. The second one should list the Small Areas which have an above average percentage of children as well as an above average percentage of elderly. Only two Small Areas should meet both criteria which are Small Area N00002928 and N00002983. The final line of code should show the Small Areas which have a low population density but have a high percentage of children or have a high percentage of elderly.

4. Troubleshooting

The first step to make sure there is no compatibility issue between the different modules, especially between python and the jupyter notebook, is to ensure that the latest version of the programs has been installed. For example, it is strongly advised to use the Python version 3.9 and above when using this program. 

If different data files are used to run the program, it is advisable to make sure that all the shapefile extensions (shp, dbf, shx,…) are transferred in the folder and that the change has been saved and upload to GitHub. The new shapefile name should also be changed in the jupyter notebook. If an excel file  is used instead of  a file with a CSV extension, it is recommended to change the code ‘gpd.read_file’ to ‘gpd.read_excel’ to avoid any problems when uploading the data. 

One recurring issue when modifying some of the map parameters, such as marker size or the feature transparency, in the jupyter notebook is that changes might not appear on the map or they might overlap with the previous version of the map. If that problem occurs, the best way to fix this is to select the kernel tab and choose the ‘Restart and Run all’ option. If that still does not resolve the issue, the jupyter notebook as well as the Anaconda Navigator should both be closed and restarted. 

The python program includes a help function which can provide assistance in case some of the functions are not operating as they should be or if after modifying the program part of the code does not work. This function can be called by typing help() and including the function name instead the parentheses or by typing the function name followed by a question mark. This will produce a docstring explaining what the function does and how to use it. 

Finally, there are several websites, such as stackoverflow (https://stackoverflow.com/),  which can provide assistance and help in solving issues when using programs such as python or the jupyter notebook. 

