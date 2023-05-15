##### Settlements generation SOP #####
from qgis.core import *
import processing
import qgis.utils
import os # This is is needed in the pyqgis console also

dir = "/Users/karastuart/Dropbox (Aquaya)/WASHPaLS_RProjects/PEFO/SPT-data/datasets/"   # UPDATE
directory = os.fsencode(dir)
cc = "idn"  # country code  #UPDATE

### Pixels to Points
def pixels_points(in_fn,out_fn):
    processing.run("native:pixelstopoints", {'INPUT_RASTER':in_fn,\
    'RASTER_BAND':1,'FIELD_NAME':'VALUE','OUTPUT':out_fn})
in_fn = dir+cc+"/pop/"+cc+"_ppp_2020_constrained.tif"
out_fn = dir+cc+"/comms/"+cc+"_raspoints.shp"
pixels_points(in_fn,out_fn)

### DBSCAN Clustering
def cluster(in_fn, min_clus, dist, out_fn):
    processing.run("native:dbscanclustering", {'INPUT':in_fn,\
    'MIN_SIZE':min_clus,'EPS':dist,'DBSCAN*':False,\
    'FIELD_NAME':'CLUSTER_ID','OUTPUT':out_fn})
in_fn = dir+cc+"/comms/"+cc+"_raspoints.shp"
min_clus = 2
dist = 0.005
out_fn = dir+cc+"/comms/"+cc+"_raspoints_clus.shp"
cluster(in_fn, min_clus, dist, out_fn)

### Remove NULL cluster IDs
def extract(in_fn,out_fn):
    processing.run("native:extractbyattribute", {'INPUT':in_fn,\
    'FIELD':'CLUSTER_ID','OPERATOR':9,'VALUE':'','OUTPUT':out_fn})
in_fn = dir+cc+"/comms/"+cc+"_raspoints_clus.shp"
out_fn = dir+cc+"/comms/"+cc+"_raspoints_clus_nonull.gpkg"
extract(in_fn, out_fn)

### Buffer clusters
def buff(in_fn,out_fn):
    processing.run("native:buffer", {'INPUT':in_fn,\
    'DISTANCE':0.0015,'SEGMENTS':5,'END_CAP_STYLE':0,\
    'JOIN_STYLE':0,'MITER_LIMIT':2,'DISSOLVE':False,'OUTPUT':out_fn})
in_fn = dir+cc+"/comms/"+cc+"_raspoints_clus_nonull.gpkg"
out_fn = dir+cc+"/comms/"+cc+"_raspoints_clus_nonull_buff.gpkg"
buff(in_fn, out_fn)

### Concave hull
def polygon(in_fn,out_fun):
    processing.run("qgis:minimumboundinggeometry", {'INPUT':in_fn,\
    'FIELD':'CLUSTER_ID','TYPE':3,'OUTPUT':out_fn})
in_fn = dir+cc+"/comms/"+cc+"_raspoints_clus_nonull_buff.gpkg"
out_fn = dir+cc+"/comms/"+cc+"_clus_concave.gpkg"
polygon(in_fn, out_fn)
#%%
