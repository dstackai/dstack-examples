import os
from pathlib import Path

import gradio as gr
import torch
from diffusers import StableDiffusionPipeline
from huggingface_hub import snapshot_download

model_name = "runwayml/stable-diffusion-v1-5"

local_dir = f"./models/{model_name}"
if not Path(local_dir).exists() or len(os.listdir(local_dir)) == 0:
    snapshot_download(model_name, local_dir=local_dir, local_dir_use_symlinks=False)

pipe = StableDiffusionPipeline.from_pretrained(f"./models/{model_name}", local_files_only=True)
if torch.cuda.is_available():
    pipe = pipe.to("cuda")

with gr.Blocks() as demo:
    def infer(prompt):
        return pipe([prompt]).images


    with gr.Row():
        text = gr.Textbox(
            show_label=False,
            max_lines=1,
            placeholder="Enter your prompt!",
        ).style(container=False)
        btn = gr.Button("Generate image").style(full_width=False)

    gallery = gr.Gallery(
        show_label=False
    ).style(columns=[2], height="auto")

    text.submit(infer, inputs=text, outputs=[gallery])
    btn.click(infer, inputs=text, outputs=[gallery])

if __name__ == "__main__":
    demo.launch()
