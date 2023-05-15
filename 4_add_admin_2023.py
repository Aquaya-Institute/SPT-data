#Map generation SOP
from qgis.core import *
import qgis.utils
import processing
import os # This is is needed in the pyqgis console also

dir = "/Users/karastuart/Dropbox (Aquaya)/WASHPaLS 2/PEFO/SPT-data/datasets/"   # UPDATE
directory = os.fsencode(dir)
cc = "gha"  # country code # UPDATE
var = "comms"   # variable name, select either 'pixel', 'dist', or 'prov'  # UPDATE
suffix = "" # UPDATE - leave blank unless this is a second subnational boundary of the same resolution (e.g., add health districts as well as admin disticts. In this case, add a suffix such as "_health" when running for health districts.)
dist = "adm2"   # UPDATE number to be 2 or 3 as needed

### Check that a spatial index exists, and create it
def spatialindex(in_fn):
    processing.run("native:createspatialindex", {'INPUT':in_fn})
infn = dir + cc + "/"+var+"/"+cc+"_multivariable_noadmin_"+var+suffix+".shp"
spatialindex(infn)

##### Set join function and predicate value per variable #####
if var == "pixel" or var == "comms":
    infn = dir + cc + "/dist/"+cc+"_"+dist+suffix+".shp"
    spatialindex(infn)
    def spatial_join(in_fn, join_fn, join_fields, out_fn):
        processing.run("native:joinattributesbylocation", {'INPUT':in_fn,\
        'JOIN':join_fn,'PREDICATE':[0],'JOIN_FIELDS':join_fields,'METHOD':2,\
        'DISCARD_NONMATCHING':False,'PREFIX':'','OUTPUT':out_fn})
    joinfn = dir + cc + "/dist/"+cc+"_"+dist+suffix+".shp"
elif var == "dist":
    infn = dir + cc + "/dist/"+cc+"_"+dist+suffix+".shp"
    spatialindex(infn)
    def spatial_join(in_fn, join_fn, join_fields, out_fn):
        processing.run("native:joinattributesbylocation", {'INPUT':in_fn,\
        'JOIN':join_fn,'PREDICATE':[2],'JOIN_FIELDS':join_fields,'METHOD':2,\
        'DISCARD_NONMATCHING':False,'PREFIX':'','OUTPUT':out_fn})
    joinfn = dir + cc + "/dist/"+cc+"_"+dist+suffix+".shp"
else:
    infn = dir + cc + "/prov/"+cc+"_"+dist+suffix+".shp"
    spatialindex(infn)
    def spatial_join(in_fn, join_fn, join_fields, out_fn):
        processing.run("native:joinattributesbylocation", {'INPUT':in_fn,\
        'JOIN':join_fn,'PREDICATE':[2],'JOIN_FIELDS':join_fields,'METHOD':2,\
        'DISCARD_NONMATCHING':False,'PREFIX':'','OUTPUT':out_fn})
    joinfn = dir + cc + "/prov/"+cc+"_"+dist+suffix+".shp"

##### Set remainder of parameters #####
infn = dir + cc + "/"+var+"/"+cc+"_multivariable_noadmin_"+var+suffix+".shp"

### UPDATE - select the line that includes the correct boundary level names + geometry
### there will be 1 or 2 boundary levels depending on the country
#join_fields = ['NAME_1','NAME_2','NAME_3']
#join_fields = ['NAME_1','NAME_2']
join_fields = ['ADM1_EN','ADM2_EN']
#join_fields = ['REGION','DISTRICT']
#join_fields = ['ADM1_FR','ADM2_FR','Nom']
#join_fields = ['ADM1_FR']
#join_fields = ['NAME_1']
outfn=dir + cc + "/"+var+"/"+cc+"_multivariable_"+var+suffix+".shp"

##### Run spatial join #####
spatial_join(infn, joinfn, join_fields, outfn)
