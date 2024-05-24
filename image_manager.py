import random
from network.efficient_net import EfficientNet
from torchvision.io import read_image
from os import listdir
from torchvision.transforms._presets import ImageClassification, InterpolationMode
from functools import partial

from io import BytesIO
import base64

class ImageManager():    
    def __init__(self) -> None:
        '''
        Class that handles the images, such as the users annotations
        '''
        # List of all images
        self.image_list = [f"assets/images/{imagepath}" for imagepath in listdir("assets/images")]
        self.original_image = None
        self.ki_image = None
        self.user_image = None
        self.network = EfficientNet()
        self.prediction = ""

    def clean_up(self):
        '''cleans the generated images, triggered everytime when returning to start screen'''
        self.original_image = None
        self.ki_image = None
        self.user_image = None
        self.network = EfficientNet()
        print("Did some cleaning")
    
    # Convert Image to Base64 
    def im_2_b64(self,image):
        image = image.resize((600,600))
        buff = BytesIO()
        print(image.size)
        image.save(buff, format="PNG")        
        img_str = base64.b64encode(buff.getvalue()).decode("utf-8")
        return img_str
    
    def random_image(self):
        '''Sets a random image for classification'''
        random_path =  random.choice(self.image_list)
        self.set_image(random_path)
        return random_path
    
    def set_image(self, path: str):
        '''Sets the image in the path'''
        self.original_image = self.network.process_image(path)

    def get_prediction(self):
        #TODO: Make async with asyncio (?)
        self.ki_image = self.im_2_b64(self.network.pass_image_to_net())
        self.prediction = self.network.prediction
        
        return False
    