##Map generation SOP
from qgis.core import *
import processing
import qgis.utils
import os # This is is needed in the pyqgis console also

dir = "/Users/karastuart/Dropbox (Aquaya)/WASHPaLS_RProjects/PEFO/SPT-data/datasets/"

directory = os.fsencode(dir)
cc = "tza" #update as needed
grid3 = "yes"

def mergelayers(layers, out_fn):
    processing.run("native:mergevectorlayers", {'LAYERS':layers,\
    'CRS':None,\
    'OUTPUT':out_fn})
if(grid3=="yes"):
    bua = dir+cc+"/comms/"+cc+"_GRID3.gdb|layername=bua_extents"
    ssa = dir+cc+"/comms/"+cc+"_GRID3.gdb|layername=ssa_extents"
    layers = [bua, ssa]
    outfn=dir+cc+"/comms/"+cc+"_buassa.shp"
    mergelayers(layers, outfn)

def bufferlayer(in_fn, out_fn, dist):
    processing.run("native:buffer", {'INPUT':in_fn,
    'DISTANCE':dist,'SEGMENTS':5,'END_CAP_STYLE':0,'JOIN_STYLE':0,
    'MITER_LIMIT':2,'DISSOLVE':False,'OUTPUT':out_fn})
if(grid3=="yes"):
    infn = dir+cc+"/comms/"+cc+"_buassa.shp"
else:
    infn = dir+cc+"/comms/"+cc+"_clus_concave.gpkg"
outfn = dir+cc+"/comms/"+cc+"_buassa_b.shp"
dist = 0.001
bufferlayer(infn, outfn, dist)

def zonal(in_ras,in_vec):
    processing.run("qgis:zonalstatistics", {'INPUT_RASTER':in_ras,
    'RASTER_BAND':1,'INPUT_VECTOR':in_vec,
    'COLUMN_PREFIX':'_','STATISTICS':[1]})
in_ras = dir+cc+"/pop/"+cc+"_ppp_2020_constrained.tif"
in_vec = dir+cc+"/comms/"+cc+"_buassa_b.shp"
zonal(in_ras,in_vec)

#Select 5,000+, save as
def extract_towns(in_fn, out_fn, field, val):
    processing.run("native:extractbyattribute", {'INPUT':in_fn,\
    'FIELD':field,'OPERATOR':3,'VALUE':val,\
    'OUTPUT':out_fn})
val = "5000"
outfn = dir+cc+"/disttowns/"+cc+"_towns.shp"
infn=dir+cc+"/comms/"+cc+"_buassa_b.shp"
field='_sum'
extract_towns(infn, outfn, field, val)

#Select 50,000+, save as
val = "50000"
outfn = dir+cc+"/disttowns/"+cc+"_cities.shp"
infn=dir+cc+"/comms/"+cc+"_buassa_b.shp"
field='_sum'
extract_towns(infn, outfn, field, val)

if(grid3=="yes"):
    #Select large hamlets, save as
    val = ".0000045"
    outfn = dir+cc+"/comms/"+cc+"_hambig.shp"
    infn=dir+cc+"/comms/"+cc+"_GRID3.gdb|layername=hamlet_extents"
    field='Shape_Area'
    extract_towns(infn, outfn, field, val)

    #Buffer large hamlets
    infn = dir+cc+"/comms/"+cc+"_hambig.shp"
    outfn = dir+cc+"/comms/"+cc+"_hambig_b.shp"
    dist = 0.0005
    bufferlayer(infn, outfn, dist)

    #Merge all settlements
    buassa = dir+cc+"/comms/"+cc+"_buassa_b.shp"
    ham = dir+cc+"/comms/"+cc+"_hambig_b.shp"
    layers = [buassa, ham]
    outfn=dir+cc+"/comms/"+cc+"_comms_b.shp"
    mergelayers(layers, outfn)