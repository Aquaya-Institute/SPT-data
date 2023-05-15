#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 30 14:24:30 2021

@author: karastuart
"""

import os
import pandas as pd
import geopandas as gpd
from rasterstats import zonal_stats
from shapely.geometry import Polygon
import numpy as np
import math

os.chdir("/Users/karastuart/Dropbox (Aquaya)/WASHPaLS 2/PEFO/SPT-data") # UPDATE


###Set Variables
# Varibale-specfic variables
cc = 'cod'  # country code  #UPDATE
var = 'pixel'  # variable name, select either 'pixel', 'dist', or 'prov'  # UPDATE
suffix = "" # UPDATE - leave blank unless this is a second subnational boundary of the same resolution (e.g., add health districts as well as admin disticts. In this case, add a suffix such as "_health" when running for health districts.)
adm_fn = 'adm3'  # UPDATE number to be 2 or 3 as needed

#Define paths
country_path = os.path.join('./datasets/' + cc + '/')
global_path = os.path.join('./datasets/global/')


file_path = 'dist/'+cc+'_'+adm_fn+'.shp'  # shapefile name
shp_path = os.path.join(country_path + file_path)

### UPDATE IF VAR = DIST
dist = gpd.read_file(shp_path)
### UPDATE IF VAR = DIST select the line that includes the correct boundary level names + geometry
### there will be 2 or 3 boundary levels depending on the country
dist = dist[["ADM1_EN", "ADM2_EN", "geometry"]]
# dist = dist[["REGION", "DISTRICT", "geometry"]] 
# dist = dist[["ADM1_FR", "ADM2_FR", "NOM", "geometry"]]
# dist = dist[["NAME_1", "NAME_2", "NAME_3", "geometry"]]
# dist = dist[["NAME_1", "NAME_2", "geometry"]]

### UPDATE IF VAR = PROV
# prov = gpd.read_file(shp_path)
### UPDATE IF VAR = PROV select the line that includes the correct boundary level names + geometry
### there will be 2 or 3 boundary levels depending on the country
# prov = prov[["NAME_1", "geometry"]]
# prov = prov[["ADM1_EN", "geometry"]]
# prov = prov[["REGION", "geometry"]] 
# prov = prov[["ADM1_FR", "geometry"]]

### SET RAW DATA PATHS
od = os.path.join(global_path + 'IHME_OD.tif')
timecities = os.path.join(global_path + 'MAP_timecities.tif')
dia = os.path.join(global_path + 'IHME_Dia.tif')
cholera = os.path.join(global_path + 'IDD_cholera.tif')
s_unimp = os.path.join(global_path + 'IHME_S_UNIMP.tif')
s_imp = os.path.join(global_path + 'IHME_S_IMP.tif')
s_imp_other = os.path.join(global_path + 'IHME_S_IMP_OTHER.tif')
s_piped = os.path.join(global_path + 'IHME_S_PIPED.tif')
w_unimp = os.path.join(global_path + 'IHME_W_UNIMP.tif')
w_imp = os.path.join(global_path + 'IHME_W_IMP.tif')
w_imp_other = os.path.join(global_path + 'IHME_W_IMP_OTHER.tif')
w_piped = os.path.join(global_path + 'IHME_W_PIPED.tif')
w_surface = os.path.join(global_path + 'IHME_W_SURFACE.tif')
edu_w = os.path.join(global_path + 'IHME_EDU_W_00-17.tif')
edu_m = os.path.join(global_path + 'IHME_EDU_M_00-17.tif')
u5m = os.path.join(global_path + 'IHME_U5M_00-17.tif')
dr = os.path.join(country_path + 'distroads/'+cc+'_distroads.tif')
dt = os.path.join(country_path + 'disttowns/'+cc+'_disttowns.tif')
classes = os.path.join(country_path + 'class/'+cc+'_class.tif')
pop = os.path.join(country_path + 'pop/'+cc+'_ppp_2020_constrained.tif')

### Define variables depending on resolution and set boundaries to the appropriate regions
if var == "dist":
    bounds = dist
    vars = [
        ("od",od),
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
        ("classes",classes),
        ("pop",pop),
        ("s_imp", s_imp),
        ("s_imp_other", s_imp_other),
        ("s_piped", s_piped),
        ("w_imp", w_imp),
        ("w_imp_other", w_imp_other),
        ("w_piped", w_piped),
        ("w_surface", w_surface),
        ]
    
elif var == "prov":
    bounds = prov
    vars = [
        ("od",od),
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
        ("classes",classes),
        ("pop",pop),
        ("s_imp", s_imp),
        ("s_imp_other", s_imp_other),
        ("s_piped", s_piped),
        ("w_imp", w_imp),
        ("w_imp_other", w_imp_other),
        ("w_piped", w_piped),
        ("w_surface", w_surface),
        ]
    
elif var=="pixel":   
    ### Create custom grid within shapefile polygon, set as boundaries
        crop_extent = gpd.read_file(country_path+'country/'+cc+'_adm0.shp')
        xmin,ymin,xmax,ymax = crop_extent.total_bounds
        length = 0.04166667170983360396   # set y resolution
        wide = 0.04166666509561942067   # set x resolution
        cols = list(np.arange(xmin, xmax + wide, wide))
        rows = list(np.arange(ymin, ymax + length, length))
        polygons = []
        for x in cols[:-1]:
            for y in rows[:-1]:
                polygons.append(Polygon([(x,y), (x+wide, y), (x+wide, y+length), (x, y+length)]))
        grid = gpd.GeoDataFrame({'geometry':polygons})
        grid_clip = gpd.clip(grid, crop_extent)
        grid_clip = grid_clip[~grid_clip.is_empty]
        grid_clip.to_file(country_path+var+'/'+cc+'_'+var+'.shp')
        bounds=gpd.read_file(country_path+var+'/'+cc+'_'+var+'.shp')
        bounds = bounds[["FID","geometry"]]
        
        vars = [
            ("od",od),
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
            ("classes",classes),
            ("pop",pop),
            ("s_imp", s_imp),
            ("s_imp_other", s_imp_other),
            ("s_piped", s_piped),
            ("w_imp", w_imp),
            ("w_imp_other", w_imp_other),
            ("w_piped", w_piped),
            ("w_surface", w_surface),
            ]

elif var == "comms":
    file_path = var+'/'+cc+'_comms_s.shp'
    shp_path = os.path.join(country_path + file_path)
    bounds = gpd.read_file(shp_path)
    bounds = bounds[["geometry"]]
    
    vars = [
            ("timecities",timecities),
            ("dr",dr),
            ("dt",dt),
            ("classes",classes),
            ("pop",pop)
            ]

### Calculate zonal statistics for the boundaries
for i in vars:
    if i[0] in ('u5m','edu_w','edu_m'):
        tmp=zonal_stats(bounds, i[1], stats="mean", all_touched=True, band=18, nodata=-339999995214436420000000000000000000000)
    elif i[0]=='classes':
        tmp=zonal_stats(bounds, i[1], stats="mean", all_touched=True, categorical=True)
    elif i[0]=='pop':
        tmp=zonal_stats(bounds, i[1], stats="sum", all_touched=False, band=1, nodata=-99999)
    elif i[0]=='timecities':
        tmp=zonal_stats(bounds, i[1], stats="mean", all_touched=True, band=1, nodata=-9999)
    elif i[0]=='cholera':
        tmp=zonal_stats(bounds, i[1], stats="mean", all_touched=True, band=1, nodata=-339999995214436420000000000000000000000)
    elif i[0]=='dr':
        tmp=zonal_stats(bounds, i[1], stats="mean", all_touched=True, band=1, nodata=-340282346638528860000000000000000000000)
    else:
        tmp=zonal_stats(bounds, i[1], stats="mean", all_touched=True, band=1, nodata=-999999)

    ### Format values in attribute table
    tmp=gpd.GeoDataFrame(tmp)
    tmp=tmp.rename(columns={"mean": i[0]})
    tmp=tmp.rename(columns={"sum": i[0]})
    
    if i[0]=='cholera':
        tmp=round(100000*tmp,1)
    elif i[0]=='u5m':
        tmp=round(tmp*100,1)
    elif i[0] in ('dt','dr'):
        tmp=round(tmp/1000,1)
    elif i[0]=='dia':
        tmp=round(tmp/10,1)
    elif i[0]=='pop':
        tmp=round(tmp,0)
        tmp.fillna(0, inplace = True)
    elif i[0]=='classes':
        
        if var == 'dist':
            for x in range(tmp.shape[0]):
                if tmp.loc[x,1.0]== np.nanmax([tmp.loc[x,1.0],tmp.loc[x,2.0],tmp.loc[x,3.0], tmp.loc[x,4.0]]):
                    tmp.loc[x,'classes'] = 1
                elif tmp.loc[x,2.0]== np.nanmax([tmp.loc[x,1.0],tmp.loc[x,2.0],tmp.loc[x,3.0], tmp.loc[x,4.0]]):
                    tmp.loc[x,'classes'] = 2
                elif tmp.loc[x,3.0]== np.nanmax([tmp.loc[x,1.0],tmp.loc[x,2.0],tmp.loc[x,3.0], tmp.loc[x,4.0]]):
                    tmp.loc[x,'classes'] = 3
                elif tmp.loc[x,4.0]== np.nanmax([tmp.loc[x,1.0],tmp.loc[x,2.0],tmp.loc[x,3.0], tmp.loc[x,4.0]]):
                    tmp.loc[x,'classes'] = 4
        elif var == 'prov':
            for x in range(tmp.shape[0]):
                if tmp.loc[x,1.0]== np.nanmax([tmp.loc[x,1.0],tmp.loc[x,2.0],tmp.loc[x,3.0], tmp.loc[x,4.0]]):
                    tmp.loc[x,'classes'] = 1
                elif tmp.loc[x,2.0]== np.nanmax([tmp.loc[x,1.0],tmp.loc[x,2.0],tmp.loc[x,3.0], tmp.loc[x,4.0]]):
                    tmp.loc[x,'classes'] = 2
                elif tmp.loc[x,3.0]== np.nanmax([tmp.loc[x,1.0],tmp.loc[x,2.0],tmp.loc[x,3.0], tmp.loc[x,4.0]]):
                    tmp.loc[x,'classes'] = 3
                elif tmp.loc[x,4.0]== np.nanmax([tmp.loc[x,1.0],tmp.loc[x,2.0],tmp.loc[x,3.0], tmp.loc[x,4.0]]):
                    tmp.loc[x,'classes'] = 4
        else:
            for x in range(tmp.shape[0]):
                if (tmp.loc[x,4.0] > 0):
                    tmp.loc[x,'classes'] = 4
                elif (tmp.loc[x,3.0] > 0) & math.isnan(tmp.loc[x,4.0]):
                    tmp.loc[x,'classes'] = 3
                elif (tmp.loc[x,2.0] > 0) & math.isnan(tmp.loc[x,4.0]) & math.isnan(tmp.loc[x,3.0]):
                    tmp.loc[x,'classes'] = 2
                elif (tmp.loc[x,1.0] > 0) & math.isnan(tmp.loc[x,4.0]) & math.isnan(tmp.loc[x,3.0]) & math.isnan(tmp.loc[x,2.0]):
                    tmp.loc[x,'classes'] = 1
        tmp.fillna(0, inplace = True)
        tmp["rr"] = round(100*(tmp[1.0]/(tmp[1.0]+tmp[2.0]+tmp[3.0]+tmp[4.0])),0)
        tmp["rrd"] = round(100*(tmp[2.0]/(tmp[1.0]+tmp[2.0]+tmp[3.0]+tmp[4.0])),0)
        tmp["rm"] = round(100*(tmp[3.0]/(tmp[1.0]+tmp[2.0]+tmp[3.0]+tmp[4.0])),0)
        tmp["u"] = round(100*(tmp[4.0]/(tmp[1.0]+tmp[2.0]+tmp[3.0]+tmp[4.0])),0)
        
    else:
        tmp=round(tmp,0)
    
    bounds = pd.concat([bounds, tmp], axis=1)

### Filter columns for output
if var=="comms":
    bounds = bounds[["geometry",'timecities','dr','dt','classes','rr','rrd','rm','u','pop']]
else:
    bounds = bounds[["geometry",'od','timecities','dia','cholera','s_unimp','s_imp','s_imp_other','s_piped','w_unimp','w_imp','w_imp_other','w_piped','w_surface','edu_w','edu_m','u5m','dr','dt','classes','rr','rrd','rm','u','pop']]
bounds.set_geometry('geometry', inplace=True

### Output file
bounds.to_file(country_path+var+'/'+cc+'_multivariable_noadmin_'+var+suffix+'.shp')

### Create CSV of column minimums and maximums
min = pd.DataFrame(bounds.min())
max = pd.DataFrame(bounds.max())
varvals= pd.concat([min, max], axis=1)
varvals.to_csv(country_path+var+'/'+cc+'_'+var+suffix+'_varvals.csv')
#%%
