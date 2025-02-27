import asyncio
from random import randint
from PIL import Image
import requests
import os
import subprocess
from dotenv import load_dotenv
from time import sleep

# Load API Key
load_dotenv()
API_KEY = os.getenv("HuggingFaceAPIKey")

headers = {"Authorization": f"Bearer {'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'}"}
API_URL = "https://api-inference.huggingface.co/models/stabilityai/stable-diffusion-xl-base-1.0"

# Function to open images automatically
def open_images(prompt):
    folder_path = r"Data"
    prompt = prompt.replace(" ", "_")

    files = [f"{prompt}{i}.jpg" for i in range(1, 5)]
    
    for jpg_file in files:
        image_path = os.path.join(folder_path, jpg_file)
        try:
            img = Image.open(image_path)
            print(f"Opening image: {image_path}")

            # Open with system's default image viewer
            subprocess.run(["start", image_path], shell=True)

            sleep(1)
        except IOError:
            print(f"Unable to open {image_path}")

# Async function to query Hugging Face API
async def query(payload):
    response = await asyncio.to_thread(requests.post, API_URL, headers=headers, json=payload)
    return response.content

# Async function to generate images
async def generate_images(prompt: str):
    tasks = []
    
    for _ in range(4):  # Generate 4 images
        payload = {
            "inputs": f"{prompt}, quality=4K, sharpness= maximum, Ultra High details, high resolution, seed={randint(0, 1000000)}"
        }
        task = asyncio.create_task(query(payload))
        tasks.append(task)

    image_bytes_list = await asyncio.gather(*tasks)

    # Save images
    for i, image_bytes in enumerate(image_bytes_list):
        with open(fr"Data\{prompt.replace(' ','_')}{i+1}.jpg", "wb") as f:
            f.write(image_bytes)

# Wrapper function to generate and open images
def GenerateImages(prompt: str):
    asyncio.run(generate_images(prompt))
    open_images(prompt)

# Main Loop
while True:
    try:
        with open(r"Frontend\Files\ImageGeneration.data", "r") as f:
            Data: str = f.read()
        
        Prompt, Status = Data.split(",")

        if Status.strip() == "True":
            print("Generating Images...")
            GenerateImages(prompt=Prompt.strip())

            # Reset status after generating images
            with open(r"Frontend\Files\ImageGeneration.data", "w") as f:
                f.write("False, False")
            
            break
        else:
            sleep(1)
    except:
        pass
