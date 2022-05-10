#Map generation SOP
from qgis.core import *
import qgis.utils
import processing
import os # This is is needed in the pyqgis console also
dir = "/Users/karastuart/Dropbox (Aquaya)/WASHPaLS_RProjects/PEFO/SPT-data/datasets/" #UPDATE
directory = os.fsencode(dir)
cc = "npl" #UPDATE
var = "pixel"
dist = "adm2"

def clip(in_fn, join_fn, overlay, out_fn):
    processing.run("native:clip", {'INPUT': in_fn,'OVERLAY':overlay,'OUTPUT':out_fn})
infn = dir + cc + "/comms/"+cc+"_multivariable_comms.shp"
overlay = dir + cc + "/country/"+cc+"_adm0.shp"
outfn=dir + cc + "/"+var+"/"+cc+"_multivariable_comms_clip.shp"
clip(infn, overlay, outfn)

def centroid(in_fn, join_fn, overlay, out_fn):
    processing.run("native:centroids", {'INPUT':'memory://MultiPolygon?crs=EPSG:4326&field=timecities:double(23,15)&field=dr:double(23,15)&field=dt:double(23,15)&field=classes:double(23,15)&field=rr:double(23,15)&field=rrd:double(23,15)&field=rm:double(23,15)&field=u:double(23,15)&field=pop:double(23,15)&field=NAME_1:string(75,0)&field=NAME_2:string(75,0)&field=NAME_3:string(75,0)&field=id:integer(10,0)&uid={caf22611-1c69-4d3e-b790-98d826df084d}','ALL_PARTS':False,'OUTPUT':'TEMPORARY_OUTPUT'})
infn = dir + cc + "/"+var+"/"+cc+"_multivariable_noadmin_"+var+".shp"
overlay = dir + cc + "/dist/"+cc+"_"+dist+".shp"
outfn=dir + cc + "/"+var+"/"+cc+"_multivariable_"+var+".shp"
clip(infn, overlay, outfn)

def spatial_join(in_fn, join_fn, join_fields, out_fn):
    processing.run("native:joinattributesbylocation", {'INPUT':in_fn,\
    'JOIN':join_fn,'PREDICATE':[0],'JOIN_FIELDS':join_fields,'METHOD':2,\
    'DISCARD_NONMATCHING':False,'PREFIX':'','OUTPUT':out_fn})
infn = dir + cc + "/"+var+"/"+cc+"_multivariable_noadmin_"+var+".shp"
joinfn = dir + cc + "/dist/"+cc+"_"+dist+".shp"
join_fields = ['ADM1_EN','ADM2_EN']
outfn=dir + cc + "/"+var+"/"+cc+"_multivariable_"+var+".shp"
spatial_join(infn, joinfn, join_fields, outfn)

def column_join(in_fn, join_fn, join_fields, out_fn):
    processing.run("native:joinattributesbylocation", {'INPUT':in_fn,\
    'JOIN':join_fn,'PREDICATE':[0],'JOIN_FIELDS':join_fields,'METHOD':2,\
    'DISCARD_NONMATCHING':False,'PREFIX':'','OUTPUT':out_fn})
infn = dir + cc + "/"+var+"/"+cc+"_multivariable_noadmin_"+var+".shp"
joinfn = dir + cc + "/dist/"+cc+"_"+dist+".shp"
#join_fields = ['NAME_1','NAME_2','NAME_3']
#join_fields = ['NAME_1','NAME_2']
join_fields = ['ADM1_EN','ADM2_EN']
#join_fields = ['REGION','DISTRICT']
outfn=dir + cc + "/"+var+"/"+cc+"_multivariable_"+var+".shp"
column_join(infn, joinfn, join_fields, outfn)
