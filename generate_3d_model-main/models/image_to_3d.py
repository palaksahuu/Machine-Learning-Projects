import os
import cv2
import numpy as np
import torch
from PIL import Image
from torchvision import transforms
import trimesh

class ImageTo3DConverter:
    def __init__(self, device='cuda' if torch.cuda.is_available() else 'cpu'):
     self.device = torch.device(device)
     self.model = torch.hub.load("intel-isl/MiDaS", "MiDaS_small", trust_repo=True).to(self.device)
     self.model.eval()
     self.transform = torch.hub.load("intel-isl/MiDaS", "transforms", trust_repo=True).small_transform

    def remove_background(self, image_path):
        img = cv2.imread(image_path)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        _, mask = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY_INV)
        kernel = np.ones((5, 5), np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
        result = cv2.bitwise_and(img, img, mask=mask)
        return result

    def estimate_depth(self, image):
        input_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        input_tensor = self.transform(input_image).to(self.device)  
        with torch.no_grad():
         prediction = self.model(input_tensor)
        prediction = torch.nn.functional.interpolate(
            prediction.unsqueeze(1),
            size=input_image.shape[:2],
            mode="bicubic",
            align_corners=False,
        ).squeeze()
        depth_map = prediction.cpu().numpy()
        return depth_map

    def depth_to_point_cloud(self, depth_map, scale=0.1, step=10):
        points = []
        h, w = depth_map.shape
        for y in range(0, h, step):
            for x in range(0, w, step):
                z = depth_map[y, x] * scale
                points.append([x, y, z])
        return np.array(points)

    def save_point_cloud_as_obj(self, points, output_path):
        with open(output_path, 'w') as f:
            for p in points:
                f.write(f"v {p[0]} {p[1]} {p[2]}\n")

    def generate(self, image_path, output_dir='output'):
        os.makedirs(output_dir, exist_ok=True)
        print(f" Processing image: {image_path}")
        bg_removed = self.remove_background(image_path)
        depth_map = self.estimate_depth(bg_removed)
        points = self.depth_to_point_cloud(depth_map)
        obj_path = os.path.join(output_dir, 'output_model.obj')
        self.save_point_cloud_as_obj(points, obj_path)
        print(f" 3D model saved as: {obj_path}")
        return obj_path