#Map generation SOP
from qgis.core import *
import qgis.utils
import processing
import os

dir = "/Users/karastuart/Dropbox (Aquaya)/WASHPaLS 2/PEFO/SPT-data/datasets/"   # UPDATE
directory = os.fsencode(dir)
cc = "lbr"  # country code # UPDATE


def spatialindex(in_fn):
    processing.run("native:createspatialindex", {'INPUT':in_fn})
infn = dir + cc + "/comms/"+cc+"_multivariable_comms.shp"
spatialindex(infn)

infn = dir + cc + "/pixel/"+cc+"_multivariable_noadmin_pixel.geojson"   # CHECK
spatialindex(infn)

##### REPEAT FOR EACH BOUNDARY LEVEL (incl. suffixes) #####
infn = dir + cc + "/dist/"+cc+"_multivariable_noadmin_dist.shp"   # CHECK
spatialindex(infn)

def column_join(in_fn, join_fn, join_fields, prefix, out_fn):
    processing.run("native:joinattributesbylocation", {'INPUT':in_fn,\
    'JOIN':join_fn,'PREDICATE':[0],'JOIN_FIELDS':join_fields,'METHOD':2,\
    'DISCARD_NONMATCHING':False,'PREFIX':prefix,'OUTPUT':out_fn})
infn = dir + cc + "/comms/"+cc+"_multivariable_comms.shp"
joinfn = dir + cc + "/pixel/"+cc+"_multivariable_noadmin_pixel.geojson"   # CHECK
join_fields = []
prefix = "p_"
outfn=dir + cc + "/comms/"+cc+"_multivariable_comms_join1.shp"
column_join(infn, joinfn, join_fields, prefix, outfn)

##### REPEAT FOR EACH BOUNDARY LEVEL #####
infn = dir + cc + "/comms/"+cc+"_multivariable_comms_join1.shp" # IF REPEATED, ADJUST FOR THE EXPORT OF PREVIOUS REPEAT
joinfn = dir + cc + "/dist/"+cc+"_multivariable_noadmin_dist.shp"   # CHECK
join_fields = []
prefix = "_d"   # CUSTOMIZE FOR EACH ADDED BOUNDARY LEVEL
outfn=dir + cc + "/comms/"+cc+"_multivariable_comms_join.shp"   # IF REPEATED, USE "_join2", etc. and keep "_join" for the file export
column_join(infn, joinfn, join_fields, prefix, outfn)
