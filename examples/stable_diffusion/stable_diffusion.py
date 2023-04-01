from huggingface_hub import snapshot_download

if __name__ == '__main__':
    snapshot_download("runwayml/stable-diffusion-v1-5", local_dir="./models/runwayml/stable-diffusion-v1-5")
