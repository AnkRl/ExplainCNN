import json

IMAGE_YELLOW = "#F3CC19"
IMAGE_ORANGE = "#EB600F"
LNG = "DE"

CENTER_X = 0
CENTER_Y = 0

with open("assets/de.json", "rb") as f:
    text = json.load(f)
translator = text

def switch_lng(lng):
    match lng:
        case "DE":
            file = "assets/de.json"
        case "EN" | _:
            file = "assets/en.json"
    with open(file) as f:
        translator = json.load(f)



# Section 1
# title_1 = text["section_1"]["title"]
# text_1 = text["section_1"]["text"]