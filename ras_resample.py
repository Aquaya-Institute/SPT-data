#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 14 15:13:55 2020

@author: karastuart
"""

#Open raster
rds = xarray.open_rasterio('./datasets/global/MAP_timecities.tif').squeeze().drop("band")
rds.attrs.pop("nodatavals")

#Resample raster
##
downsampled = rds.rio.reproject(rds.rio.crs, resolution=0.05)

#Write to new geotiff file
downsampled.rio.to_raster('./datasets/global/MAP_timecities_rs.tif')


