#Map generation SOP
from qgis.core import *
import qgis.utils
from qgis.utils import iface
import processing
import os # This is is needed in the pyqgis console also
os.environ["PROJ_LIB"]="/Applications/QGIS.app/Contents/Resources/proj"

dir = "/Users/karastuart/Dropbox (Aquaya)/WASHPaLS_RProjects/PEFO/SPT-data/datasets/" #UPDATE
directory = os.fsencode(dir)
cc = "ken" #UPDATE

####Get Country Extent (deg)
country = QgsVectorLayer(dir+cc+"/country/"+cc+"_adm0.shp", cc+"_country", "ogr")
QgsProject.instance().addMapLayer(country)
country = iface.activeLayer()

ext = country.extent()
xmin = ext.xMinimum()
xmax = ext.xMaximum()
ymin = ext.yMinimum()
ymax = ext.yMaximum()
coords = "%f,%f,%f,%f" %(xmin, xmax, ymin, ymax) # this is a string that stores the coordinates
extent = coords+' [EPSG:4326]'
QgsProject.instance().removeMapLayer(country)

####Get Country Extent (m)
#Reproject for geometric units
def reproject(in_fn, out_fn, crs):
    processing.run("native:reprojectlayer", {'INPUT':in_fn,\
    'TARGET_CRS':crs,
    'OPERATION':'+proj=pipeline +step +proj=unitconvert +xy_in=deg +xy_out=rad +step +proj=webmerc +lat_0=0 +lon_0=0 +x_0=0 +y_0=0 +ellps=WGS84',\
    'OUTPUT':out_fn})
infn = dir+cc+"/country/"+cc+"_adm0.shp"
outfn = dir+cc+"/country/"+cc+"_adm0p.shp"
crs = QgsCoordinateReferenceSystem('EPSG:3857')
reproject(infn, outfn, crs)

country = QgsVectorLayer(dir+cc+"/country/"+cc+"_adm0p.shp", cc+"_country", "ogr")
QgsProject.instance().addMapLayer(country)
country = iface.activeLayer()

ext = country.extent()
xmin = ext.xMinimum()
xmax = ext.xMaximum()
ymin = ext.yMinimum()
ymax = ext.yMaximum()
coords = "%f,%f,%f,%f" %(xmin, xmax, ymin, ymax) # this is a string that stores the coordinates
extent_p = coords+' [EPSG:3857]'
QgsProject.instance().removeMapLayer(country)

####ROADS
#Extract cat 1-3 roads
#Select 1-3 roads, save as
def extract_roads(in_fn, out_fn, exp):
    processing.run("native:extractbyexpression", {'INPUT':in_fn,\
    'EXPRESSION':exp,\
    'OUTPUT':out_fn})
infn = dir + cc + "/roads/hotosm_"+cc+"_roads_lines.shp"
outfn=dir + cc + "/roads/"+cc+"_roads_123.shp"
exp = ' \"highway\" = \'primary\' OR  \"highway\" = \'secondary\' OR  \"highway\" = \'tertiary\' OR  \"highway\" = \'trunk\' OR  \"highway\" = \'primary_link\' OR  \"highway\" = \'secondary_link\' OR  \"highway\" = \'tertiary_link\' OR  \"highway\" = \'trunk_link\' '
extract_roads(infn, outfn, exp)

#Reproject for geometric units
def reproject(in_fn, out_fn, crs):
    processing.run("native:reprojectlayer", {'INPUT':in_fn,\
    'TARGET_CRS':crs,'OPERATION':'+proj=pipeline +step +proj=unitconvert +xy_in=deg +xy_out=rad +step +proj=webmerc +lat_0=0 +lon_0=0 +x_0=0 +y_0=0 +ellps=WGS84',\
    'OUTPUT':out_fn})
filename = os.fsdecode(cc+"/roads/"+cc+"_roads_123.shp")
outfn = dir + cc + "/roads/"+cc+"_roads_123p.shp"
infn = os.path.join(os.fsdecode(directory),filename)
crs = QgsCoordinateReferenceSystem('EPSG:3857')
reproject(infn, outfn, crs)

#Rasterize
def rasterize_roads(in_fn, out_fn, extent_temp):
    processing.run("gdal:rasterize", {'INPUT':in_fn,\
    'FIELD':'','BURN':1,'UNITS':1,'WIDTH':200,'HEIGHT':200,\
    'EXTENT':extent_temp,\
    'NODATA':None,'OPTIONS':'','DATA_TYPE':5,'INIT':None,'INVERT':False,'EXTRA':'',\
    'OUTPUT':out_fn})
filename = os.fsdecode(cc+"/roads/"+cc+"_roads_123p.shp")
outfn = dir + cc + "/roads/"+cc+"_roads_123p.tif"
infn=os.path.join(os.fsdecode(directory),filename)
extent_temp = extent_p
rasterize_roads(infn, outfn, extent_temp)

#Proximity
def prox_roads(in_fn, out_fn, max):
    processing.run("gdal:proximity", {'INPUT':in_fn,\
    'BAND':1,'VALUES':'','UNITS':0,'MAX_DISTANCE':None,'REPLACE':None,'NODATA':None,'OPTIONS':'','EXTRA':'','DATA_TYPE':2,\
    'OUTPUT':out_fn})
infn= dir + cc + "/roads/"+cc+"_roads_123p.tif"
outfn = dir + cc + "/distroads/"+cc+"_distroadsp.tif"
max='None'
prox_roads(infn, outfn, max)

def assign_crs(in_fn):
    processing.run("gdal:assignprojection", {'INPUT':in_fn,'CRS':QgsCoordinateReferenceSystem('EPSG:3857')})
infn = dir + cc + "/distroads/"+cc+"_distroadsp.tif"
assign_crs(infn)

#Warp
def warp(in_fn, out_fn, crs):
    processing.run("gdal:warpreproject", {'INPUT':in_fn,\
    'SOURCE_CRS':None,'TARGET_CRS':crs,\
    'RESAMPLING':0,'NODATA':None,'TARGET_RESOLUTION':None,'OPTIONS':'','DATA_TYPE':0,'TARGET_EXTENT':None,\
    'TARGET_EXTENT_CRS':None,'MULTITHREADING':False,'EXTRA':'','OUTPUT':out_fn})
infn = dir + cc + "/distroads/"+cc+"_distroadsp.tif"
outfn = dir + cc + "/distroads/"+cc+"_distroads.tif"
crs = QgsCoordinateReferenceSystem('EPSG:4326')
warp(infn, outfn, crs)

####TOWNS
#Reproject
infn=dir + cc + "/disttowns/"+cc+"_towns.shp"
outfn = dir + cc + "/disttowns/"+cc+"_townsp.shp"
crs=QgsCoordinateReferenceSystem('EPSG:3857')
reproject(infn, outfn, crs)
    
#Rasterize
def rasterize_towns(in_fn, out_fn, extent_temp):
    processing.run("gdal:rasterize", {'INPUT':in_fn,\
    'FIELD':'','BURN':1,'UNITS':1,'WIDTH':200,'HEIGHT':200,\
    'EXTENT':extent_temp,\
    'NODATA':None,'OPTIONS':'','DATA_TYPE':5,'INIT':None,'INVERT':False,'EXTRA':'',\
    'OUTPUT':out_fn})
infn=dir + cc + "/disttowns/"+cc+"_townsp.shp"
outfn = dir + cc + "/disttowns/"+cc+"_townsp.tif"
extent_temp = extent_p
rasterize_towns(infn, outfn, extent_temp)
    
#Proximity
def prox_towns(in_fn, out_fn, max):
    processing.run("gdal:proximity", {'INPUT':in_fn,\
    'BAND':1,'VALUES':'','UNITS':0,'MAX_DISTANCE':max,'REPLACE':None,'NODATA':None,'OPTIONS':'','EXTRA':'','DATA_TYPE':5,\
    'OUTPUT':out_fn})
infn=dir + cc + "/disttowns/"+cc+"_townsp.tif"
outfn = dir + cc + "/disttowns/"+cc+"_disttownsp.tif"
max=None
prox_towns(infn, outfn, max)

infn = dir + cc + "/disttowns/"+cc+"_disttownsp.tif"
assign_crs(infn)

#Warp
infn = dir + cc + "/disttowns/"+cc+"_disttownsp.tif"
outfn = dir + cc + "/disttowns/"+cc+"_disttowns.tif"
crs = QgsCoordinateReferenceSystem('EPSG:4326')
warp(infn, outfn, crs)

####CITIES
#Reproject
infn=dir + cc + "/disttowns/"+cc+"_cities.shp"
outfn = dir + cc + "/disttowns/"+cc+"_citiesp.shp"
crs=QgsCoordinateReferenceSystem('EPSG:3857')
reproject(infn, outfn, crs)
    
#Rasterize
infn=dir + cc + "/disttowns/"+cc+"_citiesp.shp"
outfn = dir + cc + "/disttowns/"+cc+"_citiesp.tif"
extent_temp = extent_p
rasterize_towns(infn, outfn, extent_temp)

#Warp
infn = dir + cc + "/disttowns/"+cc+"_citiesp.tif"
outfn = dir + cc + "/disttowns/"+cc+"_cities.tif"
crs = QgsCoordinateReferenceSystem('EPSG:4326')
warp(infn, outfn, crs)

####TIME TO CITIES
def cliplayer(in_fn, out_fn, masklayer):
    processing.run("gdal:cliprasterbymasklayer", {'INPUT': in_fn,'MASK':masklayer,\
    'SOURCE_CRS':None,'TARGET_CRS':None,'NODATA':None,'ALPHA_BAND':False,'CROP_TO_CUTLINE':True,\
    'KEEP_RESOLUTION':False,'SET_RESOLUTION':False,'X_RESOLUTION':None,'Y_RESOLUTION':None,\
    'MULTITHREADING':False,'OPTIONS':'','DATA_TYPE':0,'EXTRA':'','OUTPUT':out_fn})
infn = dir + "/global/MAP_timecities.tif"
outfn=dir + cc + "/timecities/"+cc+"_timecities.tif"
masklayer = dir + cc + "/country/"+cc+"_adm0.shp"
cliplayer(infn, outfn, masklayer)

####CLASSIFICATION
#Raster calculator
def rastercalc_class(out_fn, exp, layers, extent_temp):
    processing.run("qgis:rastercalculator", {'EXPRESSION':exp,\
    'LAYERS':layers,'CELLSIZE':None,\
    'EXTENT':extent_temp,'CRS':None,\
    'OUTPUT':out_fn})


disttowns = QgsRasterLayer(dir + cc + "/disttowns/"+cc+"_disttowns.tif","disttowns")
timecities = QgsRasterLayer(dir + cc + "/timecities/"+cc+"_timecities.tif","timecities")
distroads = QgsRasterLayer(dir + cc + "/distroads/"+cc+"_distroads.tif","distroads")
cities = QgsRasterLayer(dir + cc + "/disttowns/"+cc+"_cities.tif","cities")
outfn = dir + cc + "/class/"+cc+"_class_nc.tif"
QgsProject.instance().addMapLayer(disttowns)
QgsProject.instance().addMapLayer(distroads)
QgsProject.instance().addMapLayer(timecities)
QgsProject.instance().addMapLayer(cities)
layers = [timecities]
extent_temp = extent
exp = '(\"cities@1\" > 0 OR \"timecities@1\"<= 10)*4+(( \"cities@1\" < 1 AND \"timecities@1\">10) AND (\"disttowns@1\" <= 800 OR \"timecities@1\" <= 25))*3+((\"cities@1\" < 1) AND (\"disttowns@1\" > 800 AND \"timecities@1\">25) AND \"distroads@1\" <= 1500)*2+((\"cities@1\" < 1) AND (\"disttowns@1\" > 800 AND \"timecities@1\">25) AND \"distroads@1\" > 1500)*1'
rastercalc_class(outfn, exp, layers, extent_temp)
QgsProject.instance().removeMapLayer(disttowns)
QgsProject.instance().removeMapLayer(distroads)
QgsProject.instance().removeMapLayer(timecities)
QgsProject.instance().removeMapLayer(cities)

#Clip
infn = dir + cc + "/class/"+cc+"_class_nc.tif"
outfn=dir + cc + "/class/"+cc+"_class.tif"
masklayer = dir + cc + "/country/"+cc+"_adm0.shp"
cliplayer(infn, outfn, masklayer)

iface.addRasterLayer(dir + cc + "/class/"+cc+"_class.tif","class")

def polygonize(in_fn, out_fn):
    processing.run("gdal:polygonize", {'INPUT':in_fn,\
    'BAND':1,'FIELD':'classes','EIGHT_CONNECTEDNESS':False,'EXTRA':'',\
    'OUTPUT':out_fn})
infn = dir + cc + "/class/"+cc+"_class.tif"
outfn= dir + cc + "/class/"+cc+"_class.geojson"
polygonize(infn, outfn)