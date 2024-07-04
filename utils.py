import json

IMAGE_YELLOW = "#F3CC19"
IMAGE_ORANGE = "#EB600F"
IMAGE_ORANGE_LIGHT = "#f3813f"
IMAGE_ORANGE_DARK = "a8440b"
LNG = "DE"

CENTER_X = 0
CENTER_Y = 0

def get_size_main_container():
    return get_size(0.8,0.8)

def get_size(width, height):
    w = (CENTER_X*2)*width
    h = (CENTER_Y*2)*height
    return w, h

def get_size_with_margin(width, height):
    w,h = get_size(width=width, height=height)
    ve = (CENTER_X - (0.5 * w))*0.5
    ho = (CENTER_Y - (0.5 * h))*0.5
    return w,h, ve, ho

def get_labels(router):
    lng = router.get_data("lng")
    if lng == "DE":
        file = "assets/image_summary_DE.json"
    else:
        file = "assets/image_summary_EN.json"
    
    with open(file, "rb") as f:
        text = json.load(f)
    image_path = router.get_data("img_org").split('/')
    
    if "picture_" in image_path[-1]:
        return False
    
    return text[image_path[-1]]
    
# Section 1
# title_1 = text["section_1"]["title"]
# text_1 = text["section_1"]["text"]