import torch
from shap_e.diffusion.sample import sample_latents
from shap_e.diffusion.gaussian_diffusion import diffusion_from_config
from shap_e.models.download import load_model, load_config
from shap_e.util.notebooks import create_pan_cameras, decode_latent_images
import os
import numpy as np
from PIL import Image
import trimesh

class TextTo3DConverter:
    def __init__(self, device='cuda' if torch.cuda.is_available() else 'cpu'):
        self.device = torch.device(device)
        print(f"Using device: {self.device}")
        self.xm = load_model('transmitter', device=self.device)
        self.model = load_model('text300M', device=self.device)
        self.diffusion = diffusion_from_config(load_config('diffusion'))

    def generate(self, prompt, output_dir='output'):
       os.makedirs(output_dir, exist_ok=True)

       print(f"Generating 3D model for prompt: '{prompt}'")

        #generate 3d latent
       latent = sample_latents(
            batch_size=1,
            model=self.model,
            diffusion=self.diffusion,
            guidance_scale=7.5,
            model_kwargs=dict(texts=[prompt]),
            progress=True,
            clip_denoised=True,
            use_fp16=True,
            use_karras=True,
            karras_steps=16,
            sigma_min=1e-3,
            sigma_max=30,
            s_churn=0,
        )[0]

        #secode latent to mesh
       mesh = self.xm.decode_latent_mesh(latent).tri_mesh()

        # filesafe name
       safe_name = "".join(c if c.isalnum() else "_" for c in prompt[:20])

        # save .obj file
       obj_path = os.path.join(output_dir, f"{safe_name}.obj")
       with open(obj_path, 'w') as f:
            mesh.write_obj(f)

        # save .stl file
       stl_path = os.path.join(output_dir, f"{safe_name}.stl")
       tm = trimesh.Trimesh(vertices=mesh.verts, faces=mesh.faces)
       tm.export(stl_path)

        # create preview image
       cameras = create_pan_cameras(64, self.device)
       images = decode_latent_images(self.xm, latent, cameras, render_mode='nerf')


       preview_path = os.path.join(output_dir, f"{safe_name}_preview.gif")
       images[0].save(preview_path, save_all=True, append_images=images[1:], loop=0)

       print(f"\n Generated files:")
       print(f"  OBJ: {obj_path}")
       print(f"  STL: {stl_path}")
       print(f"  Preview GIF: {preview_path}")

       return obj_path, stl_path, preview_path


# interface
if __name__ == "__main__":
    prompt = input("Enter your text prompt to generate a 3D model: ")
    converter = TextTo3DConverter()
    converter.generate(prompt)
