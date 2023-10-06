
from torchvision.io import read_image
from torchvision.models.efficientnet import efficientnet_b0, EfficientNet_B0_Weights
from torchvision.transforms import Normalize

from captum.attr import Saliency
from captum.attr import visualization as viz

import numpy as np
from PIL import Image
import io


class EfficientNet():
    def __init__(self) -> None:
        weights = EfficientNet_B0_Weights.DEFAULT
        self.categories_eng = weights.meta["categories"]
        model = efficientnet_b0(weights)
        model.eval()
        self.model = model        
        self.preprocess = weights.transforms()
        with open('src/network/translate.txt','r', encoding='utf-8') as f:
            categories = f.read().split(',')
        self.categories = categories
        #print(self.categories)
        self.saliency = Saliency(self.model)
    
    #Trigger function, Image is selected
    def pass_image_to_net(self, image_path):
        img = read_image(image_path)
        img = self.preprocess(img).unsqueeze(0)

        preprocessed_image = img
        predict = self.model(img).squeeze(0).softmax(0)
        class_id = predict.argmax().item()
        
        self.prediction = self.categories[class_id]
        #self.prediction = self.categories_eng[class_id]
        self.attribution = self._get_explanation(class_id, preprocessed_image)
        self.original_image_path = self._set_original_image(preprocessed_image)
        self.ki_image_path = self._set_attribution_image(preprocessed_image)


    def _set_attribution_image(self, preprocessed_image):
        file = "ki_image.png"
        fig, ax = viz.visualize_image_attr(self.attribution,
                             np.transpose(preprocessed_image.squeeze().cpu().detach().numpy(), (1,2,0)),
                             method='heat_map',
                             show_colorbar=False,
                             sign='absolute_value',
                             alpha_overlay=0.5,
                             outlier_perc=1,
                             use_pyplot=False)
        buf = io.BytesIO()
        fig.savefig(buf, format='png', bbox_inches='tight', pad_inches=0)
        buf.seek(0)
        im = Image.open(buf)
        im = self._threshold_blue_channel(im)
        
        im = Image.composite(im, Image.open(self.original_image_path),im)
        im.save(file)
        buf.close()
        return file

    def _set_original_image(self, preprocessed_image):
        scaled_image = self._scale_image(preprocessed_image)
        file = "original_image.png"
        fig, ax = viz.visualize_image_attr(self.attribution,
                                    np.transpose(scaled_image.squeeze().cpu().detach().numpy(), (1,2,0)),
                                    method='original_image',
                                    show_colorbar=False,
                                    use_pyplot=False)
        
        fig.savefig(file, format='png', bbox_inches='tight', pad_inches=0)

        return file
    
    # sets the attribution map
    def _get_explanation(self, id, preprocessed_image):
         attribution = self.saliency.attribute(preprocessed_image, target=id)
         return np.transpose(attribution.squeeze().cpu().detach().numpy(), (1,2,0))

    # Split the red, green and blue bands from the Image
    def _threshold_blue_channel(self,image, threshold = 230):
        def pixelProc(intensity):
            return 0
        multiBands = image.split()
        redBand = multiBands[0].point(pixelProc)
        greenBand = multiBands[1].point(pixelProc)
        blueBand = multiBands[2].point(lambda x: 0 if x > threshold else 255)

        return Image.merge("RGBA", (redBand, greenBand, blueBand, blueBand))

    def _scale_image(self,preprocessed_image):
        inv_normalize = Normalize(
            mean=[-0.485/0.229, -0.456/0.224, -0.406/0.225],
            std=[1/0.229, 1/0.224, 1/0.225]
        )
        return inv_normalize(preprocessed_image)