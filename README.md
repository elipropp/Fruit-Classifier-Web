# Fruit Classifier Web

This repo is the code base for the web app version of a deep learning model I created using the [fast.ai](https://www.fast.ai) library. Upload an image of any of the listed fruits on the page and let it tell you what fruit you uploaded. Try it out and let me know how it goes!

I trained the model using the ResNet50 model with a dataset I created from Google images (taught in the fastai course linked below). I used around 300 images per category, with an 80/20 split of training/validation sets. No test set was created at the moment as I continue the course mentioned below, although I may create one at a later date. I cleaned a large portion of the data myself using a tool from the fast.ai library, but not all of it. I may clean it further later on.

The jupyter notebooks used to create the model will be uploaded soon. I may be retraining the model, so it may take a little longer to upload them.

Check out the [Practical Deep Learning for Coders](https://course.fast.ai/) course by fast.ai that taught me how to create the model!

To make the website I used the [Streamlit](https://www.streamlit.io/) library for Python. The library is really simple to use and allows for rapid deployment of data models.
