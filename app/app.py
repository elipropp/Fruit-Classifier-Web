import aiohttp
import asyncio
import streamlit as st
from fastai import *
from fastai.vision import *
import numpy as np
import pandas as pd
import matplotlib.image as mpimg
import os
import time
from PIL import Image
import requests
from io import BytesIO

# App Title
st.title("Fruit Classifier")

export_file_url = 'https://drive.google.com/uc?export=download&id=1fW61igTn4zac92nR825R55hdE7pvibgO'
export_file_name = 'Fruit_classifier.pkl'

classes = ['Apple', 'Banana', 'Blackberry', 'Blueberry', 'Lemon', 'Lime', 'Mango', 'Orange',
           'Pear', 'Raspberry', 'Strawberry', 'Tomato']

path = Path(__file__).parent

st.sidebar.header("About the Model")
st.sidebar.markdown(""" 

Hi! Welcome to my fruit classifier.
Upload an image or pass in a url of one of the following
fruits, and have the classifier let you know what it is.

Apple, Banana, Blackberry, Blueberry, Lemon,
Lime, Mango, Orange, Pear, Raspberry, 
Strawberry, Tomato

And yes, tomatoes are fruits.
""")

st.sidebar.header("About Me")
st.sidebar.markdown("""

I'm Eli Propp, a computer engineering student at the
University of Waterloo. I'm passionate about data science,
machine learning and software development.

Check out the GitHub Repo for this website below.
Reach out if like what you see, have any tips, or
want to work on a project together.

GitHub Repo: [Click here](https://github.com/Ehpropp/Fruit-Classifier-Web)

""")


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


@st.cache
def predict(img):

    # Show a message while executing
    with st.spinner('Analyzing...'):
        time.sleep(3)

    pred_class = model.predict(img)[0]
    # Maybe add in prediction probability after

    pred_prob = round(torch.max(model.predict(img)[2]).item()*100)

    return str(pred_class), str(pred_prob)


def print_result(fruit, prob):
    st.success("This is a " + fruit + " with " +
               prob + "%" + " certainty")


def show_image(image):
    # Display the image
    st.image(image, use_column_width=True)


upload_type = st.radio(
    '', ['Upload Image from device', 'Upload image from URL'])

if (upload_type == 'Upload Image from device'):
    img_file_buffer = st.file_uploader(
        "Upload an image", type=['png', 'jpg', 'jpeg'])
    if img_file_buffer is not None:
        img = open_image(img_file_buffer)
        display_img = np.array(Image.open(img_file_buffer))
        show_image(display_img)
        fruit, prob = predict(img)
        print_result(fruit, prob)

elif (upload_type == 'Upload image from URL'):
    st.write("The url should be a link directly to the file.")
    url = st.text_input("URL:")

    if url != "":
        try:
            # Read image from the url
            response = requests.get(url)
            pil_img = Image.open(BytesIO(response.content))
            img = open_image(BytesIO(response.content))
            display_img = np.asarray(pil_img)
            show_image(display_img)

            predict(img)

            fruit, prob = predict(img)
            print_result(fruit, prob)

        except:
            st.text("Invalid url!")
