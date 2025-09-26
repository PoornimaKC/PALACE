# main.py
import subprocess
import shutil
from pathlib import Path
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import FileResponse, JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import Request
import uuid
import json

ROOT = Path(__file__).parent.resolve()
UPLOADS = ROOT / "uploads"
RESULTS = ROOT / "results"
TEMPLATE_DIR = ROOT / "templates"

for p in (UPLOADS, RESULTS, TEMPLATE_DIR):
    p.mkdir(exist_ok=True)

app = FastAPI(title="VR180 Converter API")
app.mount("/static", StaticFiles(directory=str(ROOT / "static")), name="static")
templates = Jinja2Templates(directory=str(TEMPLATE_DIR))


def build_filters(effects: list[str]) -> str:
    filters = "split=2[original][copy];[copy]hflip[flipped];[original][flipped]hstack=inputs=2[vr]"

    chain = "[vr]"

    if "lens" in effects:
        filters += f";{chain}lenscorrection=k1=-0.3:k2=0.2[step1]"
        chain = "[step1]"

    if "color" in effects:
        filters += f";{chain}eq=brightness=0.05:contrast=1.2:saturation=1.3[step2]"
        chain = "[step2]"

    if "text" in effects:
        filters += f";{chain}drawtext=text='VR180 Demo':fontcolor=white:fontsize=24:x=10:y=H-th-10[step3]"
        chain = "[step3]"

    return filters.replace("[vr]", chain) if chain != "[vr]" else filters


def convert_video(input_path: str, output_path: str, effects: list[str]):
    ffmpeg_path = shutil.which("ffmpeg")
    if ffmpeg_path is None:
        raise RuntimeError("ffmpeg not found. Please install it in your environment.")

    filters = build_filters(effects)

    cmd = [
        ffmpeg_path,
        "-i", input_path,
        "-vf", filters,
        "-c:v", "libx264",
        "-crf", "20",
        "-preset", "fast",
        str(output_path),
    ]

    try:
        subprocess.run(cmd, capture_output=True, text=True, check=True)
        return {"status": "success", "output": str(output_path)}
    except subprocess.CalledProcessError as e:
        return {"status": "failed", "error": e.stderr}


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/convert")
async def convert(
    file: UploadFile = File(...),
    lens: bool = Form(False),
    color: bool = Form(False),
    text: bool = Form(False)
):
    job_id = uuid.uuid4().hex
    local_name = UPLOADS / f"{job_id}_{file.filename}"
    with open(local_name, "wb") as f:
        shutil.copyfileobj(file.file, f)

    output_path = RESULTS / f"{job_id}_vr180.mp4"

    # gather selected effects
    effects = []
    if lens:
        effects.append("lens")
    if color:
        effects.append("color")
    if text:
        effects.append("text")

    result = convert_video(str(local_name), output_path, effects)

    if result["status"] == "success":
        return FileResponse(output_path, filename=output_path.name, media_type="video/mp4")
    else:
        return JSONResponse(result, status_code=500)
