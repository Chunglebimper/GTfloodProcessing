import argparse
from generate import generate_func
import json

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Damage Assessment Training")
    parser.add_argument('--drawJSON',       action='store_true',  help='Enable script to draw given a json file')
    parser.add_argument('--json_root',      type=str,   required=False, help='Path to json dataset root directory')
    parser.add_argument('--tif2composite',  action='store_true',  help='Enable script to convert tif to composite png')
    parser.add_argument('--tif_root',       type=str,   required=False, help='Path to tif dataset root directory')
    parser.add_argument('--SIZE',           type=int, required=True, help='The desired size of the output images (downsizing)')
    args = parser.parse_args()


    generate_func(
        drawJSON=args.drawJSON,
        json_root=args.json_root,
        tif2composite=args.tif2composite,
        tif_root=args.tif_root,
        SIZE=args.SIZE
    )

