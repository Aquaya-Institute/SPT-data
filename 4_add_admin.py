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

def spatial_join(in_fn, join_fn, join_fields, out_fn):
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
spatial_join(infn, joinfn, join_fields, outfn)
