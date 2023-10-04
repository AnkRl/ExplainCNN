import numpy as np

from matplotlib.colors import LinearSegmentedColormap

from torchvision.io import read_image
from torchvision.models.efficientnet import efficientnet_b0, EfficientNet_B0_Weights

from captum.attr import IntegratedGradients, Saliency, DeepLift, Deconvolution, DeepLiftShap
from captum.attr import GradientShap
from captum.attr import Occlusion
from captum.attr import NoiseTunnel
from captum.attr import visualization as viz
METHOD = "p"

img = read_image("images/n01662784_244_turtle.jpg") # turtle, around it, it is important?
#img = read_image("images/n07739125_8731_apple.jpg")

# Step 1: Initialize model with the best available weights
weights = EfficientNet_B0_Weights.DEFAULT
model = efficientnet_b0(weights) #EfficientNet(weights=weights)
model.eval()

# Step 2: Initialize the inference transforms
preprocess = weights.transforms()

# Step 3: Apply inference preprocessing transforms
image = preprocess(img).unsqueeze(0)

# Step 4: Use the model and print the predicted category
prediction = model(image).squeeze(0).softmax(0)
class_id = prediction.argmax().item()
score = prediction[class_id].item()
category_name = weights.meta["categories"][class_id]
print(len(weights.meta["categories"]))
print(f"{category_name}: {100 * score:.1f}%")

with open("myfile.txt", "w") as file1:
    # Writing data to a file
    file1.write(str(weights.meta["categories"]))

print(METHOD)
if METHOD == "IG":
    # Uses up to 20 GB RAM
    integrated_gradients = IntegratedGradients(model)
    attributions = integrated_gradients.attribute(image, n_steps=200, target=class_id)

elif METHOD =="Saliency":
    # Uses up to 1 GB RAM
    saliency = Saliency(model)
    attributions = saliency.attribute(image, target=class_id)

elif METHOD =="DL":
    # Uses up to 1 GB RAM
    deep_lift = DeepLift(model)
    attributions = deep_lift.attribute(image, target=class_id)

elif METHOD =="DLShap":
    # Uses up to 1 GB RAM
    deep_lift_shap = DeepLiftShap(model)
    attributions = deep_lift_shap.attribute(image, target=class_id)

elif METHOD =="Deconv":
    # Uses up to  GB RAM
    deconv = Deconvolution(model)
    attributions = deconv.attribute(image, target=class_id)
else:
    raise NotImplementedError

# Visualize
_ = viz.visualize_image_attr(np.transpose(attributions.squeeze().cpu().detach().numpy(), (1,2,0)),
                             np.transpose(image.squeeze().cpu().detach().numpy(), (1,2,0)),
                             method='blended_heat_map',
                             #cmap=default_cmap,
                             show_colorbar=False,
                             sign='absolute_value',
                             alpha_overlay=0.5,
                             outlier_perc=1)