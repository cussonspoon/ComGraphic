import json
from objects import SphereObject

def save_scene(scene, filename="scene.json"):
    data = []
    for obj in scene.objects:
        if hasattr(obj, 'to_dict'):
            data.append(obj.to_dict())
    
    try:
        with open(filename, 'w') as f:
            json.dump(data, f, indent=4)
        print(f"Scene saved to {filename}")
    except Exception as e:
        print(f"Error saving scene: {e}")

def load_scene(scene, filename="scene.json"):
    try:
        with open(filename, 'r') as f:
            data = json.load(f)
        
        scene.objects = [] # Clear current scene
        for item in data:
            if item["type"] == "sphere":
                p = item["pos"]
                c = item["color"]
                # SphereObject(x, y, z, radius, r, g, b, a, shininess, specular)
                obj = SphereObject(
                    p[0], p[1], p[2], 
                    item["radius"], 
                    c[0], c[1], c[2], c[3],
                    item.get("shininess", 30.0),
                    item.get("specular", 0.5)
                )
                scene.add_object(obj)
        print(f"Scene loaded from {filename}")
    except FileNotFoundError:
        print("Save file not found.")
    except Exception as e:
        print(f"Error loading scene: {e}")