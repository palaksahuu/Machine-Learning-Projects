#  Convert Photo or Text to 3D Model
This project allows you to generate simple 3D models from either text prompts or 2D images using AI models like [Shape-E](https://github.com/openai/shap-e) and OpenCV preprocessing techniques. Output is generated in .obj format with optional previews for text-based generation.

## Files Structure
|-models/
   -image_to_3d.py
   -text_to_3d.py
   -main.py
   -utils/
   -visualization.py

|-output/
   -output.obj (output save of 3d model in .obj and .stl form here)
|-images/
   -images( some images you can use for take image as imput )   
|-requirements.txt
|-README.md
|-venv



##  File explaination
- text_to_3d.py :  
  Takes a text prompt as input and generates a 3D model in .obj and .stl formats using the [Shape-E](https://github.com/openai/shap-e) library.

- image_to_3d.py:  
  Takes an input image and generates a 3D model using pretrained image-to-3D generation techniques. Outputs are saved in .obj and .stl format.

- visualization.py:  
  Generates a .gif rotating preview of the generated 3D model using Shape-E's decoding utilities.

- main.py:  
  This is the entry point of the project. It provides a terminal-based interface:
  - Press `1` → Input a "text prompt" for 3D generation.
  - Press `2` → Input an "image path" to generate a 3D model from an image.


## Setup Instructions


1. Set up a virtual environment
python -m venv venv
venv\Scripts\activate

2. Install dependencies

Install dependencies from requirements.txt

pip install -r requirements.txt
torch
torchvision
torchaudio
rembg
matplotlib
pyrender
open3d
ipywidgets
Pillow
opencv-python
trimesh
pyrender
matplotlib
git+https://github.com/openai/shap-e.git
 OR
git+https://github.com/openai/shap-e.git@main

3. Run
python main.py

agter run this commond in terminal python main.py press key "1" for text to 3d model generation or press key "2" for image to 3d model generation.

It will take some time to generated 3d model (totally based on cpu perfomace )

## output in form of .obj 
like :-
output/your_prompt.obj
output/your_image.obj
output/your_prompt_preview.gif

Text -“car”
output/car.obj 

Image -chair.jpg
output/chair.obj

Ouput get in .obj  so use any online 3d viewer plateform to watch the 3d visulization .
use online platform - https://3dviewer.net/

##  thought process Summary
I wanted a flexible solution so I split the flow into text-based and image-based pipelines.

For text- I chose Shape-E because it is state of the art, open source, and fast.

For image- I focused on preprocessing and constructing a mesh using pixel values and image contours.

Visualization was added to help preview models before using them.