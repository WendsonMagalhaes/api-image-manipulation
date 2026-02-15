import gradio as gr
from isnet_general_use import new_session
from PIL import Image
import io
import base64

# Cria a sessão do modelo
session = new_session("isnet-general-use")

def remove_background(image: Image.Image):
    """
    Recebe PIL.Image, retorna PIL.Image com fundo removido
    """
    if image.mode != "RGB":
        image = image.convert("RGB")

    # Aplica remoção de fundo
    output_image = session.process(image)  # dependendo da versão do isnet-general-use

    return output_image

# Interface Gradio
demo = gr.Interface(
    fn=remove_background,
    inputs=gr.Image(type="pil"),
    outputs=gr.Image(type="pil"),
    title="Remover Fundo AI",
    description="Envie uma imagem e remova o fundo automaticamente.",
    allow_flagging="never"
)

demo.launch()
