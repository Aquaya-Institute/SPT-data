# sanitation-planning-data
WASHPaLS Sanitation Planning Tool data treatment

## Generate TopoJSON for visualization

*check repository status using 'git status' prior to making any changes on your local machine*

#### 1. Create file tree for countries/variables you plan to treat

Use consistent naming convention:

* 3 letter country codes: https://www.iban.com/country-codes
    
* Variable codes: timecities, od, edW, dia

#### 2. If variable <5km resolution, first resample: 

    ras_resample.py
    
#### 3. To clip to country, convert to TopoJSOn and compress (choose based on input file type):

    ras_conversion_compression.py *data layers*
    
    shp_conversion_compression.py *admin boundaries*

## Merge data to for composite community/polygon filtering

    *incomplete* aggregator.py
