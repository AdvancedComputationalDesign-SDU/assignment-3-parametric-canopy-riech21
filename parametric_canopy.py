"""
Assignment 3: Parametric Structural Canopy

Author: Rie Pilgaard Christiansen

Description:
This script generates a parametric structural canopy using depth maps and recursive geometry generation.
It explores different functions to control both the depth map and the fractal geometry to generate a
structural system composed of:
- A shell/gridshell
- A set of vertical supports

The script also combines a strategy for surface tessellation to achieve a non-uniform tessellation
of the input surface.

Note: This script is intended to be used within Grasshopper's Python scripting component.
"""

# Import necessary libraries for the script
import rhinoscriptsyntax as rs  # RhinoScript functions for geometry creation and manipulation
import ghpythonlib.treehelpers as th  # Grasshopper utilities for handling data trees
import math  # For mathematical operations
import random  # For generating random values
import Rhino.Geometry as rg  # Rhino's geometry library (Point3d, curves)

# Define parameters for tree growth
vec = [0, 0, 1]  # Initial growth direction vector (straight up along the Z-axis)
lines = []  # A list to store all the branches of the tree as they are created

# Recursive function to grow the fractal tree
def grow(pt, vec, length, g):
    """
    Recursive function to grow the tree by creating branches at each depth level.

    Args:
    pt: The starting point of the branch.
    vec: The direction vector for growth.
    length: The length of the branch.
    g: The current generation (recursion depth).

    """
    if g < gen:  # Stop recursion if the current generation exceeds the maximum generation
        # Create a local plane at the current point perpendicular to the growth direction
        plane = rs.PlaneFromNormal(pt, vec)
        
        # Select a random point on the plane to define the axis of rotation
        random_pt = rs.EvaluatePlane(plane, [random.uniform(-1, 1), random.uniform(-1, 1)])
        rot_axis = rs.VectorCreate(random_pt, pt)  # Vector from the current point to the random point
        
        # Generate a rotated vector for one branch (negative angle)
        V1 = rs.VectorRotate(vec, random.uniform(-angle, 0), rot_axis)
        pt1 = rs.PointAdd(pt, rs.VectorScale(V1, length))  # Calculate endpoint of this branch
        
        # Define control points for creating a smooth curve (midpoints)
        m1 = [pt[0], pt[1], pt[2] + (pt1[2] - pt[2]) * 0.5]  # Midpoint 1
        m2 = [pt1[0], pt1[1], pt[2] + (pt1[2] - pt[2]) * 0.5]  # Midpoint 2

        # Generate a rotated vector for the other branch (positive angle)
        V2 = rs.VectorRotate(vec, random.uniform(0, angle), rot_axis)
        pt2 = rs.PointAdd(pt, rs.VectorScale(V2, length))  # Calculate endpoint of the second branch
        
        # Define control points for the second curve
        m3 = [pt[0], pt[1], pt[2] + (pt2[2] - pt[2]) * 0.5]  # Midpoint 3
        m4 = [pt2[0], pt2[1], pt[2] + (pt2[2] - pt[2]) * 0.5]  # Midpoint 4

        # Create curves for the two branches and add them to the lines list
        L1 = rs.AddCurve([pt, m1, m2, pt1])  # First branch
        L2 = rs.AddCurve([pt, m3, m4, pt2])  # Second branch

        lines.append(L1)
        lines.append(L2)

        # Recursive calls to grow branches from the endpoints of the current branches
        grow(pt1, V1, length * random.uniform(0.75, 0.95), g + 1)  # Grow from first branch endpoint
        grow(pt2, V2, length * random.uniform(0.75, 0.95), g + 1)  # Grow from second branch endpoint

# Get the U and V domains of the input surface
srf_du = rs.SurfaceDomain(srf, 0)  # Domain of the surface in the U direction
srf_dv = rs.SurfaceDomain(srf, 1)  # Domain of the surface in the V direction

# Define a depth map function to create wave-like deformations in the Z-direction
def depth_map(x, y):
    """
    Compute a wave-like depth based on a sine pattern.
    
    Args:
    x, y: Coordinates within the surface domain.

    Returns:
    A scalar value representing the depth at the given (x, y) position.
    """
    return 2 * math.sin(2 * math.pi * x) * math.cos(2 * math.pi * y)

# Generate a grid of points on the surface, applying depth map transformations
srf_pts = []
for i in range(u + 1):  # Loop through divisions in the U direction
    row = []
    for j in range(v + 1):  # Loop through divisions in the V direction
        # Map grid indices to the surface's parametric domain
        srf_u = srf_du[0] + (i / u) * (srf_du[1] - srf_du[0])
        srf_v = srf_dv[0] + (j / v) * (srf_dv[1] - srf_dv[0])
        
        # Evaluate the surface to find the corresponding 3D point
        tmp_pt = rs.EvaluateSurface(srf, srf_u, srf_v)
        if tmp_pt:
            # Apply the depth map to modify the Z-coordinate
            depth = depth_map(srf_u, srf_v)
            tmp_pt = (tmp_pt[0], tmp_pt[1], tmp_pt[2] + depth)
            tmp_pt = rg.Point3d(tmp_pt[0], tmp_pt[1], tmp_pt[2])  # Convert to Rhino Point3d object
        
        row.append(tmp_pt)  # Add point to the current row
    srf_pts.append(row)  # Add the row to the grid of points

# Generate polylines for visualization along the U and V directions
u_lines = [rs.AddPolyline([pt for pt in row]) for row in srf_pts]  # Polylines along U
v_lines = []
for i in range(len(srf_pts[0])):  # Polylines along V
    tmp_pts = [srf_pts[j][i] for j in range(len(srf_pts))]
    v_lines.append(rs.AddPolyline(tmp_pts))

# Flatten the grid of points and apply a vertical offset for mesh creation
flat_pts = [pt for row in srf_pts for pt in row]  # Flatten the 2D grid into a 1D list
deltaZ = 10  # Vertical offset to lift points in the Z-direction
flat_pts = [rg.Point3d(pt.X, pt.Y, pt.Z + deltaZ) for pt in flat_pts]  # Apply offset

# Select a subset of points from the grid to use as tree starting points
projected_pts = [rg.Point3d(pt.X, pt.Y, 0) for pt in flat_pts]  # Project points to Z=0
selected_pts = random.sample(projected_pts, min(4, len(projected_pts)))  # Select 4 points randomly

# Grow fractal trees from the selected points
for start_point in selected_pts:
    # Create an initial branch for each tree
    B = rs.PointAdd(start_point, rs.VectorScale(vec, length))  # Calculate endpoint of the branch
    lines.append(rs.AddLine(start_point, B))  # Add the branch to the lines list
    random.seed(s)  # Set the random seed for consistent results
    grow(B, vec, length, 0)  # Start the recursive growth process

# Create a new surface using the adjusted grid of points
grid_rows, grid_cols = len(srf_pts), len(srf_pts[0])  # Number of rows and columns in the grid
new_surface = rs.AddSrfPtGrid((grid_rows, grid_cols), flat_pts)  # Generate the surface

# Create a tessellation mesh from the surface points
tessellation_faces = []
for i in range(grid_rows - 1):
    for j in range(grid_cols - 1):
        # Define indices for the corners of each grid cell
        p1_idx = i * grid_cols + j
        p2_idx = i * grid_cols + (j + 1)
        p3_idx = (i + 1) * grid_cols + j
        p4_idx = (i + 1) * grid_cols + (j + 1)
        
        # Define two triangles 
        tessellation_faces.append([p1_idx, p2_idx, p3_idx])  # First triangle
        tessellation_faces.append([p2_idx, p3_idx, p4_idx])  # Second triangle

# Create the mesh object
tessellation_mesh = rs.AddMesh(flat_pts, tessellation_faces)

# Convert the 2D list of surface points to a Grasshopper-compatible data tree
srf_pts_tree = th.list_to_tree(srf_pts)
