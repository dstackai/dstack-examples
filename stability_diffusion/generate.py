import argparse
import os
from pathlib import Path

from stable_diffusion_inference import create_text2image

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--variant", choices=["sd1", "sd2_base", "sd2_high"], default="sd1")
    parser.add_argument("-S", "--size", type=int, default=512)
    parser.add_argument("-s", "--steps", type=int, default=1)
    parser.add_argument("-p", "--prompt", action='append', required=True)
    args = parser.parse_args()
    text2image = create_text2image(args.variant, cache_dir="checkpoints")
    image = text2image(args.prompt, args.size, args.steps)
    output_path = Path("output")
    output_path.mkdir(parents=True, exist_ok=True)
    image.save(output_path / f"{(os.environ.get('RUN_NAME') or 'image')}.png")
