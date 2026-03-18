import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import numpy as np

def plot_3d_model(obj_path):
    """Simple 3D plot of OBJ file using matplotlib"""
    vertices = []
    faces = []
    
    with open(obj_path, 'r') as f:
        for line in f:
            if line.startswith('v '):
                vertices.append([float(v) for v in line.strip().split()[1:]])
            elif line.startswith('f '):
                faces.append([int(v.split('/')[0])-1 for v in line.strip().split()[1:]])
    
    vertices = np.array(vertices)
    faces = np.array(faces)
    
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    
    mesh = Poly3DCollection(vertices[faces], alpha=0.5)
    mesh.set_facecolor('cyan')
    ax.add_collection3d(mesh)
    
    # Auto-scale to the mesh size
    scale = vertices.flatten()
    ax.auto_scale_xyz(scale, scale, scale)
    
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    plt.title('3D Model Preview')
    plt.tight_layout()
    plt.show()