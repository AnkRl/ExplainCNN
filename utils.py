from os.path import join, abspath
from io import BytesIO
from kivy.uix.image import Image, CoreImage
import sys

''' helper to make paths'''
def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return join(sys._MEIPASS, relative_path)
    return join(abspath("."), relative_path)

'''Helper to make kivy images out of images'''
def img2kivy(image, size_hint = (1,1)):
        image_bytes = BytesIO()
        image.save(image_bytes, format="png")
        image_bytes.seek(0)

        img = CoreImage(image_bytes, ext="png").texture

        new_img = Image(size_hint=size_hint)
        new_img.texture = img
        image_bytes.close()
        
        return new_img