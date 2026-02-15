from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from rembg import remove
from PIL import Image
import requests
import io
import base64
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

IMGBB_API_KEY = os.getenv("IMGBB_API_KEY")

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


@app.post("/remove-background")
async def remove_background(file: UploadFile = File(...)):
    try:
        contents = await file.read()

        input_image = Image.open(io.BytesIO(contents)).convert("RGBA")

        # Remove fundo
        output_image = remove(input_image)

        # Salvar em memória com alta qualidade
        buffer = io.BytesIO()
        output_image.save(buffer, format="PNG", optimize=True)
        buffer.seek(0)

        # Converter para base64
        img_base64 = base64.b64encode(buffer.read())

        # Enviar para ImgBB
        response = requests.post(
            "https://api.imgbb.com/1/upload",
            data={
                "key": IMGBB_API_KEY,
                "image": img_base64
            }
        )

        result = response.json()

        if "data" not in result:
            return {"error": result}

        return {
            "message": "Fundo removido e enviado com sucesso",
            "imgbb_url": result["data"]["url"]
        }

    except Exception as e:
        return {"error": str(e)}
