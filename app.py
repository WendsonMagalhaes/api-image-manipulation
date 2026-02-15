import gradio as gr
from rembg import remove
from PIL import Image
import io

def remove_bg(image: Image.Image) -> Image.Image:
    output = remove(image)
    return output

demo = gr.Interface(
    fn=remove_bg,
    inputs=gr.Image(type="pil"),
    outputs=gr.Image(type="pil"),
    title="Remove Background API",
    description="Remove o fundo das imagens usando isnet-general-use."
)

demo.launch(server_name="0.0.0.0", server_port=7860)
