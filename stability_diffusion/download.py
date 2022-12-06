import argparse
import os

from stable_diffusion_inference.lit_model import create_text2image

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--variant", type=str, choices=["sd1", "sd2_base", "sd2_high"], default="sd1")
    args = parser.parse_args()
    create_text2image(os.environ.get("SD_VARIANT") or args.variant,
                      cache_dir=os.environ.get("SD_CHECKPOINTS_CACHE_DIR") or "checkpoints")
