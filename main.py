from fastapi import FastAPI
from fastapi.responses import JSONResponse
import yt_dlp

app = FastAPI()

@app.get("/")
def home():
    return {"message": "MP Back4App Server is Live!"}

@app.get("/download")
def download_video(url: str):
    ydl_opts = {
        'format': 'best',
        'quiet': True,
        'no_warnings': True,
        'nocheckcertificate': True,
        'http_headers': {'User-Agent': 'Mozilla/5.0'}
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            video_url = info.get('url') or info.get('requested_downloads', [{}])[0].get('url')
            if video_url:
                return JSONResponse(content={"status": "success", "url": video_url})
            else:
                return JSONResponse(content={"status": "error"})
    except Exception as e:
        return JSONResponse(content={"status": "error", "message": str(e)})
