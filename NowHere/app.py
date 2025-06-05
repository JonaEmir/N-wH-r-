from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

app = FastAPI()

# Configuracion de CORS (ajusta los orígenes según tu frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.mount("/images", StaticFiles(directory="NowHere/web/images"), name="images")

@app.get("/web/inicio/index.html")
async def inicio():
    file_path = os.path.join("NowHere", "web", "inicio", "index.html")
    return FileResponse(file_path, media_type="text/html")
