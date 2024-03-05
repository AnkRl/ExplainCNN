import random
from network.efficient_net import EfficientNet
from utils import resource_path

class ImageManager():    
    def __init__(self) -> None:
        '''
        Class that handles the images, such as the users annotations
        '''
        # List of all images
        self.image_list = [

            resource_path("images/basketball.jpg"),
            resource_path("images/bee.jpg"),
            resource_path("images/cucumber.jpg"),
            resource_path("images/frog.jpg"),

            resource_path("images/giant_panda.jpg"),
            resource_path("images/hamster.jpg"),
            resource_path("images/lemon.jpg"),
            resource_path("images/lion.jpg"),

            resource_path("images/whale.jpg"),
            resource_path("images/apple.jpg"),
            resource_path("images/elephant.jpg"),
            resource_path("images/sheep.jpg")
        ]
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
    
    def random_image(self):
        '''Sets a random image for classification'''
        random_path =  random.choice(self.image_list)
        self.set_image(random_path)
    
    def set_image(self, path: str):
        '''Sets the image in the path'''
        self.original_image = self.network.process_image(path)

    def get_prediction(self):
        
        self.ki_image = self.network.pass_image_to_net()
        self.prediction = self.network.prediction
        
        return False