from torchvision.io import read_image
from torchvision.models.efficientnet import efficientnet_b0, EfficientNet_B0_Weights
from torchvision.transforms import Normalize

from captum.attr import Saliency
from captum.attr import visualization as viz

from io import BytesIO
from PIL import Image

from .translate import categories

import numpy as np

class EfficientNet():
    def __init__(self) -> None:
        # Use pretrained efficient net as default. 
        weights = EfficientNet_B0_Weights.DEFAULT
        self.preprocess = weights.transforms()

        model = efficientnet_b0(weights)
        model.eval()
        self.model = model        
        self.saliency = Saliency(self.model)

        # Categories
        # with open(resource_path('/network/translate.txt'),'r', encoding='utf-8') as f:
        #     categories = f.read().split(',')
        self.categories = categories()
        self.categories_eng = weights.meta["categories"]
    
    def pass_image_to_net(self, image_path:str):
        '''Triggers the image classification process
        :return: PIL Image instance of the original image and the explained image
        '''
        # Process the image
        img = read_image(image_path)
        preprocessed_image = self.preprocess(img).unsqueeze(0)

        # Make Prediction
        predict = self.model(preprocessed_image).squeeze(0).softmax(0)
        class_id = predict.argmax().item()        
        self.prediction = self.categories[class_id]
        #self.prediction = self.categories_eng[class_id]

        # Make images
        attribution = self._get_explanation(class_id, preprocessed_image)
        original_image = self._get_original_image(preprocessed_image, attribution)
        ki_image = self._get_attribution_image(preprocessed_image, attribution, original_image)

        return original_image, ki_image

    def _get_original_image(self, preprocessed_image, attribution)-> Image:
        '''Private function that returns the original but scaled image'''
        # Scale image
        scaled_image = self._scale_image(preprocessed_image)
        
        # Use Captum for visualisation        
        fig, ax = viz.visualize_image_attr(attribution,
                                    np.transpose(scaled_image.squeeze().cpu().detach().numpy(), (1,2,0)),
                                    method='original_image',
                                    show_colorbar=False,
                                    use_pyplot=False)
        
        # Get a PIL image
        image = self._fig2img(fig)
        return image

    def _get_attribution_image(self, preprocessed_image, attribution, original_image)-> Image:
        '''Private function that returns the explaination image'''
        # Use Captum for visualisation     
        fig, ax = viz.visualize_image_attr(attribution,
                             np.transpose(preprocessed_image.squeeze().cpu().detach().numpy(), (1,2,0)),
                             method='heat_map',
                             show_colorbar=False,
                             sign='absolute_value',
                             alpha_overlay=0.5,
                             outlier_perc=1,
                             use_pyplot=False)
        
        image = self._fig2img(fig)
        image = self._threshold_blue_channel(image) #looks cleaner, accuracy is not relevant for this purpose here.
        
        t_image = Image.composite(image, original_image, mask=image) #combine with original image

        return t_image
    

    def _get_explanation(self, id, preprocessed_image):
         '''Get the attribution map'''
         attribution = self.saliency.attribute(preprocessed_image, target=id)
         return np.transpose(attribution.squeeze().cpu().detach().numpy(), (1,2,0))


    def _threshold_blue_channel(self,image, threshold = 230)->Image:
        '''Calculate the blue marks for the KI recognition. 
        This is not accurate, but the outcome looks way nicer and cleaner.
        For the purpose of visualisation it is perfectly fine
        (Saliency is not reliable anyways)
        '''
        def pixelProc(attr):
            return 0
        multiBands = image.split()
        # only blue pixels thus set green and red to 0
        redBand = multiBands[0].point(pixelProc)
        greenBand = multiBands[1].point(pixelProc)
        # allow blue pixels when above threshold
        blueBand = multiBands[2].point(lambda x: 0 if x > threshold else 255)

        return Image.merge("RGBA", (redBand, greenBand, blueBand, blueBand))


    def _scale_image(self,preprocessed_image):
        '''Make image look correctly'''
        inv_normalize = Normalize(
            mean=[-0.485/0.229, -0.456/0.224, -0.406/0.225],
            std=[1/0.229, 1/0.224, 1/0.225]
        )
        return inv_normalize(preprocessed_image)
    
    def _fig2img(self, figure, use_buf = True):
        '''TODO: Remove, for testing purpose only. Decide for a method!'''
        if use_buf:
            buf = BytesIO()
            figure.savefig(buf, format='png', bbox_inches='tight', pad_inches=0)
            buf.seek(0)
            return Image.open(buf)
        else:
            return Image.frombytes('RGB', figure.canvas.get_width_height(),figure.canvas.tostring_rgb())