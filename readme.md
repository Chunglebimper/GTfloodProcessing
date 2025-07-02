# GTfloodProcessing
This repository is meant to process the flood data GT .json files from the xBD dataset, however with some modifications, the scripts can also apply to any GT json file labelled with polygons.
**This repository will output the data at the specififed size and will generate folders for new results.**

The code expects a certain form of the .json file and will print images mapped with all zeroes.

Console commands should take the form:
```commandline
python main.py --drawJSON --json_root '/home/user/samples/json_folder' --tif2composite --tif_root '/home/user/samples/tif_folder' --SIZE 512
python main.py --json_root '/home/user/samples/json_folder' --tif2composite --tif_root '/home/user/samples/tif_folder' --SIZE 512
```


# Reading the .json
When generate.py is reading the .json files, the form is assumed to be the following:
~~~
features = data['features']['xy']  # items of interest 
level_of_destruction = feature['properties']['subtype']
wkt_str = feature['wkt']  # coords to be loaded and drawn
~~~

Intended data to use: https://xview2.org/dataset

Author: https://github.com/Chunglebimper