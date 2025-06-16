def get_depth(coord):
    depth_map = {
        (0, 5): 3500,
        (-1, 4): 3500,
        (3, 2): 4000,
        (3, 3): 4000,
        (-2, 1): 4500,
        (-1, 2): 3700
    }
    
    return depth_map.get(coord, "Depth not found")  # Returns depth if found, otherwise a default message

# Example usage
coord = (-2, 1)  # Example input as a tuple
print(get_depth(coord))
