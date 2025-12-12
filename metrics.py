import trimesh
import numpy as np
from scipy.spatial import cKDTree

# ===== Utility functions =====
def sample_points(mesh, n=30000):
    pts, face_idx = trimesh.sample.sample_surface(mesh, n)
    normals = mesh.face_normals[face_idx]
    return pts, normals

def chamfer(mesh_a, mesh_b, samples=30000):
    pa, _ = sample_points(mesh_a, samples)
    pb, _ = sample_points(mesh_b, samples)
    ka, kb = cKDTree(pa), cKDTree(pb)
    da,_ = kb.query(pa, k=1)
    db,_ = ka.query(pb, k=1)
    return da.mean(), db.mean(), (da.mean()+db.mean())/2

def hausdorff(mesh_a, mesh_b, samples=30000):
    pa,_ = sample_points(mesh_a, samples)
    pb,_ = sample_points(mesh_b, samples)
    ka, kb = cKDTree(pa), cKDTree(pb)
    da,_ = kb.query(pa, k=1)
    db,_ = ka.query(pb, k=1)
    return da.max(), db.max(), max(da.max(), db.max())

def rms_vertex_distance_o3d(mesh_a, mesh_b):
    import open3d as o3d

    a = o3d.geometry.TriangleMesh(
        vertices=o3d.utility.Vector3dVector(np.asarray(mesh_a.vertices)),
        triangles=o3d.utility.Vector3iVector(np.asarray(mesh_a.faces))
    )
    b = o3d.geometry.TriangleMesh(
        vertices=o3d.utility.Vector3dVector(np.asarray(mesh_b.vertices)),
        triangles=o3d.utility.Vector3iVector(np.asarray(mesh_b.faces))
    )
    a.compute_vertex_normals()
    b.compute_vertex_normals()

    pcd_B = b.sample_points_poisson_disk(50000)
    pts_B = np.asarray(pcd_B.points)

    from sklearn.neighbors import KDTree
    tree = KDTree(pts_B)

    verts_A = np.asarray(mesh_a.vertices)
    dist, _ = tree.query(verts_A, k=1)

    return float(np.sqrt((dist**2).mean()))

# ===== Load your two meshes and compute metrics =====
A = trimesh.load("01.stl", process=True)
B = trimesh.load("01_m.stl", process=True)

print("=== 3D METRIC RESULTS ===\n")
print("Chamfer Distance (A→B, B→A, sym):")
print(chamfer(A, B))

print("\nHausdorff Distance (A→B, B→A, sym):")
print(hausdorff(A, B))

print("\nRMS Vertex Distance (Open3D):")
print(rms_vertex_distance_o3d(A, B))
