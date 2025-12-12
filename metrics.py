import trimesh
import numpy as np
from scipy.spatial import cKDTree
import open3d as o3d
from sklearn.neighbors import KDTree

# ===== Utility functions =====

def sample_points(mesh, n=30000):
    """
    Sample points on a mesh surface and get corresponding face normals.

    Args:
        mesh (trimesh.Trimesh): Input mesh.
        n (int): Number of points to sample.

    Returns:
        tuple: (points, normals)
            - points: ndarray of shape (n, 3)
            - normals: ndarray of shape (n, 3)
    """
    pts, face_idx = trimesh.sample.sample_surface(mesh, n)
    normals = mesh.face_normals[face_idx]
    return pts, normals

def chamfer(mesh_a, mesh_b, samples=30000):
    """
    Compute Chamfer distance between two meshes.
    
    Args:
        mesh_a, mesh_b: trimesh.Trimesh objects
        samples: number of points to sample on each mesh
    
    Returns:
        tuple: (A->B mean, B->A mean, symmetric mean)
    """
    pa, _ = sample_points(mesh_a, samples)
    pb, _ = sample_points(mesh_b, samples)
    ka, kb = cKDTree(pa), cKDTree(pb)
    da,_ = kb.query(pa, k=1)
    db,_ = ka.query(pb, k=1)
    return da.mean(), db.mean(), (da.mean()+db.mean())/2

def hausdorff(mesh_a, mesh_b, samples=30000):
    """
    Compute Hausdorff distance between two meshes.

    Args:
        mesh_a, mesh_b (trimesh.Trimesh): Input meshes.
        samples (int): Number of points to sample from each mesh.

    Returns:
        tuple: (A_to_B_max, B_to_A_max, symmetric_max)
    """
    pa,_ = sample_points(mesh_a, samples)
    pb,_ = sample_points(mesh_b, samples)
    ka, kb = cKDTree(pa), cKDTree(pb)
    da,_ = kb.query(pa, k=1)
    db,_ = ka.query(pb, k=1)
    return da.max(), db.max(), max(da.max(), db.max())
    
def rms_vertex_distance_o3d(mesh_a, mesh_b):
    """
    Compute RMS vertex distance from mesh A to mesh B using Open3D.

    Args:
        mesh_a, mesh_b (trimesh.Trimesh): Input meshes.

    Returns:
        float: Root mean square distance of vertices in mesh A to mesh B surface.
    """
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

    # use point-to-mesh distance by sampling surface of B
    pcd_B = b.sample_points_poisson_disk(50000)
    pts_B = np.asarray(pcd_B.points)

    tree = KDTree(pts_B)

    verts_A = np.asarray(mesh_a.vertices)
    dist, _ = tree.query(verts_A, k=1)

    return float(np.sqrt((dist**2).mean()))

