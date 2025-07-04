import gradio as gr
import torch
from diffusers import StableDiffusionPipeline
import random

# Check if MPS is available
device = "mps" if torch.backends.mps.is_available() else "cpu"

# Load the model from Hugging Face (token required if private)
model_id = "nikkijiang/sd-pokemon-generator"
pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float32)
pipe.to(device)

# Function to generate a fictional name
def generate_name(type):
    prefixes = {
        "normal": "Norm",
        "fire": "Pyro",
        "water": "Aqua",
        "electric": "Volt",
        "grass": "Flor",
        "ice": "Cryo",
        "fighting": "Brawl",
        "poison": "Tox",
        "ground": "Terra",
        "flying": "Aero",
        "psychic": "Psy",
        "bug": "Insect",
        "rock": "Geo",
        "ghost": "Spect",
        "dragon": "Draco",
        "dark": "Umbra",
        "steel": "Metal",
        "fairy": "Charm"
    }
    suffixes = ["zor", "mon", "chu", "dra", "gon", "tail", "eon"]
    return f"{prefixes.get(type.lower(), 'Monster')}{random.choice(suffixes)}"

# Main logic
def generate_monster(description, type, color, nature):
    prompt = f"""
      A cute, original Pokémon-style creature. It is {description}, belongs to the {type} type, has a primarily {color} color scheme, and exhibits a {nature} personality. 
      Drawn in high-quality digital art style, vibrant colors, clean lines, and full-body design. White background.
    """
    result = pipe(prompt)
    if not result.images:
        raise ValueError("No images were generated by the model.")
    image = result.images[0]
    name = generate_name(type)

    return name, image

types = [
    "Normal", "Fire", "Water", "Electric", "Grass", "Ice",
    "Fighting", "Poison", "Ground", "Flying", "Psychic", "Bug",
    "Rock", "Ghost", "Dragon", "Dark", "Steel", "Fairy"
]

colors = [
    "Red", "Blue", "Green", "Yellow", "Black", "White", "Purple", 
    "Pink", "Orange", "Brown", "Gray", "Cyan",
    "Light Blue", "Dark Red", "Neon Green", "Bright Yellow", "Metallic Silver", 
    "Pastel Pink", "Glossy Black", "Matte Gray", "Earthy Brown"
]

natures = [
    "Hardy", "Lonely", "Brave", "Adamant", "Naughty",
    "Bold", "Docile", "Relaxed", "Impish", "Lax",
    "Timid", "Hasty", "Serious", "Jolly", "Naive",
    "Modest", "Mild", "Quiet", "Bashful", "Rash",
    "Calm", "Gentle", "Sassy", "Careful", "Quirky"
]

# Gradio Interface
with gr.Blocks() as demo:
    gr.Markdown("## Monster Generator")
    with gr.Row():
        with gr.Column():
            description_input = gr.Textbox(label="Description")
            type_input = gr.Dropdown(choices=types, label="Type")
            color_input = gr.Dropdown(choices=colors, label="Color")
            nature_input = gr.Dropdown(choices=natures, label="Nature")
            button = gr.Button("Generate Monster")

        with gr.Column():
            name_output = gr.Textbox(label="Monster Name", interactive=False)
            image_output = gr.Image(label="Imagen generada")

    button.click(
        fn=generate_monster,
        inputs=[description_input, type_input, color_input, nature_input],
        outputs=[name_output, image_output]
    )

demo.launch()