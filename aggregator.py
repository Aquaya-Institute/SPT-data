import h3
import os
import json
import pandas as pd
from shapely.geometry import Point, Polygon
os.chdir(os.path.dirname(os.path.abspath(__file__))) #Set working directory to the folder where the script is saved.

#########Set Variables########
#Varibale-specfic variables
cc = 'gha'  #country code
var = 'timecities'  #variable name
json_filename = 'gha_timecities.json' 
dist_filename = 'gha_dist.json' 

#Global variables
datasets_dir = 'datasets'
dist_dir = 'dist'

#Define paths
map_path = os.path.join('./' + datasets_dir + '/' + cc + '/' + var + '/' + json_filename)
var_path = os.path.join('./' + datasets_dir + '/' + cc + '/' + var + '/')
data_path = os.path.join('./' + datasets_dir + '/' + cc + '/' + dist_dir + '/' + dist_filename)


# measure = 'od'
mapping = json.load(open(map_path))
data = json.load(open(data_path))

df = pd.DataFrame(data['features'])
length = len(df)
processed = 0

for feature_idx in range(length):
    feature = df.loc[feature_idx]
    geo = feature.geometry

    coordinates = geo['coordinates'][0][0]
    poly = Polygon(coordinates)

    sum_of_vals = 0
    count = 0

    for pid in mapping:
        pixel = mapping[hid]
        lat = pixel['lat']
        lng = pixel['lng']
        val = pixel['val']

        p = Point(lat, lng)
        contained = poly.contains(p)
        if contained == True:
            sum_of_vals += val
            count += 1

            print(feature['properties']['DISTRICT'])
            print(p)
            print(val)
            print(contained)

    processed += count
    
    metric_name = 'mean_' + var

    if count == 0:
        data['features'][feature_idx]['properties'][metric_name] = None
    else:
        data['features'][feature_idx]['properties'][metric_name] = sum_of_vals / count #add average to geojson

print('done')
print(processed)

json_object = json.dumps(data, indent=1)
  
with open('./res.geojson', 'w') as dset_f: 
    dset_f.write(json_object)