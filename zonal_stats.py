#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 10 23:14:17 2020

@author: karastuart
"""
import os
import pandas as pd
# import numpy as np
import geopandas as gpd
# import rasterio as rio
# from rasterio.mask import mask
import topojson as tp
# from shapely.wkt import loads as load_wkt
# import gdal
# import rioxarray
# from rasterio.warp import reproject
from rasterstats import zonal_stats

os.chdir('/Users/karastuart/phase2/sanitation-planning-data')

#########Set Variables########
#Varibale-specfic variables
cc = 'gha'  #country code
var = 'dist'  #variable name

#Global variables
datasets_dir = 'datasets'
glob_dir = 'global'

#Define paths
var_path = os.path.join('./' + datasets_dir + '/' + cc + '/' + var + '/')
ras_path = os.path.join('./' + datasets_dir + '/' + glob_dir + '/')
ras_clipped_path = os.path.join('./' + datasets_dir + '/' + cc + '/no_vis/')

if var=="dist":
    shp_filename = '216district.shp'  #shapefile name
    shp_path = os.path.join('./' + datasets_dir + '/' + cc + '/' + var + '/'+ shp_filename)
    bounds = gpd.read_file(shp_path)
    bounds = bounds[["REGION", "DISTRICT", "geometry"]]
elif var=="comms":
    shp_filename = 'gh_comms_poly.shp'  #shapefile name
    shp_path = os.path.join('./' + datasets_dir + '/' + cc + '/' + var + '/'+ shp_filename)
    bounds = gpd.read_file(shp_path)
    bounds = bounds[["fid", "pop_est", "geometry"]]
    
# #Global
# od = rio.open(ras_path + 'IHME_OD.tif')
# timecities = rio.open(ras_path + 'MAP_timecities.tif')
# dia = rio.open(ras_path + 'IHME_Dia.tif')
# cholera = rio.open(ras_path + 'IDD_cholera.tif')
# s_unimp = rio.open(ras_path + 'IHME_S_UNIMP.tif')
# w_unimp = rio.open(ras_path + 'IHME_W_UNIMP.tif')

# edu_w = rio.open(ras_path + 'IHME_EDU_W_00-17.tif')
# edu_w=edu_w.read(18)
# edu_m = rio.open(ras_path + 'IHME_EDU_M_00-17.tif')
# edu_m=edu_m.read(18)
# u5m = rio.open(ras_path + 'IHME_U5M_00-17.tif')
# u5m=u5m.read(18)
# #Country
# dr = rio.open(ras_clipped_path + 'gh04_prox_r.tif')
# dt = rio.open(ras_clipped_path + 'gh11_prox_t.tif')
# classes = rio.open(ras_clipped_path + 'gh12_class_round.tif')

# gdal_band=classes.GetRasterBand(1)
# stats = gdal_band.GetStatistics(True, True)
# classes.reproject(districts.crs)
    
####################
od = os.path.join(ras_path + 'IHME_OD.tif')
timecities = os.path.join(ras_path + 'MAP_timecities.tif')
dia = os.path.join(ras_path + 'IHME_Dia.tif')
cholera = os.path.join(ras_path + 'IDD_cholera.tif')
s_unimp = os.path.join(ras_path + 'IHME_S_UNIMP.tif')
w_unimp = os.path.join(ras_path + 'IHME_W_UNIMP.tif')
edu_w = os.path.join(ras_path + 'IHME_EDU_W_00-17.tif')
edu_m = os.path.join(ras_path + 'IHME_EDU_M_00-17.tif')
u5m = os.path.join(ras_path + 'IHME_U5M_00-17.tif')
dr = os.path.join(ras_clipped_path + 'gh04_prox_r.tif')
dt = os.path.join(ras_clipped_path + 'gh11_prox_t.tif')
classes = os.path.join(ras_clipped_path + 'gh12_class_round.tif')

vars = [
        ('od',od),
        ("timecities",timecities),
        ("dia",dia), 
        ("cholera",cholera), 
        ("s_unimp",s_unimp), 
        ("w_unimp",w_unimp),
        ("edu_w",edu_w), 
        ("edu_m",edu_m), 
        ("u5m",u5m),
        ("dr",dr),
        ("dt",dt),
        ("classes",classes)
        ]

for i in vars:
    if i[0] in ('u5m','edu_w','edu_m'):
        tmp=zonal_stats(shp_path, i[1], stats="mean", all_touched=True, band=18)
    elif i[0]=='classes':
        tmp=zonal_stats(shp_path, i[1], stats="mean", all_touched=True, categorical=True)
    else:
        tmp=zonal_stats(shp_path, i[1], stats="mean", all_touched=True, band=1)
    tmp=gpd.GeoDataFrame(tmp)
    tmp=tmp.rename(columns={"mean": i[0]})
    if i[0]=='cholera':
        tmp=round(100000*tmp,1)
    elif i[0]=='u5m':
        tmp=round(tmp,3)
    else:
        tmp=round(tmp,0)
    bounds = pd.concat([bounds, tmp], axis=1)

###################################################
# def derive_stats(geom, data, **mask_kw):
#     masked, mask_transform = mask(dataset=data, shapes=(geom,),
#                                   crop=True, all_touched=True, filled=True)
#     return masked
# # bounds=bounds.to_crs(epsg=4326)
# # derive_stats(data=od,geom=bounds.geometry)

# for i in vars:
#     if i[0]=='cholera':
#         bounds[i[0]]=round(100000*derive_stats(data=i[1], geom=bounds.geometry).apply(np.mean),1)
#     elif i[0]=='u5m':
#         bounds[i[0]]=round(derive_stats(data=i[1], geom=bounds.geometry).apply(np.mean),3)
#     elif i[0] in ('dr','dt'):
#         bounds[i[0]]=round(derive_stats(data=i[1], geom=bounds.geometry).apply(np.mean),1)
#     else:
#         bounds[i[0]]=round(derive_stats(data=i[1], geom=bounds.geometry).apply(np.mean),0)
#     # bounds[i[0]] = derive_stats(data=i[1], geom=bounds.geometry).apply(np.mean)




###################################################
#boundaries: toposimplify=.001
#classes: toposimplify=.0001
topo = tp.Topology(bounds, 
                    prequantize=False, 
                    topology=True, 
                    toposimplify=.001, 
                    simplify_with='simplification', 
                    simplify_algorithm='vw',
                    prevent_oversimplify=True)
# topo  = topo.crs(epsg=4326)
#Write to TopoJSON file
topo.to_json(var_path+cc+'_'+var+'.topo.json')

if var=="comms":
    # copy poly to new GeoDataFrame
    points = bounds.copy()
    # change the geometry
    points.geometry = points['geometry'].centroid
    # same crs
    points.crs =bounds.crs
    topo = tp.Topology(points, 
                    prequantize=False, 
                    topology=True, 
                    toposimplify=.001, 
                    simplify_with='simplification', 
                    simplify_algorithm='vw',
                    prevent_oversimplify=True)
    # topo  = topo.crs(epsg=4326)
    #Write to TopoJSON file
    topo.to_json(var_path+cc+'_'+var+'_point.topo.json')

