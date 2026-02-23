from __future__ import annotations

import base64
import io
from typing import Optional

from fastapi import FastAPI, File, Form, Request, UploadFile
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from PIL import Image

app = FastAPI(title="Printable Doc Studio")
templates = Jinja2Templates(directory="app/templates")
app.mount("/static", StaticFiles(directory="app/static"), name="static")

PAPER_PRESETS = {
    "A4": {"width_mm": 210, "height_mm": 297},
    "A5": {"width_mm": 148, "height_mm": 210},
}


@app.get("/", response_class=HTMLResponse)
async def home(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(
        request,
        "index.html",
        {
            "paper_presets": PAPER_PRESETS,
            "background_presets": ["纯白", "米白", "网格", "横线"],
            "style_presets": ["简洁", "商务", "柔和"],
        },
    )


@app.post("/api/generate")
async def generate_preview(
    text: str = Form(""),
    paper_size: str = Form("A4"),
    background_style: str = Form("纯白"),
    visual_style: str = Form("简洁"),
    image: Optional[UploadFile] = File(default=None),
) -> JSONResponse:
    paper = PAPER_PRESETS.get(paper_size, PAPER_PRESETS["A4"])

    image_data = None
    image_meta = None

    if image and image.filename:
        raw = await image.read()
        if raw:
            pil_image = Image.open(io.BytesIO(raw))
            pil_image.thumbnail((1200, 1200))
            out = io.BytesIO()
            pil_image.save(out, format="PNG")
            image_data = base64.b64encode(out.getvalue()).decode("utf-8")
            image_meta = {
                "name": image.filename,
                "width": pil_image.width,
                "height": pil_image.height,
            }

    return JSONResponse(
        {
            "paper": paper,
            "paper_size": paper_size,
            "background_style": background_style,
            "visual_style": visual_style,
            "text": text,
            "image_data": image_data,
            "image_meta": image_meta,
        }
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
