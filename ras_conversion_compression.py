import rasterio
import rioxarray as rxr
import os
import geopandas as gpd
from shapely.geometry import mapping
import topojson as tp
from rasterio.features import shapes

#os.chdir(os.path.dirname(os.path.abspath(__file__))) #Set working directory to the folder where the script is saved.

#########Set Variables########
#Varibale-specific variables
cc = 'gha'  #country code
var = 'edW'  #variable name
ras_filename = 'IHME_EDU_W_00-17.tif'  #global raster
shp_filename = 'GHA_adm0.shp'  #country mask

#Global variables
datasets_dir = 'datasets'
glob_dir = 'global'

#Define paths
ras_path = os.path.join(datasets_dir + '/' + glob_dir + '/' + ras_filename)
var_path = os.path.join('./' + datasets_dir + '/' + cc + '/' + var + '/')
shp_path = os.path.join(datasets_dir + '/' + cc + '/' + shp_filename)


########Clip raster########
#Open raster
ras = rxr.open_rasterio(ras_path)

# Open crop extent (your study area extent boundary)
crop_extent = gpd.read_file(shp_path)
# print('crop extent crs: ', crop_extent.crs)
# print('raster crs: ', ras.rio.crs)

#Clip raster
ras_clipped = ras.rio.clip(crop_extent.geometry.apply(mapping))
                                      # This is needed if your GDF is in a diff CRS than the raster data
                                      # crop_extent.crs)

# Write to new geotiff file
ras_clipped.rio.to_raster(var_path + cc + '_' + var + '.tif')

if var=="edW":
    band=18
else:
    band=1

########Convert to GeoJSON########
with rasterio.Env():
    with rasterio.open(var_path + cc + '_' + var + '.tif') as src:
        image = src.read(band) # first band
        mask = image >=0
        results = (
        {'properties': {'val': v}, 'geometry': s}
        for i, (s, v) 
        in enumerate(
            shapes(image, mask=mask, transform=src.transform)))
 
geoms = list(results)

#Convert to GeoDataFrame
gpd_polygonized_raster  = gpd.GeoDataFrame.from_features(geoms)

#Write to GeoJSON file (optional)
gpd_polygonized_raster.to_file(var_path + cc + '_' + var + '.json', driver='GeoJSON')


########Compress GeoJSON########
#Simplify GeoDataFrame
topo = tp.Topology(gpd_polygonized_raster, 
                   prequantize=False, 
                   topology=True, 
                   toposimplify=100, 
                   simplify_with='simplification', 
                   simplify_algorithm='vw',
                   prevent_oversimplify=True)

#Write to TopoJSON file
topo.to_json(var_path + cc + '_' + var + '.topo.json')

# #Plot to test resolution
# topo_load = gpd.read_file(var_path + cc + '_' + var + '.topo.json')
# topo_load.plot()

