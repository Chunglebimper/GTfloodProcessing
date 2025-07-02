# GTfloodProcessing Overview
This repository is meant to process the .json and .tif files files from the xBD dataset, however with some modifications, the scripts can also apply to any GT json file labelled with polygons.
**This repository will output the data at the specififed size  and will generate folders gt_post, gt_pre, img_post, and img_pre for corresponding data.**

The code expects a certain form of the .json file and will print images mapped with all zeroes as an exception.

Console commands should take the form:
```commandline
python main.py --drawJSON --json_root '/home/user/samples/json_folder' --SIZE 512
python main.py --tif2composite --tif_root '/home/user/samples/tif_folder' --SIZE 512
# or both at the same time
python main.py --drawJSON --json_root '/home/user/samples/json_folder' --tif2composite --tif_root '/home/user/samples/tif_folder' --SIZE 512
```
Details
-
- --SIZE is meant for downscaling rather than upscaling
- When a .json file is loaded to draw, there may not always be buildings present in the image which are represented as polygons. Therefore if no polygons are present, a black image is drawn with classes representing the background class
- The dataset used, expects classes with specific names, otherwise errors will arise
- It is recommended that you clean the output data after running the raw data through this program
___________________________
## Reading the .json
When generate.py is reading the .json files, the form is assumed to be the following:
~~~
features = data['features']['xy']  # items of interest 
level_of_destruction = feature['properties']['subtype']
wkt_str = feature['wkt']  # coords to be loaded and drawn
~~~

level_of_destruction must correspond to one of the keys listed otherwise #000000 is drawn
~~~
# Add polygon overlay and determine color of edge
                    color = {
                        'no-damage': '#010101',
                        'minor-damage': '#020202',
                        'moderate-damage': '#030303',
                        'major-damage': '#040404',
                        'destroyed': '#050505',
                    }.get(level_of_destruction, '#000000')  # Default to black if level_of_destruction is invalid
~~~
________________________
Intended data to use: https://xview2.org/dataset

Author: https://github.com/Chunglebimper