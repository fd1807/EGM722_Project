#!/usr/bin/env python
# coding: utf-8

# # Part 1: Module and data import

# In[1]:


# this lets us use the figures interactively

import os
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
from cartopy.feature import ShapelyFeature
import cartopy.crs as ccrs
import matplotlib.patches as mpatches
import matplotlib.lines as mlines
from shapely.geometry import Point, LineString, Polygon
get_ipython().run_line_magic('matplotlib', 'inline')

plt.ion() # make the plotting interactive


# In[2]:


def generate_handles(labels, colors, edge='k', alpha=1):
    lc = len(colors)  # get the length of the color list
    handles = []
    for i in range(len(labels)):
        handles.append(mpatches.Rectangle((0, 0), 1, 1, facecolor=colors[i % lc], edgecolor=edge, alpha=alpha))
    return handles


# In[3]:


def scale_bar(ax, location=(0.32, 0.95)):
    x0, x1, y0, y1 = ax.get_extent()
    sbx = x0 + (x1 - x0) * location[0]
    sby = y0 + (y1 - y0) * location[1]

    ax.plot([sbx, sbx - 10000], [sby, sby], color='k', linewidth=9, transform=ax.projection)
    ax.plot([sbx, sbx - 5000], [sby, sby], color='k', linewidth=6, transform=ax.projection)
    ax.plot([sbx-5000, sbx - 10000], [sby, sby], color='w', linewidth=6, transform=ax.projection)

    ax.text(sbx, sby-1000, '10 km', transform=ax.projection, fontsize=10)
    ax.text(sbx-5000, sby-1000, '5 km', transform=ax.projection, fontsize=10)
    ax.text(sbx-8000, sby-1000, '0 km', transform=ax.projection, fontsize=10)


# In[4]:


#import data file: flood, buildings, roads, population excel file, county outline, sa outline
flood= gpd.read_file(os.path.abspath('Project_datafiles/Flood_2m.shp'))
roads= gpd.read_file(os.path.abspath('Project_datafiles/Fermanagh_roads.shp'))
buildings= gpd.read_file(os.path.abspath('Project_datafiles/Building_Fermanagh.shp'))
pop_demography=gpd.read_file(os.path.abspath('Project_datafiles/popdemography.csv'))
outline = gpd.read_file(os.path.abspath('Project_datafiles/Fermanagh_DCA.shp'))
small_area= gpd.read_file(os.path.abspath('Project_datafiles/SApoly.shp'))
land_cover= gpd.read_file(os.path.abspath('Project_datafiles/LC_Fermanagh.shp'))


# In[5]:


small_area =gpd.GeoDataFrame(pop_demography.merge(small_area, on="SA2011"))
small_area.head()


# In[6]:


small_area.rename(columns={'geometry_y':'geometry'}, inplace=True)

small_area.set_geometry('geometry')


# In[7]:


small_area['residents'] = small_area['residents'].astype(int)
small_area['Shape_Area'] = small_area['Shape_Area'].astype(int)


# In[8]:


for ind, row in small_area.iterrows(): # iterate over each row in the GeoDataFrame
    small_area.loc[ind, 'pop_density'] = row['residents']/ row['Shape_Area']* 1000000
print(small_area.head())


# In[9]:


small_area['pop_density'].describe()


# In[10]:


flood.to_crs(epsg = 2157)
roads.to_crs(epsg = 2157)
buildings.to_crs(epsg = 2157)
outline.to_crs(epsg = 2157)
small_area.to_crs(epsg = 2157)
land_cover.to_crs(epsg = 2157)


# In[11]:


def underwater(shapefile):
    flood_geom = flood['geometry'].values[0]
    underwater = shapefile['geometry'].within(flood_geom)
    return shapefile['geometry'].within(flood_geom)


# # Part 2: Landcover analyses and map

# In[12]:


myFig = plt.figure(figsize=(12, 12))  # create a figure of size 10x10 (representing the page size in inches)

myCRS = ccrs.UTM(29)  # create a Universal Transverse Mercator reference system to transform our data.
# be sure to fill in XX above with the correct number for the UTM Zone that Northern Ireland is part of.

ax = plt.axes(projection=myCRS)  # finally, create an axes object in the figure, using a UTM projection,
# where we can actually plot our data.


# In[13]:


# first, we just add the outline of Northern Ireland using cartopy's ShapelyFeature
outline_feature = ShapelyFeature(outline['geometry'], myCRS, edgecolor='k', facecolor='w')
xmin, ymin, xmax, ymax = flood.total_bounds
ax.add_feature(outline_feature) # add the features we've created to the map.
ax.set_extent([xmin-1000, xmax+1000, ymin-1000, ymax+1000], crs=myCRS)


# In[14]:


# get the number of unique municipalities we have in the dataset
landcover= len(land_cover.LAND_COVER.unique())
print('Number of unique features: {}'.format(landcover))


# In[40]:


land_cover_colors = ['springgreen','olive', 'sienna','darkred', 'lawngreen', 'forestgreen','yellowgreen', 'y','darkgreen','darkorange','lightgrey','gold','black','grey']
landcover=list(land_cover.LAND_COVER.unique())
for ii, name in enumerate(landcover):
    feat = ShapelyFeature(land_cover.loc[land_cover['LAND_COVER'] == name, 'geometry'], # first argument is the geometry
                          myCRS, # second argument is the CRS
                          edgecolor='k', # outline the feature in black
                          facecolor=land_cover_colors[ii],
                        linewidth=0.1,
                         alpha=0.8) # set the face color to the corresponding color from the list
                           # set the outline width to be 1 pt
                           # set the alpha (transparency) to be 0.25 (out of 1)
    ax.add_feature(feat)

myFig


# In[44]:


flood_feature = ShapelyFeature(flood['geometry'], myCRS, edgecolor='k',facecolor='navy',alpha=1,linewidth=0.1)
ax.add_feature(flood_feature)


# In[41]:


landcover_handles = generate_handles(land_cover.LAND_COVER.unique(), land_cover_colors)
flood_handles = generate_handles(['Flood'], ['navy'])


# In[42]:


# ax.legend() takes a list of handles and a list of labels corresponding to the objects
# you want to add to the legend
handles = landcover_handles  + flood_handles # use '+' to concatenate (combine) lists
labels = landcover + ['Flood']

leg = ax.legend(handles, labels, title='Legend', title_fontsize=12,
                 fontsize=10, loc='lower left', frameon=True, framealpha=1)

gridlines = ax.gridlines(draw_labels=True, alpha=1, edgecolor='k') # draw  labels for the grid lines
                         
gridlines.left_labels = False # turn off the left-side labels
gridlines.bottom_labels = False

scale_bar(ax)
myFig # to show the updated figure


# In[43]:


lc_flooded = underwater(land_cover) # call underwater function to select land parcels in 5m flood zone
land_flooded = land_cover[lc_flooded] # subset the land cover shapefile to include only underwater = true
print(land_flooded[['LAND_COVER','Shape_Area']])


# In[21]:


land_flooded.groupby(['LAND_COVER'])['Shape_Area'].sum().sort_values(ascending=False)


# # Part 3: Infrastructure and population analyses and map

# In[22]:


build_flooded = underwater(buildings) # call underwater function to select land parcels in 5m flood zone
building_flooded = buildings[build_flooded] # subset the land cover shapefile to include only underwater = true

rd_flooded = underwater(roads) # call underwater function to select land parcels in 5m flood zone
roads_flooded = roads[rd_flooded] # subset the land cover shapefile to include only underwater = true

sa_flooded = small_area.sjoin(flood, how="inner") # call underwater function to select land parcels in 5m flood zone
 # subset the land cover shapefile to include only underwater = true
sa_flooded['SA2011'].count()


# In[23]:


sum_roads = roads_flooded['Length'].sum() /1000
sum_motorway = roads_flooded[roads_flooded['CLASS'] == 'A']['Length'].sum() /1000
print('{:.2f} total km of roads'.format(sum_roads))
print('{:.2f} total km of A class road'.format(sum_motorway))


# In[24]:


building_flooded.groupby(['CLASSIFICA'])['CLASSIFICA'].count().sort_values(ascending=False)


# In[25]:


high_density= sa_flooded[sa_flooded.pop_density==sa_flooded.pop_density.max()]
print(high_density[['SA2011', 'pop_density']])


# In[26]:


myFig2, ax = plt.subplots(1, 1, figsize=(10, 10), subplot_kw=dict(projection=myCRS))

xmin, ymin, xmax, ymax = flood.total_bounds
  # create a figure of size 10x10 (representing the page size in inches)
  # create a Universal Transverse Mercator reference system to transform our data.
# be sure to fill in XX above with the correct number for the UTM Zone that Northern Ireland is part of. 
# first, we just add the outline of Northern Ireland using cartopy's ShapelyFeature


# In[27]:


outline_feature = ShapelyFeature(outline['geometry'], myCRS, edgecolor='k', facecolor='w')
ax.add_feature(outline_feature)
#ax.add_feature(outline_feature) # add the features we've created to the map.
#ax.set_extent([xmin-1000, xmax+1000, ymin-1000, ymax+1000], crs=myCRS)# finally, create an axes object in the figure, using a UTM projection,
# where we can actually plot our data.
myFig2


# In[28]:


flood_feature = ShapelyFeature(flood['geometry'], myCRS, edgecolor='k',facecolor='navy',alpha=0.5,linewidth=0.1)
ax.add_feature(flood_feature)

roads_feature = ShapelyFeature(roads['geometry'], myCRS, edgecolor='k', linewidth=1)
ax.add_feature(roads_feature)


myFig2


# In[29]:


# ShapelyFeature creates a polygon, so for point data we can just use ax.plot()
residential=buildings.loc[buildings['CLASSIFICA']=='Residential']
residential_handle= ax.plot(residential.geometry.x, residential.geometry.y, 's', color='b', ms=2, transform=myCRS)

commercial=buildings.loc[buildings['CLASSIFICA']=='Commercial']
commercial_handle=ax.plot(commercial.geometry.x, commercial.geometry.y, 'o', color='k', ms=2, transform=myCRS)

education=buildings.loc[buildings['CLASSIFICA']=='Education']
education_handle=ax.plot(education.geometry.x, education.geometry.y, '^', color='g', ms=2, transform=myCRS)

health=buildings.loc[buildings['CLASSIFICA']=='Health']
health_handle=ax.plot(health.geometry.x, health.geometry.y, '*', color='r', ms=2, transform=myCRS)

other=buildings.loc[buildings['CLASSIFICA']=='Other']
other_handle=ax.plot(other.geometry.x, other.geometry.y, 'h', color='y', ms=2, transform=myCRS)

myFig2


# In[30]:


# set a variable that will call whatever column we want to visualise on the map
#myFig2= small_area.explore('population_density', cmap='viridis')
# set the range for the choropleth

divider = make_axes_locatable(ax)
cax = divider.append_axes("right", size="5%", pad=0.1, axes_class=plt.Axes)

#pop_density=small_area.plot(column='residents', ax=ax, vmax=10000, cmap='magma',
                       #legend=True, cax=cax, legend_kwds={'label': 'Resident Population'})


# In[31]:


small_area_plot = small_area.plot(column='pop_density', ax=ax, vmax=100, cmap='Blues',
                       legend=True, cax=cax, legend_kwds={'label': 'Population Density'})
sa_outline = ShapelyFeature(small_area['geometry'], myCRS, edgecolor='r',linewidth=0.1, facecolor='none')
ax.add_feature(sa_outline)
myFig2


# In[32]:


roads_handle = [mlines.Line2D([], [], color='k')]
flood_handle = generate_handles(['Flood'], ['navy'])


# In[33]:


# ax.legend() takes a list of handles and a list of labels corresponding to the objects
# you want to add to the legend
handles = roads_handle  + flood_handle + residential_handle + commercial_handle + other_handle + health_handle + education_handle # use '+' to concatenate (combine) lists
labels = ['Roads'] + ['Flood'] + ['Residential'] + ['Commercial'] + ['Other'] + ['Health'] + ['Education']

leg = ax.legend(handles, labels, title='Legend', title_fontsize=12,
                 fontsize=10, loc='lower left',markerscale=4, frameon=True, framealpha=1)


gridlines = ax.gridlines(draw_labels=True, alpha=1, edgecolor='k') # draw  labels for the grid lines
                         
gridlines.right_labels = False # turn off the left-side labels
gridlines.bottom_labels = False

scale_bar(ax)
myFig2 # to show the updated figure


# In[34]:


#create % column for elderly and child ?


# In[35]:


#all data shapefile clipped to flood polygon with within


# In[36]:


#analyses:-tot pop in flood polygon
#         - nbr resident houses
#         - tot length of road impacted and class A roas
#         - Sa with highest pop density and if any are adjacent
#         - SA with less than avg pop density
#         - which landcover types has highest area in flood poly
#         - total area flooded per landcover types
#         - SA with highest % of elderly/child
#         - SA with low pop density but high child %
#         - SA with medical building
#         - residential building furtherest from medical build (use original dataset ?)
#         - SA centre furthest from medical building


# In[37]:


#add scale and legend handle


# In[38]:


#create map and add features to map
# do second map with landcover


# In[ ]:


#different labels depending on building class and road class


# In[ ]:


#grid lines


# In[ ]:





# In[ ]:




