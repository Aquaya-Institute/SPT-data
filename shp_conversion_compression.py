#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 15 15:24:18 2020

@author: karastuart
"""
import os
# from shapely.geometry import mapping
import topojson as tp
import geopandas as gp
# import matplotlib.pyplot as plt

os.chdir(os.path.dirname(os.path.abspath(__file__))) #Set working directory to the folder where the script is saved.

#########Set Variables########
#Varibale-specfic variables
cc = 'gha'  #country code
var = 'roads'  #variable name
shp_filename = 'gh_roads_123.shp'  #shapefile name

#Global variables
datasets_dir = 'datasets'
glob_dir = 'global'

#Define paths
shp_path = os.path.join('./' + datasets_dir + '/' + cc + '/' + var + '/'+ shp_filename)
var_path = os.path.join('./' + datasets_dir + '/' + cc + '/' + var + '/')


########Convert to GeoJSON########
shp_file = gp.read_file(shp_path)
shp_file.to_file(var_path + cc + '_' + var + '.geojson', driver='GeoJSON')

#Convert to GeoDataFrame
gpd_polygonized  = gp.GeoDataFrame.from_features(shp_file)

#Write to GeoJSON file (optional)
gpd_polygonized.to_file(var_path + cc + '_' + var + '.json', driver='GeoJSON')


########Compress GeoJSON########
#Simplify GeoDataFrame
#boundaries: toposimplify=.001
#classes: toposimplify=.0001
topo = tp.Topology(gpd_polygonized, 
                   prequantize=False, 
                   topology=True, 
                   toposimplify=100, 
                   simplify_with='simplification', 
                   simplify_algorithm='vw',
                   prevent_oversimplify=True)

#Write to TopoJSON file
topo.to_json(var_path + cc + '_' + var + '.topo.json')

# #Plot to test resolution
# topo_load = gp.GeoDataFrame.from_file(var_path + cc + '_' + var + '.topo.json')
# topo.plot()
# plt.show()

