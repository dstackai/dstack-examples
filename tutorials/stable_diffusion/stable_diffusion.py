import shutil

from diffusers import StableDiffusionPipeline


def main():
    _, cache_folder = StableDiffusionPipeline.from_pretrained("runwayml/stable-diffusion-v1-5",
                                                              return_cached_folder=True)
    # Copy the model from the cache folder (that uses symlinks) to a local dir (that doesn't use symlinks)
    shutil.copytree(cache_folder, "./models/runwayml/stable-diffusion-v1-5", dirs_exist_ok=True)


if __name__ == '__main__':
    main()
