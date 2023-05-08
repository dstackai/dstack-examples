import os
from pathlib import Path

import gradio as gr
import torch
from huggingface_hub import snapshot_download
from transformers import pipeline

model_name = "databricks/dolly-v2-12b"

local_dir = f"./models/{model_name}"
if not Path(local_dir).exists() or len(os.listdir(local_dir)) == 0:
    snapshot_download(model_name, local_dir=local_dir)

generate_text = pipeline(model=local_dir, torch_dtype=torch.bfloat16, trust_remote_code=True,
                         device_map="auto")

theme = gr.themes.Monochrome(
    primary_hue="indigo",
    secondary_hue="blue",
    neutral_hue="slate",
    radius_size=gr.themes.sizes.radius_sm,
    font=[gr.themes.GoogleFont("Open Sans"), "ui-sans-serif", "system-ui", "sans-serif"],
)

with gr.Blocks(theme=theme) as demo:
    chatbot = gr.Chatbot()
    msg = gr.Textbox()
    clear = gr.Button("Clear")


    def user(user_message, history):
        return "", history + [[user_message, None]]


    def bot(history):
        history[-1][1] = generate_text(history[-1][0])[0]["generated_text"]
        return history


    msg.submit(user, [msg, chatbot], [msg, chatbot], queue=False).then(
        bot, chatbot, chatbot
    )
    clear.click(lambda: None, None, chatbot, queue=False)

if __name__ == "__main__":
    server_port = int(os.getenv("PORT_0")) if os.getenv("PORT_0") else None
    demo.launch(server_name="0.0.0.0", server_port=server_port)
