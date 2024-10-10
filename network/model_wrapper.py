from torchvision.io import read_image
from torchvision.models.efficientnet import efficientnet_b0, EfficientNet_B0_Weights
from torchvision.transforms import Normalize
from torchvision.transforms._presets import ImageClassification, InterpolationMode
from functools import partial

from captum.attr import Saliency
from captum.attr import visualization as viz

from art.attacks.evasion import FastGradientMethod
from art.estimators.classification import PyTorchClassifier

from io import BytesIO
from PIL import Image

import torch.nn as nn
import torch.optim as optim
from torch import from_numpy
from torch import Tensor

import numpy as np

class ModellWrapper():
    def __init__(self) -> None:
        weights = EfficientNet_B0_Weights.DEFAULT
        transform = partial(ImageClassification, crop_size=256, resize_size=256, interpolation=InterpolationMode.BICUBIC)
        self.model = efficientnet_b0(weights)
        self.model.eval()
        criterion = nn.CrossEntropyLoss()
        optimizer = optim.Adam(self.model.parameters(), lr=0.01)
        self.art_model = PyTorchClassifier(
            model=self.model,
            clip_values=(0,1),
            loss=criterion,
            optimizer=optimizer,
            input_shape=(3, 256, 256),
            nb_classes=1000,
        )
        self.saliency = Saliency(self.model)
        self.attack = FastGradientMethod(estimator=self.art_model, eps = 0.1)
        self.preprocess = transform()

    def get_attack(self, image):
        image = image.numpy()
        adversarial_image = self.attack.generate(x=image)
        pixel_image = Tensor(adversarial_image - image)
        adv = self._get_pil_image(from_numpy(adversarial_image))
        pixel  = self._get_pil_image(pixel_image)

        return adv, pixel, Tensor(adversarial_image), pixel_image

    def get_explanations(self, image, prediction):
        attribution = self.saliency.attribute(image, target=prediction)
        attribution = np.transpose(attribution.squeeze().cpu().detach().numpy(), (1,2,0))

        image = self._get_pil_image(image)

        # Use Captum for visualisation     
        fig, _ = viz.visualize_image_attr(attribution,
                             image,
                             method='heat_map',
                             show_colorbar=False,
                             sign='absolute_value',
                             alpha_overlay=0.5,
                             outlier_perc=1,
                             use_pyplot=False)
        
        explanation = self._fig2img(fig)
        explanation = self._threshold_blue_channel(explanation) #looks cleaner, accuracy is not relevant for this purpose here.
        
        return Image.composite(explanation, image, mask=explanation) #combine with original image
    
    def transform(self,image):
        transform = partial(ImageClassification, crop_size=256, resize_size=256, interpolation=InterpolationMode.BICUBIC)()
        return transform(image).unsqueeze(0)
        
    def get_predictions(self, image):
        predict = self.model(image).squeeze(0).softmax(0)
        idx = sorted(range(len(predict)), key = lambda sub: predict[sub])[-3:]
        probs = predict[idx]*100
        return idx, probs.tolist()
    
    def scale_image(self, image):
        '''Make image look correctly'''
        inv_normalize = Normalize(
            mean=[-0.485/0.229, -0.456/0.224, -0.406/0.225],
            std=[1/0.229, 1/0.224, 1/0.225]
        )
        return inv_normalize(image)
    
    def process_image(self, image_path:str, pil = False):
        img = read_image(image_path)
        img = self.transform(img)
        if pil:
            return img, self._get_pil_image(img)
        
        return img
    
    def _get_pil_image(self, preprocessed_image)-> Image:
        '''Private function that returns the original but scaled image'''
        # Scale image
        scaled_image = self.scale_image(preprocessed_image)
        
        # Use Captum for visualisation        
        fig, ax = viz.visualize_image_attr(None, #hier
                                    np.transpose(scaled_image.squeeze().cpu().detach().numpy(), (1,2,0)),
                                    method='original_image',
                                    show_colorbar=False,
                                    use_pyplot=False)
        
        # Get a PIL image
        image = self._fig2img(fig)
        return image

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

    def _fig2img(self, figure, use_buf = True):
        '''TODO: Remove, for testing purpose only. Decide for a method!'''
        if use_buf:
            buf = BytesIO()
            figure.savefig(buf, format='png', bbox_inches='tight', pad_inches=0)
            buf.seek(0)
            return Image.open(buf)
        else:
            return Image.frombytes('RGB', figure.canvas.get_width_height(),figure.canvas.tostring_rgb())