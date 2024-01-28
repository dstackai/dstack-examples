import asyncio
import uuid
from pathlib import Path
from typing import Optional

import PIL
import torch
from diffusers import DiffusionPipeline, StableDiffusionXLPipeline
from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel

base = StableDiffusionXLPipeline.from_pretrained(
    "stabilityai/stable-diffusion-xl-base-1.0",
    torch_dtype=torch.float16,
    variant="fp16",
    use_safetensors=True,
)
base.to("cuda")

refiner = None
refiner_lock = asyncio.Lock()

images_dir = Path("images")
images_dir.mkdir(exist_ok=True)

app = FastAPI()


class GenerateRequest(BaseModel):
    prompt: str
    negative_prompt: Optional[str] = None
    width: Optional[int] = None
    height: Optional[str] = None


class ImageResponse(BaseModel):
    id: str


class RefineRequest(BaseModel):
    id: str
    prompt: str


@app.post("/generate")
async def generate(request: GenerateRequest):
    image = base(
        prompt=request.prompt,
        negative_prompt=request.negative_prompt,
        width=request.width,
        height=request.height,
    ).images[0]
    id = str(uuid.uuid4())
    image.save(images_dir / f"{id}.png")
    return ImageResponse(id=id)


@app.post("/refine")
async def refine(request: RefineRequest):
    await refiner_lock.acquire()
    global refiner
    if refiner is None:
        refiner = DiffusionPipeline.from_pretrained(
            "stabilityai/stable-diffusion-xl-refiner-1.0",
            text_encoder_2=base.text_encoder_2,
            vae=base.vae,
            torch_dtype=torch.float16,
            use_safetensors=True,
            variant="fp16",
        )
        refiner.to("cuda")
    refiner_lock.release()

    image = refiner(
        prompt=request.prompt,
        image=PIL.Image.open(images_dir / f"{request.id}.png"),
    ).images[0]

    id = str(uuid.uuid4())
    image.save(images_dir / f"{id}.png")
    return ImageResponse(id=id)


@app.get("/download/{id}")
async def download(id: str):
    filename = f"{id}.png"
    return FileResponse(
        images_dir / filename, media_type="image/png", filename=filename
    )
