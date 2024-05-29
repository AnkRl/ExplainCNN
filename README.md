# ExplainCNN
Visually explain image classifications.

Install using pip install -r requirements.txt
⚠️ There is a problem with matplotlib and captum. Replace line 250 `plt_axis.grid(b=False)` in captums `_utils/visualization.py` with `plt_axis.grid(visible=False)`

## Libraries
- `torchvision` with the pretrained EfficientNet for classification
- `captum` for explaining and plotting the results
- `flet` for the GUI

## Repository structure
- `main.py`  starts the app. The content of the app is displayed in changing views.
- `image_manager.py` class that communicates between flet ( aka gui) components and the EfficientNet

- `/views` contains the components of the gui. 
- `/assets/images` contains example images for classification
- `/network`  contains the neural network for classification and explaining
