import numpy as np

def generate_wbt(wall_matrix):
    cell_size = 1  # Define the cell size
    walls = []
    wbt_content = ""

    rows, cols = wall_matrix.shape
    for r in range(rows):
        for c in range(cols):
            walls_4bit = wall_matrix[r, c]
            x, z = c * cell_size, r * cell_size

            if walls_4bit[0] == '1':
                walls.append(f"Solid {{\n  translation {x} 0 {z + cell_size / 2}\n  size {cell_size} 0.1 0.1\n  children [\n    Shape {{\n      appearance Appearance {{\n        material Material {{\n          diffuseColor 0.5 0.5 0.5\n        }}\n      }}\n      geometry Box {{ }}\n    }}\n  ]\n}}\n")
            if walls_4bit[1] == '1':
                walls.append(f"Solid {{\n  translation {x + cell_size / 2} 0 {z}\n  size 0.1 0.1 {cell_size}\n  children [\n    Shape {{\n      appearance Appearance {{\n        material Material {{\n          diffuseColor 0.5 0.5 0.5\n        }}\n      }}\n      geometry Box {{ }}\n    }}\n  ]\n}}\n")
            if walls_4bit[2] == '1':
                walls.append(f"Solid {{\n  translation {x} 0 {z - cell_size / 2}\n  size {cell_size} 0.1 0.1\n  children [\n    Shape {{\n      appearance Appearance {{\n        material Material {{\n          diffuseColor 0.5 0.5 0.5\n        }}\n      }}\n      geometry Box {{ }}\n    }}\n  ]\n}}\n")
            if walls_4bit[3] == '1':
                walls.append(f"Solid {{\n  translation {x - cell_size / 2} 0 {z}\n  size 0.1 0.1 {cell_size}\n  children [\n    Shape {{\n      appearance Appearance {{\n        material Material {{\n          diffuseColor 0.5 0.5 0.5\n        }}\n      }}\n      geometry Box {{ }}\n    }}\n  ]\n}}\n")

    # Add all walls to the .wbt content
    wbt_content += "\n".join(walls)

    return wbt_content

# Example usage (replace `wall_matrix` with the actual 4-bit binary representation):
wall_matrix = np.array([["1111", "1010"], ["0101", "0000"]])
  # Placeholder for demonstration
# wall_matrix = np.array(["".join(map(str, row)) for row in wall_matrix])
wbt_content = generate_wbt(wall_matrix)

# Save to file
with open("maze.wbt", "w") as f:
    f.write(wbt_content)

print("maze.wbt file generated successfully!")