# main.py
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from rembg import remove, new_session
from PIL import Image
import requests
import io
import base64
import os
from dotenv import load_dotenv
import uvicorn

# Carregar variáveis de ambiente
load_dotenv()

app = FastAPI()

IMGBB_API_KEY = os.getenv("IMGBB_API_KEY")

# Use a sessão otimizada do rembg
session = new_session("u2netp")

if not IMGBB_API_KEY:
    raise ValueError("IMGBB_API_KEY não configurada")

# Permitir acesso do frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================================
# 🔹 ROTA 1 — REMOVER FUNDO
# =========================================
@app.post("/remove-background")
async def remove_background(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        input_image = Image.open(io.BytesIO(contents)).convert("RGBA")

        # Remoção com sessão otimizada
        output_image = remove(
            input_image,
            session=session,
            alpha_matting=True,
            alpha_matting_foreground_threshold=240,
            alpha_matting_background_threshold=10,
            alpha_matting_erode_size=10
        )

        buffer = io.BytesIO()
        output_image.save(buffer, format="PNG", optimize=True)
        buffer.seek(0)

        return StreamingResponse(
            buffer,
            media_type="image/png",
            headers={"Content-Disposition": "attachment; filename=removed.png"}
        )

    except Exception as e:
        return {"error": str(e)}

# =========================================
# 🔹 ROTA 2 — UPLOAD PARA IMGBB
# =========================================
@app.post("/upload-imgbb")
async def upload_imgbb(file: UploadFile = File(...)):
    try:
        contents = await file.read()
        img_base64 = base64.b64encode(contents)

        response = requests.post(
            "https://api.imgbb.com/1/upload",
            data={"key": IMGBB_API_KEY, "image": img_base64}
        )

        result = response.json()

        if "data" not in result:
            return {"error": result}

        return {
            "message": "Imagem enviada com sucesso",
            "imgbb_url": result["data"]["url"]
        }

    except Exception as e:
        return {"error": str(e)}

# =========================================
# 🔹 START DO APP (para Render)
# =========================================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))  # Porta do Render ou 8000 local
    uvicorn.run("main:app", host="0.0.0.0", port=port)
