# 3D Mesh Metrics

Compute widely used 3D mesh similarity metrics between two meshes:

* Chamfer Distance (CD)
* Hausdorff Distance (HD)
* RMS Vertex Distance (Open3D)

## Installation

```bash
pip install trimesh numpy scipy open3d scikit-learn
```

## Usage

Place your meshes in the working directory:

```python
import trimesh
from metrics import chamfer, hausdorff, rms_vertex_distance_o3d

# Load meshes
A = trimesh.load("01.stl", process=True)
B = trimesh.load("01_m.stl", process=True)

# Compute metrics
print("Chamfer Distance:", chamfer(A, B))
print("Hausdorff Distance:", hausdorff(A, B))
print("RMS Vertex Distance:", rms_vertex_distance_o3d(A, B))
```

## License

**© 2025 Sonain Jamil and Yaseen. All rights reserved.**
