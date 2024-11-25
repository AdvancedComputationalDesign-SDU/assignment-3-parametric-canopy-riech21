# Assignment 3: Parametric Structural Canopy Documentation

## Table of Contents

- [Pseudo-Code](#pseudo-code)
- [Technical Explanation](#technical-explanation)
- [Design Variations](#design-variations)
- [Challenges and Solutions](#challenges-and-solutions)
- [References](#references)

---

## Pseudo-Code

1. **Main Function: Generate Fractal Canopy with Recursive Growth**

- **Inputs**
  - `srf`: The base surface for the canopy.
  - `u, v`: Number of divisions along the U and V directions.
  - `gen`: Maximum recursion depth for tree growth.
  - `length`: Initial branch length for trees.
  - `angle`: Maximum rotation angle for branch growth.
  - `s`: Random seed for consistent results.

- **Process**
  - **Generate Depth Map**
    - Apply a sine depth variation to the surface points.
  - **Tessellate Surface**
    - Create a grid of points on the modified surface.
    - Generate polylines along the U and V directions.
    - Create a surface from the adjusted grid of points.
  - **Recursive Tree Growth**
    - Select random starting points from the surface grid.
    - Use a recursive function to grow fractal tree structures from each point.
  - **Create Tessellation Mesh**
    - Define triangular faces using the grid points.
    - Generate a tessellated mesh for the canopy structure.
  - **Outputs**
    - `tessellation_mesh`: The tessellated canopy surface.
    - `lines`: The recursive tree structures.

2. **Functions**

- **`depth_map(x, y)`**
  - *Purpose*: Calculate depth variation using a sine pattern.
  - *Implementation Details*:
    - Compute depth using `2 * sin(2πx) * cos(2πy)`.
    - Return the depth value.

- **`grow(pt, vec, length, g)`**
  - *Purpose*: Recursively generate tree branches.
  - *Implementation Details*:
    - Stop recursion if `g` exceeds `gen`.
    - Generate random rotation axes and angles.
    - Compute endpoints for two branches.
    - Add smooth curves between `pt` and each endpoint.
    - Call `grow` for each branch endpoint with reduced `length` and incremented `g`.

2. **Execution Flow**

- **Setup**
  - Define base surface, parameters (u, v, gen, length, etc.)
- **Generate Surface Grid**
  - Call `depth_map` to modify Z-coordinates.
  - Create grid, polylines, and adjusted surface.
- **Grow Trees**
  - Select random starting points.
  - For each point, call `grow` recursively to create fractal trees.
- **Tessellate and Mesh**
  - Create triangular tessellation from the grid points.
  - Generate a mesh representing the canopy structure.

---

## Technical Explanation

**Depth Map Generation**
The depth map modifies the base surface by applying sine and cosine variations to the Z-coordinate, creating a wavy, dynamic effect. The `depth_map` function computes the depth, where x and y are parametric coordinates of the surface. This wave-like pattern is controlled by the surface domain and grid resolution (`u`, `v` divisions), allowing for precise manipulation of the undulations. The mathematical principles involve trigonometric functions, which introduce periodicity.

**Surface Tessellation**
The tessellation divides the depth-modified surface into a mesh of triangular faces. A grid of points is created by evaluating the surface at uniform parametric intervals and adjusting the Z-values with the depth map. For each grid cell, two triangles are defined to form a quad. This method ensures continuity across the surface and adaptability to non-uniform grids. The resulting tessellation serves as a base for integrating supports.

**Recursive Supports Generation**
The recursive `grow` function generates tree-like support structures. Starting from selected points from the tessellated surface, branches are grown iteratively. Each branch is defined by rotating the growth vector around a randomly chosen axis within a local plane. The recursion depth (`gen`) and branch rotation angle (`angle`) control the complexity and spread of the fractal structure. This approach mimics natural branching patterns.

**Combining Geometries**
The canopy shell and recursive supports are integrated by projecting grid points onto the base surface and anchoring tree roots at selected locations. The smooth blending of tessellation and recursive geometry ensures structural continuity. Challenges include maintaining alignment and selecting anchoring points randomly.

---

## Design Variations

*(Include images and descriptions of your generated design variations. For each category, provide at least three variations and discuss the differences and design decisions.)*

### Base Surface Shape Variations

1. **Variation 1: [Name/Description]**

   ![Canopy Variation 1](images/canopy.jpg)

   - **Parameters**:
     - `control_value`: [Value]
     - Other relevant parameters.

2. **Variation 2: [Name/Description]**

   ![Canopy Variation 2](images/canopy.jpg)

   - **Parameters**:
     - `control_value`: [Value]
     - Other relevant parameters.

3. **Variation 3: [Name/Description]**

   ![Canopy Variation 3](images/canopy.jpg)

   - **Parameters**:
     - `control_value`: [Value]
     - Other relevant parameters.

*(Repeat for Surface Tessellation Pattern and Vertical Supports.)*

---

## Challenges and Solutions

*(Discuss any challenges you faced during the assignment and how you overcame them.)*

### Examples:

- **Challenge 1**: Adapting scripts to Grasshopper.
  - **Solution**: Describe how you addressed this challenge, such as learning the Rhino.Geometry module or adjusting data types.

- **Challenge 2**: Managing data structures.
  - **Solution**: Explain the strategies you used to handle lists and trees in Grasshopper.

- **Challenge 3**: Performance optimization.
  - **Solution**: Discuss how you optimized your code to run efficiently.

---

## References

*(List any resources you used or found helpful during the assignment.)*

- **Python for CAD Applications**:
  - Rhino.Python Guides
  - RhinoScriptSyntax Documentation

- **Grasshopper and GhPython**:
  - Grasshopper Primer
  - GhPython Tutorials

- **Mathematical Functions and Recursion**:
  - Python Math Module
  - Recursion in Python Tutorials

- **Surface Tessellation Techniques**:
  - Voronoi Diagrams
  - Delaunay Triangulation

---

*(Feel free to expand upon these sections to fully capture your work and learning process.)*
