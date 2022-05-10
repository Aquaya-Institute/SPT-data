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
from shapely.geometry import box
import numpy as np
import math
import mercantile
# import rasterio
# from osgeo import gdal, ogr, osr
# import rioxarray as rxr
# from shapely.geometry import mapping
# from rasterio.features import shapes
# import rasterio.mask
# import fiona

os.chdir("/Users/karastuart/Dropbox (Aquaya)/WASHPaLS_RProjects/PEFO/SPT-data") #UPDATE


#########Set Variables########
#Varibale-specfic variables
cc = 'lbr'  #country code  #UPDATE
via var = 'dist'  #variable name, select either 'pixel5', 'pixel1', or 'dist'  #UPDATE


#Define paths
country_path = os.path.join('./datasets/' + cc + '/')
global_path = os.path.join('./datasets/global/')


file_path = 'dist/'+cc+'_adm2.shp'  #shapefile name #UPDATE number to be 2 or 3 as needed
shp_path = os.path.join(country_path + file_path)
dist = gpd.read_file(shp_path)
# dist = dist[["NAME_1", "NAME_2", "NAME_3", "geometry"]] #UPDATE include all boundary level names + geometry, there will be 2 or 3 depending on the country
# dist = dist[["NAME_1", "NAME_2", "geometry"]] #UPDATE include all boundary level names + geometry, there will be 2 or 3 depending on the country
dist = dist[["ADM1_EN", "ADM2_EN", "geometry"]] #UPDATE include all boundary level names + geometry, there will be 2 or 3 depending on the country
# dist = dist[["REGION", "DISTRICT", "geometry"]] 

od = os.path.join(global_path + 'IHME_OD.tif')
timecities = os.path.join(global_path + 'MAP_timecities.tif')
dia = os.path.join(global_path + 'IHME_Dia.tif')
cholera = os.path.join(global_path + 'IDD_cholera.tif')
s_unimp = os.path.join(global_path + 'IHME_S_UNIMP.tif')
w_unimp = os.path.join(global_path + 'IHME_W_UNIMP.tif')
edu_w = os.path.join(global_path + 'IHME_EDU_W_00-17.tif')
edu_m = os.path.join(global_path + 'IHME_EDU_M_00-17.tif')
u5m = os.path.join(global_path + 'IHME_U5M_00-17.tif')
dr = os.path.join(country_path + 'distroads/'+cc+'_distroads.tif')
dt = os.path.join(country_path + 'disttowns/'+cc+'_disttowns.tif')
classes = os.path.join(country_path + 'class/'+cc+'_class.tif')
pop = os.path.join(country_path + 'pop/'+cc+'_ppp_2020_constrained.tif')

if var=="dist":
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
        ("pop",pop)
        ]
    
elif var=="pixel":
    #Clip raster with shapefile
        # #Open raster
        # ras = rxr.open_rasterio(global_path+'IHME_OD.tif')
        # # Open crop extent (your study area extent boundary)
        # crop_extent = gpd.read_file(country_path+'/country/'+cc+'_adm0.shp')
        # crop_extent['geometry'] = crop_extent.geometry.buffer(.02)
        # #Clip raster
        # ras_clipped = ras.rio.clip(crop_extent.geometry.apply(mapping))
        # # Write to new geotiff file
        # ras_clipped.rio.to_raster(country_path+'od/' + cc + '_od.tif')
        
    #Mask raster with shapefile, remove all nodata cells
        # raster = gdal.Open(country_path+'od/' + cc + '_od.tif')
        # band = raster.GetRasterBand(1) # get first band of the raster
        # numpy_band = band.ReadAsArray() ##
        # numpy_band[numpy_band>-1] = 1     ##
        # numpy_band[numpy_band<-1] = 0   ##
        # mask = gdal.Open(country_path+'od/' + cc + '_od.tif',gdal.GA_Update)
        # maskband = mask.GetRasterBand(1) # get first band of the raster
        # maskband.WriteArray(numpy_band)     ##
        # drv = ogr.GetDriverByName('ESRI Shapefile')
        # outfile = drv.CreateDataSource(country_path+'od/' + cc + '_od.shp') 
        # outlayer = outfile.CreateLayer('polygonized raster', srs = None )
        # newField = ogr.FieldDefn('DN', ogr.OFTReal)
        # newField.SetWidth(10)
        # newField.SetPrecision(6)
        # outlayer.CreateField(newField)
        # gdal.Polygonize(band, maskband, outlayer, 0, [])
        # outfile = None
    
    #Custom grid within shapefile polygon
        crop_extent = gpd.read_file(country_path+'/country/'+cc+'_adm0.shp')
        xmin,ymin,xmax,ymax = crop_extent.total_bounds
        length = 0.04166667170983360396 # set y resolution
        wide = 0.04166666509561942067 # set x resolution
        cols = list(np.arange(xmin, xmax + wide, wide))
        rows = list(np.arange(ymin, ymax + length, length))
        polygons = []
        for x in cols[:-1]:
            for y in rows[:-1]:
                polygons.append(Polygon([(x,y), (x+wide, y), (x+wide, y+length), (x, y+length)]))
        grid = gpd.GeoDataFrame({'geometry':polygons})
        # crop_extent2 = crop_extent.simplify(.2, preserve_topology=True)
        grid_clip = gpd.clip(grid, crop_extent)
        grid_clip = grid_clip[~grid_clip.is_empty]
        grid_clip.to_file(country_path+var+'/'+cc+'_'+var+'.shp')
        bounds=gpd.read_file(country_path+var+'/'+cc+'_'+var+'.shp')
        bounds = bounds[["FID","geometry"]]
        # bounds = gpd.sjoin(bounds,dist,how="left",op="intersects")
        # bounds['area'] = bounds.area
        # bounds.sort_values('area', ascending=False, inplace=True)
        # bounds = bounds.groupby('FID').first()
    ########Convert to GeoJSON########
        # with rasterio.Env():
        #     with rasterio.open(country_path+'od/' + cc + '_od.tif') as src:
        #         image = src.read(1) # first band
        #         mask = None
        #         results = (
        #         {'properties': {'val': v}, 'geometry': s}
        #         for i, (s, v) 
        #         in enumerate(
        #             shapes(image, mask=mask, transform=src.transform)))
        # geoms = list(results)
    #Convert to GeoDataFrame
        # bounds  = gpd.GeoDataFrame.from_features(geoms)
        # bounds = bounds[bounds.val != -999999]
        # bounds = bounds[["geometry"]]
        
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
            ("pop",pop)
            ]

elif var=="pixel1":
    crop_extent = gpd.read_file(country_path+'/country/'+cc+'_adm0.shp')
    xmin,ymin,xmax,ymax = crop_extent.total_bounds
    length = 0.008334908031088082009 # set y resolution
    wide = 0.008328069288389512367 # set x resolution
    cols = list(np.arange(xmin, xmax + wide, wide))
    rows = list(np.arange(ymin, ymax + length, length))
    polygons = []
    for x in cols[:-1]:
        for y in rows[:-1]:
            polygons.append(Polygon([(x,y), (x+wide, y), (x+wide, y+length), (x, y+length)]))
    grid = gpd.GeoDataFrame({'geometry':polygons})
    # crop_extent2 = crop_extent.simplify(.2, preserve_topology=True)
    grid_clip = gpd.clip(grid, crop_extent)
    grid_clip = grid_clip[~grid_clip.is_empty]
    grid_clip.to_file(country_path+var+'/'+cc+'_'+var+'.shp')
    bounds=gpd.read_file(country_path+var+'/'+cc+'_'+var+'.shp')
    bounds = bounds[["FID","geometry"]]
    # bounds=gpd.read_file(country_path+'class/'+cc+'_class.geojson')
    
    vars = [
            ("classes",classes),
            # ("timecities",timecities),
            # ("dr",dr),
            # ("dt",dt),
            # ("pop",pop)
            ]

elif var=="comms":
    file_path = var+'/'+cc+'_comms_s.shp'  #shapefile name #UPDATE number to be 2 or 3 as needed
    shp_path = os.path.join(country_path + file_path)
    bounds = gpd.read_file(shp_path)
    bounds = bounds[["geometry"]]
    
    vars = [
            # ("od",od),
            ("timecities",timecities),
            # ("dia",dia), 
            # ("cholera",cholera), 
            # ("s_unimp",s_unimp), 
            # ("w_unimp",w_unimp),
            # ("edu_w",edu_w), 
            # ("edu_m",edu_m), 
            # ("u5m",u5m),
            ("dr",dr),
            ("dt",dt),
            ("classes",classes),
            ("pop",pop)
            ]
    
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
        
        # bounds["4.0"].fillna(0, inplace = True)
        # bounds["3.0"].fillna(0, inplace = True)
        # bounds["2.0"].fillna(0, inplace = True)
        # bounds["1.0"].fillna(0, inplace = True)
        # bounds["rr"] = round(100*(bounds["1.0"]/(bounds["1.0"]+bounds["2.0"]+bounds["3.0"]+bounds["4.0"])),0)
        # bounds["rrd"] = round(100*(bounds["2.0"]/(bounds["1.0"]+bounds["2.0"]+bounds["3.0"]+bounds["4.0"])),0)
        # bounds["rm"] = round(100*(bounds["3.0"]/(bounds["1.0"]+bounds["2.0"]+bounds["3.0"]+bounds["4.0"])),0)
        # bounds["u"] = round(100*(bounds["4.0"]/(bounds["1.0"]+bounds["2.0"]+bounds["3.0"]+bounds["4.0"])),0)

    else:
        tmp=round(tmp,0)
    
    bounds = pd.concat([bounds, tmp], axis=1)

###################################################
if var=="comms":
    bounds = bounds[["geometry",'timecities','dr','dt','classes','rr','rrd','rm','u','pop']]
else:
    bounds = bounds[["geometry",'od','timecities','dia','cholera','s_unimp','w_unimp','edu_w','edu_m','u5m','dr','dt','classes','rr','rrd','rm','u','pop']]
bounds.set_geometry('geometry', inplace=True)
# with open(country_path+var+'/'+cc+'_multivariable_noadmin_'+var+'.geojson', 'w') as f:
#     f.write(bounds.to_json())

bounds.to_file(country_path+var+'/'+cc+'_multivariable_noadmin_'+var+'.shp')

# bounds=gpd.read_file(country_path+var+'5/'+cc+'_multivariable_'+var+'5.geojson')
# bounds.fillna(-1, inplace = True)
# bounds.to_file(country_path+var+'5/'+cc+'_multivariable_'+var+'no0.shp')

min = pd.DataFrame(bounds.min())
max = pd.DataFrame(bounds.max())
varvals= pd.concat([min, max], axis=1)
varvals.to_csv(country_path+var+'/'+cc+'_'+var+'_varvals.csv')

###################################################
# countries=["khm","lbr","gha","ner","rwa","nga","mdg","eth","sen","tza","ken","cod"]
# # gdf = pd.read_csv(os.path.join(country_path + 'poverty/'+cc+'_relative_wealth_index.csv'))

# for cc in countries:
#     gdf = gpd.read_file(os.path.join('./datasets/' + cc + '/poverty/'+cc+'_relative_wealth_index.csv'))
#     gdf = gpd.GeoDataFrame(gdf, geometry=gpd.points_from_xy(gdf.longitude, gdf.latitude))
#     gdf.crs = 'epsg:4326'
#     gdf.to_file('./datasets/' + cc + '/poverty/'+cc+'_relative_wealth_index.shp')

# gdf['new_geom']=gdf['quadkey']
# gdf['new_geom']=box(*mercantile.bounds(mercantile.quadkey_to_tile(gdf['quadkey'])))

# from pandas import DataFrame
# for index, row in gdf.iterrows():  
#     row['geometry']=box(*mercantile.bounds(mercantile.quadkey_to_tile(row['quadkey'])))
#     gdf.append(DataFrame(row))
# for x in range(gdf.shape[0]):
#     gdf.loc[x,'geometry']=box(*mercantile.bounds(mercantile.quadkey_to_tile(gdf.loc[x,'quadkey'])))
# for x in range(10):
#     gdf.loc[x,'geometry']=box(*mercantile.bounds(mercantile.quadkey_to_tile(gdf.loc[x,'quadkey'])))