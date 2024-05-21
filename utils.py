import json

IMAGE_YELLOW = "#F3CC19"
IMAGE_ORANGE = "#EB600F"
LNG = "DE"

CENTER_X = 0
CENTER_Y = 0

def get_size(width, height):
    w = (CENTER_X*2)*width
    h = (CENTER_Y*2)*height
    return w, h

def get_size_with_margin(width, height):
    w,h = get_size(width=width, height=height)
    ve = (CENTER_X - (0.5 * w))*0.5
    ho = (CENTER_Y - (0.5 * h))*0.5
    return w,h, ve, ho


# Section 1
# title_1 = text["section_1"]["title"]
# text_1 = text["section_1"]["text"]