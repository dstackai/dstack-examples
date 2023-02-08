import argparse
from pathlib import Path

import torch
from diffusers import StableDiffusionPipeline

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-P", "--prompt", action='append', required=True)
    args = parser.parse_args()

    pipe = StableDiffusionPipeline.from_pretrained("./models/runwayml/stable-diffusion-v1-5", local_files_only=True)
    if torch.cuda.is_available():
        pipe.to("cuda")
    images = pipe(args.prompt).images

    output = Path("./output")
    output.mkdir(parents=True, exist_ok=True)
    for i in range(len(images)):
        images[i].save(output / f"{i}.png")
