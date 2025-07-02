import os
import rasterio
import cv2
import skimage
from shapely import wkt
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from rasterio.plot import show
import numpy as np
from PIL import Image, ImageSequence
from utils import load

GLOBAL_count = 0

def generate_func(drawJSON, json_root, tif2composite, tif_root, SIZE):
    global GLOBAL_count
    for newDir in ('./OUPUTfromJson', './OUTPUTfromTif'):
        os.makedirs(newDir, exist_ok=True)

    if drawJSON:
        for fname in os.listdir(json_root):
            temp_str = f'{GLOBAL_count} Saving {fname}...'
            print(f'{temp_str:<70}', end="")
            save_path = os.path.join('OUPUTfromJson', f'{fname[:-4]}png')
            data = load(os.path.join(json_root, fname))
            try:
                features = data['features']['xy']

                # fig = figure_object, ax = axes_object for indexing subplots
                fig, ax = plt.subplots(dpi=100, figsize=(10.24, 10.24), )

                # For every feature get the class and coordinates for plotting
                for feature in features:
                    level_of_destruction = feature['properties']['subtype']
                    wkt_str = feature['wkt']
                    polygon = wkt.loads(wkt_str)
                    coords = [(x, y) for x, y in polygon.exterior.coords]

                    # Use rasterio to show the image with correct orientation
                    show(np.zeros((1024, 1024)), ax=ax, cmap='gray')

                    # Add polygon overlay and determine color of edge
                    color = {
                        'no-damage': '#010101',
                        'minor-damage': '#020202',
                        'moderate-damage': '#030303',
                        'major-damage': '#040404',
                        'destroyed': '#050505',
                    }.get(level_of_destruction, '#000000')  # Default to black if level_of_destruction is invalid

                    # Create patch with color handling from above
                    patch = patches.Polygon(coords, closed=True, edgecolor=color, facecolor=color, fill=True,
                                            linewidth=0, aa=False, rasterized=True)

                    ax.add_patch(patch)

                ax.axis('off')
                plt.subplots_adjust(left=0, right=1, top=1, bottom=0)  # remove padding
                plt.savefig("buffer0.png", bbox_inches='tight', pad_inches=0)
                plt.close(fig)

                with rasterio.open('buffer0.png') as src:
                    image = src.read()
                    image = np.delete(image, obj=[1, 2, 3], axis=0)
                    image = src.read(1).squeeze()
                    # image = (255 * (image / image.max())).astype('uint8')  # Normalize for display
                    Image.fromarray(image).save('buffer1.png')
                    img = cv2.imread('buffer1.png')
                    out = skimage.transform.resize(img,
                                                   (SIZE, SIZE),
                                                   mode='edge',
                                                   anti_aliasing=False,
                                                   anti_aliasing_sigma=None,
                                                   preserve_range=True,
                                                   order=0)
                    cv2.imwrite(save_path, out)
                    os.remove("buffer0.png")
                    os.remove("buffer1.png")
                print(f'Saved!')

            except KeyError as e:
                image = np.zeros((SIZE, SIZE), dtype=np.uint8)
                Image.fromarray(image).save(save_path)
                print("> Features were not loaded properly; saving GT with all zeros")
                #print(f"------- ERROR with file {fname}: {e} -------\n"
                      #f"\t> Features were not loaded properly\n"
                      #f"\tfeature = data['features']['xy']\n"
                      #f"\tlevel_of_destruction = feature['properties']['subtype']\n"
                      #f"\twkt_str = feature['wkt']\n",
                      #86*"^")
            finally:
                GLOBAL_count += 1

        print("drawJSON complete")



    if tif2composite:
        GLOBAL_count = 0
        for fname in os.listdir(tif_root):  # inside directory
            temp_str = f'{GLOBAL_count} Saving {fname}...'
            print(f'{temp_str:<70}', end="")

            tiff_file = os.path.join(tif_root, fname)
            save_path = os.path.join('OUTPUTfromTif', f'{fname[:-4]}.png')
            try:
                with rasterio.open(tiff_file) as src:
                    image = src.read()
                    image_array = np.array(image)
                    image_array = np.transpose(image_array, (1, 2, 0))
                    image_array = (255 * (image_array / image_array.max())).astype(np.uint8)
                    composite_image = Image.fromarray(image_array, mode='RGB')
                    composite_image.save(save_path)

                    img = cv2.imread(save_path)
                    out = skimage.transform.resize(img,
                                                   (SIZE, SIZE),
                                                   mode='edge',
                                                   anti_aliasing=False,
                                                   anti_aliasing_sigma=None,
                                                   preserve_range=True,
                                                   order=0)
                    cv2.imwrite(save_path, out)
                    print(f'Saved!')

            except Exception as e:
                print("ERROR:", e)

            finally:
                GLOBAL_count += 1

    print("tif2composite complete")