# processing.py
import subprocess
from pathlib import Path

def _has_audio(input_path: str) -> bool:
    cmd = [
        "ffprobe", "-v", "error",
        "-select_streams", "a",
        "-show_entries", "stream=index",
        "-of", "csv=p=0",
        str(input_path)
    ]
    p = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return bool(p.stdout.strip())

def convert_to_vr180(input_path: str, output_dir: str) -> str:
    """
    Convert input video to a VR180-like side-by-side with blurred background.
    Returns path to output mp4. Will raise RuntimeError on ffmpeg failure.
    """
    input_path = Path(input_path)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    out_file = output_dir / f"{input_path.stem}_vr180.mp4"

    has_audio = _has_audio(str(input_path))

    # filter_complex:
    #  - scale original to 1920x1080 twice -> left,right
    #  - hstack left+right -> vr (3840x1080)
    #  - scale original to 3840x2160 and boxblur to make bg
    #  - overlay vr centered vertically on blurred bg
    filter_complex = (
        "[0:v]scale=1920:1080,split=2[left][right];"
        "[left][right]hstack=inputs=2[vr];"
        "[0:v]scale=3840:2160,boxblur=20:5,eq=brightness=-0.05[bg];"
        "[bg][vr]overlay=0:540[outv]"
    )

    cmd = ["ffmpeg", "-y", "-i", str(input_path),
           "-filter_complex", filter_complex,
           "-map", "[outv]"]

    if has_audio:
        cmd += ["-map", "0:a"]

    cmd += ["-c:v", "libx264", "-preset", "fast", "-crf", "23"]

    if has_audio:
        cmd += ["-c:a", "aac", "-b:a", "192k"]

    cmd += [str(out_file)]

    p = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if p.returncode != 0:
        # Return a truncated stderr for readability but include a hint
        raise RuntimeError("ffmpeg failed:\n" + (p.stderr[:2000] or p.stdout[:2000]))
    return str(out_file)
