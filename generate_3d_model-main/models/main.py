import argparse
from text_to_3d import TextTo3DConverter
from image_to_3d import ImageTo3DConverter
from utils.visualization import plot_3d_model
import os
import sys
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)

def main():
    parser = argparse.ArgumentParser(description="Convert photo or text to 3D model")
    parser.add_argument('--text', type=str, help="Text prompt for 3D generation")
    parser.add_argument('--image', type=str, help="Path to input image")
    parser.add_argument('--output', type=str, default="output", help="Output directory")
    parser.add_argument('--preview', action='store_true', help="Show 3D preview")

    args = parser.parse_args()

    #no arguments passed ask user
    if len(sys.argv) == 1:
        mode = input("Generate 3d from (1) Text or (2) Image - Enter 1 or 2: ").strip()
        if mode == '1':
            args.text = input("Enter your text prompt: ").strip()
        elif mode == '2':
            args.image = input("Enter path to your image: ").strip()
        else:
            print("Invalid choice ")
            return

    if args.text and args.image:
        print("Error: Please provide only one of text or image not both.")
        return

    os.makedirs(args.output, exist_ok=True)

    try:
        if args.text:
            print(f"Generating 3d model from text: {args.text}")
            converter = TextTo3DConverter()
            obj_path, preview_path = converter.generate(args.text, args.output)

        elif args.image:
            print(f" Generating 3d model from image: {args.image}")
            converter = ImageTo3DConverter()
            obj_path = converter.generate(args.image, args.output)

        else:
            print(" no valid input provided.")
            return

        print(f"\n 3D model (.obj) saved at: {obj_path}")
        stl_path = obj_path.replace(".obj", ".stl")
        if os.path.exists(stl_path):
            print(f" 3D model (.stl) saved at: {stl_path}")
        if args.text:
            print(f" Preview saved at: {preview_path}")

        if args.preview:
            plot_3d_model(obj_path)

    except Exception as e:
        print(f" Error during generation: {e}")

if __name__ == "__main__":
    main()
