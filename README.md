# :hourglass_flowing_sand: ExplainCNN
Visually explain image classifications.
Install using pip install -r requirements.txt
⚠️ There is a problem with matplotlib and captum. Replace line 250 `plt_axis.grid(b=False)` in captums `_utils/visualization.py` with `plt_axis.grid(visible=False)`
## :hammer_and_wrench: Currently working on
GUI Design (compare figma prototype):
|  Component   |  Status   |   Figma  |
| --- | --- |  --- |
| StartScreen |:heavy_check_mark: | ![grafik](https://github.com/AnkRl/ExplainCNN/assets/76557267/747a1971-d2d2-4036-a154-81dd6e9a4421) |
| ModeScreen |⌛ | ![grafik](https://github.com/AnkRl/ExplainCNN/assets/76557267/11ae38f7-c8b8-49ab-acc0-816bccb7a6a2) |
|CompareScreen |:hourglass_flowing_sand:| ![grafik](https://github.com/AnkRl/ExplainCNN/assets/76557267/16d5ea17-3c62-44c5-abde-36cea02b513c) |

## Libraries
- `torchvision` with the pretrained EfficientNet for classification
- `captum` for explaining and plotting the results
- `kivy` and `kivymd` for the GUI

## Repository structure
- `main.py`  starts the kivymd app. All content in the app is depicted in one of three screens.
- `image_manager.py` class that communicates between kivy ( aka gui) components and the EfficientNet

- `/components` contains the components of the gui. 
- `/design` describes the components in kivy language
- `/images` contains example images for classification
- `/network`  contains the neural network for classification and explaining

## 
