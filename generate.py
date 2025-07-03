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

GLOBAL_count = 1

def send_to_dir(prefix, fname):
    """
    :param prefix:  str Should be either 'gt' or 'img'
    :param fname:   str Name to check for words post or pre
    :return:        str The directory to send file to
    """
    save_dir = None
    for word in fname.split('_'):
        if word == 'post':
            save_dir = f'data/{prefix}_post'
        elif word == 'pre':
            save_dir = f'data/{prefix}_pre'
    return save_dir


def generate_func(drawJSON, json_root, tif2composite, tif_root, SIZE):
    global GLOBAL_count
    for newDir in ('./data', './data/gt_post', './data/gt_pre', './data/img_post', './data/img_pre'):
        os.makedirs(newDir, exist_ok=True)

    if drawJSON:
        for fname in os.listdir(json_root):
            temp_str = f'{GLOBAL_count:>5} Saving {fname}...'
            print(f'{temp_str:<70}', end="", flush=True)
            # Handle save path
            save_path = os.path.join(send_to_dir('gt', fname), f'{fname[:-5]}_target.png')

            data = load(os.path.join(json_root, fname))
            try:
                features = data['features']['xy']

                # fig = figure_object, ax = axes_object for indexing subplots
                fig, ax = plt.subplots(dpi=100, figsize=(10.24, 10.24),  )
                fig.set_facecolor("#000000") # default is 255/ #FFFFFF which causes an error

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
                        'major-damage': '#030303',
                        'destroyed': '#040404',
                    }.get(level_of_destruction, '#000000')  # Default to black if level_of_destruction is invalid

                    # Create patch with color handling from above
                    patch = patches.Polygon(coords, closed=True, edgecolor=color, facecolor=color, fill=True,
                                            linewidth=0, aa=False, rasterized=True)

                    ax.add_patch(patch)

                ax.axis('off')
                plt.subplots_adjust(left=0, right=1, top=1, bottom=0)  # remove padding
                plt.savefig("buffer.png", bbox_inches='tight', pad_inches=0)
                plt.close(fig)

                # open with opencv to resize and then with rasterio save
                img = cv2.imread('buffer.png')
                img = skimage.transform.resize(img,
                                               (SIZE, SIZE),
                                               mode='edge',
                                               anti_aliasing=False,
                                               anti_aliasing_sigma=None,
                                               preserve_range=True,
                                               order=0)
                cv2.imwrite('buffer.png', img)

                with rasterio.open('buffer.png') as src:
                    img = src.read(1).squeeze()
                    classCount = np.unique(img)
                    Image.fromarray(img).save(save_path)
                    os.remove("buffer.png")

                print(f'Saved!\tClasses: {classCount}')

            except KeyError as e:
                image = np.zeros((SIZE, SIZE), dtype=np.uint8)
                Image.fromarray(image).save(save_path)
                print(">         Feature was not loaded properly OR no polygons to draw; saved GT with all zeros")
                #print(f"------- ERROR with file {fname}: {e} -------\n"
                      #f"\t> Features were not loaded properly\n"
                      #f"\tfeature = data1['features']['xy']\n"
                      #f"\tlevel_of_destruction = feature['properties']['subtype']\n"
                      #f"\twkt_str = feature['wkt']\n",
                      #86*"^")
            finally:
                GLOBAL_count += 1

        print("drawJSON complete")

    if tif2composite:
        GLOBAL_count = 0
        for fname in os.listdir(tif_root):  # inside directory
            temp_str = f'{GLOBAL_count:>5} Saving {fname}...'
            print(f'{temp_str:<70}', end="", flush=True)

            tiff_file = os.path.join(tif_root, fname)
            # Handle save path
            save_path = os.path.join(send_to_dir('img', fname), f'{fname[:-4]}.png')
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