##Map generation SOP
from qgis.core import *
import processing
import qgis.utils
import os

dir = "/Users/karastuart/Dropbox (Aquaya)/WASHPaLS 2/PEFO/SPT-data/datasets/"   # UPDATE

directory = os.fsencode(dir)
cc = "sdn" # country code  # UPDATE
grid3 = "yes"  # UPDATE to "no" if non-African country

def mergelayers(layers, out_fn):
    processing.run("native:mergevectorlayers", {'LAYERS':layers,\
    'CRS':None,\
    'OUTPUT':out_fn})
    
##### Separate out hamlets (too many for efficient use) #####

### USE if settlements raw dataset is downloaded geodatabase folder (old version) rather than shapefile
#if(grid3=="yes"):
#    bua = dir+cc+"/comms/"+cc+"_GRID3.gdb|layername=bua_extents"
#    ssa = dir+cc+"/comms/"+cc+"_GRID3.gdb|layername=ssa_extents"
#    layers = [bua, ssa]
#    outfn=dir+cc+"/comms/"+cc+"_buassa.shp"
#    mergelayers(layers, outfn)

### USE if settlements raw dataset is NOT downloaded as geodatabase folder (old version)
def extract_settlementtype(in_fn, out_fn, field, val):
    processing.run("native:extractbyattribute", {'INPUT':in_fn,\
    'FIELD':field,'OPERATOR':val,'VALUE':'Hamlet',\
    'OUTPUT':out_fn})

### Remove halmets, save all bigger regions
val = 1
outfn = dir+cc+"/comms/"+cc+"_buassa.shp"
infn=dir+cc+"/comms/"+cc+"_grid3raw.shp"    # CHECK FILENAME OF RAW DATA
field='type'
extract_settlementtype(infn, outfn, field, val)

### Remove everything BUT halmets, save as hamlets
val = 0
outfn = dir+cc+"/comms/"+cc+"_ham.shp"
infn=dir+cc+"/comms/"+cc+"_grid3raw.shp"
field='type'
extract_settlementtype(infn, outfn, field, val)

### Buffer settlement boundaries to capture nearby population data and simplify geometry
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

### Sum population per settlement boundary
def zonal(in_ras,in_vec):
    processing.run("qgis:zonalstatistics", {'INPUT_RASTER':in_ras,
    'RASTER_BAND':1,'INPUT_VECTOR':in_vec,
    'COLUMN_PREFIX':'_','STATISTICS':[1]})
in_ras = dir+cc+"/pop/"+cc+"_ppp_2020_constrained.tif"
in_vec = dir+cc+"/comms/"+cc+"_buassa_b.shp"
zonal(in_ras,in_vec)

#Select 5,000+, save as "towns"
def extract_towns(in_fn, out_fn, field, val):
    processing.run("native:extractbyattribute", {'INPUT':in_fn,\
    'FIELD':field,'OPERATOR':3,'VALUE':val,\
    'OUTPUT':out_fn})
val = "5000"
outfn = dir+cc+"/disttowns/"+cc+"_towns.shp"
infn=dir+cc+"/comms/"+cc+"_buassa_b.shp"
field='_sum'
extract_towns(infn, outfn, field, val)

#Select 50,000+, save as "cities"
val = "50000"
outfn = dir+cc+"/disttowns/"+cc+"_cities.shp"
infn=dir+cc+"/comms/"+cc+"_buassa_b.shp"
field='_sum'
extract_towns(infn, outfn, field, val)

if(grid3=="yes"):
    #Select large hamlets, save as
    val = ".0000045"    # Customize if needed
    outfn = dir+cc+"/comms/"+cc+"_hambig.shp"
    infn=dir+cc+"/comms/"+cc+"_ham.shp"
    field='SHAPE_Area'
    extract_towns(infn, outfn, field, val)

    #Buffer large hamlets
    infn = dir+cc+"/comms/"+cc+"_hambig.shp"
    outfn = dir+cc+"/comms/"+cc+"_hambig_b.shp"
    dist = 0.0005
    bufferlayer(infn, outfn, dist)

    #Population of large hamlets
    in_ras = dir+cc+"/pop/"+cc+"_ppp_2020_constrained.tif"
    in_vec = dir+cc+"/comms/"+cc+"_hambig_b.shp"
    zonal(in_ras,in_vec)

    #Merge all settlements
    buassa = dir+cc+"/comms/"+cc+"_buassa_b.shp"
    ham = dir+cc+"/comms/"+cc+"_hambig_b.shp"
    layers = [buassa, ham]
    outfn=dir+cc+"/comms/"+cc+"_comms_b.shp"
    mergelayers(layers, outfn)