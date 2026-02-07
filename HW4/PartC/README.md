# OpenGL Interactive Scene Editor (HW Challenge)

## How to Run
1. Ensure `floor.jpg` (or any image) is in the same folder.
2. Install dependencies: `pip install pygame PyOpenGL Pillow`.
3. Run: `python main.py`

## Controls
### General
* **Add Object**: Press **'A'** to spawn a random sphere.
* **Select Object**: Left Click on a sphere.
* **Save Scene**: `Ctrl + S`
* **Load Scene**: `Ctrl + L`

### Camera Controls (Camera Mode)
* **Orbit Camera**: Left Click + Drag.
* **Pan Camera**: Shift + Left Click + Drag.
* **Zoom**: Scroll Wheel.

### Mode Switching
* **TAB**: Toggle between **Camera Mode** and **Light Mode**.
* (Check Window Title bar to see current mode and light position).

### Object Transformation (When Object Selected)
* **I / K**: Move Z-axis (Forward/Back).
* **J / L**: Move X-axis (Left/Right).
* **U / O**: Move Y-axis (Up/Down).
* **Shift + Key**: Fine control (slower movement).

### Light Control (In Light Mode)
* **Arrow Keys**: Move Light X/Z.
* **Q / E**: Move Light Y (Up/Down).

## Implementation Details

### Picking / Selection
Picking is implemented in `picking.py`. We use `gluUnProject` to convert the 2D mouse screen coordinates into two 3D points: one on the "near" clipping plane and one on the "far" clipping plane. We construct a ray vector between these points. We then iterate through all spheres in the scene and perform a mathematical Ray-Sphere intersection test. The sphere with the smallest intersection distance is marked as `selected`.

### Transparency Sorting
To ensure transparent objects look correct (alpha blending), we cannot rely on the Z-buffer alone. In `scene.py`, the `draw()` function performs the following steps:
1.  Render all **opaque** objects first (writing to the depth buffer).
2.  Render the floor.
3.  Calculate the distance from the camera to every **transparent** object.
4.  **Sort** the transparent objects from furthest to nearest (descending distance).
5.  Render the sorted transparent objects with `glDepthMask(GL_FALSE)` so they blend without occluding each other in the depth buffer.