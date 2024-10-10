from network.model_wrapper import ModellWrapper
from os import listdir

from io import BytesIO
import base64

class ImageManager():    
    def __init__(self) -> None:
        '''
        Class that handles the images, such as the users annotations
        '''
        # List of all images
        self.image_list = [f"assets/images/{imagepath}" for imagepath in listdir("assets/images")]
        self.network = ModellWrapper()
        self.original_image = None
        self.ki_image = None
        self.ki_image_adv = None
        self.user_image = None
        self.attack_image = None
        self.composed_attack_image = None
        self.prediction = ""
    
    def set_image(self, path: str):
        '''Sets the image in the path'''
        self.original_image, img_pil = self.network.process_image(path, pil = True)
        self.image_b64 = self.im_2_b64(img_pil)
        
    
    def get_attack(self):
        adv, pixel, t_adv, t_pxl = self.network.get_attack(self.original_image)

        idx, probs = self.network.get_predictions(t_adv)
        self.pred_adv = (idx, probs)

        idx, probs = self.network.get_predictions(t_pxl)
        self.pred_pxl = (idx, probs)

        self.attack_image = self.im_2_b64(pixel)
        self.composed_attack_image = self.im_2_b64(adv)

        self.get_explanation(image=t_adv)

        idx, probs = self.network.get_predictions(self.original_image)
        self.prediction = idx
        self.probs = probs


    def get_explanation(self,image = None):
        if image is not None:
            pred = self.pred_adv[0]
            ki_image =self.network.get_explanations(image, pred[0])
            self.ki_image_adv = self.im_2_b64(ki_image)
            
        idx, probs = self.network.get_predictions(self.original_image)
        self.prediction = idx
        self.probs = probs

        ki_image =self.network.get_explanations(self.original_image, self.prediction[0])
        self.ki_image = self.im_2_b64(ki_image)

    def get_prediction(self, image):
        img = self.network.process_image(image)
        img = self.network.transform(img)

        return self.network.get_predictions(image=img)


    def clean_up(self):
        '''cleans the generated images, triggered everytime when returning to start screen'''
        self.network = ModellWrapper()
        self.original_image = None
        self.ki_image = None
        self.user_image = None
        self.attack_image = None
        self.composed_attack_image = None
        self.prediction = ""
        print("Did some cleaning")
    
    # Convert Image to Base64 
    def im_2_b64(self,image):
        image = image.resize((600,600))
        buff = BytesIO()
        print(image.size)
        image.save(buff, format="PNG")        
        img_str = base64.b64encode(buff.getvalue()).decode("utf-8")
        return img_str
    