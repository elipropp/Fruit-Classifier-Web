import aiohttp
import asyncio
import streamlit as st
from fastai import *
from fastai.vision import *
import numpy as np
import matplotlib.image as mpimg
import os
import time
from PIL import Image
import requests
from io import BytesIO

# App Title
st.title("Test Title")

export_file_url = 'https://drive.google.com/uc?export=download&id=1fW61igTn4zac92nR825R55hdE7pvibgO'
export_file_name = 'Fruit_classifier.pkl'

classes = ['Apple', 'Banana', 'Blackberry', 'Blueberry', 'Lemon', 'Lime', 'Mango', 'Orange',
           'Pear', 'Raspberry', 'Strawberry', 'Tomato']

path = Path(__file__).parent


async def download_file(url, dest):
    if dest.exists():
        return
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.read()
            with open(dest, 'wb') as f:
                f.write(data)


async def setup_learner():
    await download_file(export_file_url, path / export_file_name)
    learn = load_learner(path, export_file_name)
    return learn

model = asyncio.run(setup_learner())


def predict(img, display_img):

    # Display the image
    st.image(display_img, use_column_width=True)
    # display.show()

    # Show a message while executing
    with st.spinner('Analyzing...'):
        time.sleep(3)

    pred_class = model.predict(img)[0]
    # Maybe add in prediction probability after

    pred_prob = round(torch.max(model.predict(img)[2]).item()*100)

    st.write(str(pred_class))
    st.write(str(pred_prob))


upload_type = st.radio(
    '', ['Upload Image from device', 'Upload image from URL'])

if (upload_type == 'Upload Image from device'):
    img_file_buffer = st.file_uploader(
        "Upload an image", type=['png', 'jpg', 'jpeg'])
    if img_file_buffer is not None:
        img = open_image(img_file_buffer)
        display_img = np.array(Image.open(img_file_buffer))
        predict(img, display_img)

elif (upload_type == 'Upload image from URL'):
    url = st.text_input("Please input a url:")

    if url != "":
        try:
            # Read image from the url
            response = requests.get(url)
            pil_img = Image.open(BytesIO(response.content))
            img = open_image(BytesIO(response.content))
            display_img = np.asarray(pil_img)

            predict(img, display_img)

        except:
            st.text("Invalid url!")
