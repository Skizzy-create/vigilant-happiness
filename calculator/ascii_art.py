import random

def draw_city_skyline():
    """Procedurally generates a city skyline."""
    width = 50
    height = 20
    skyline = [[' ' for _ in range(width)] for _ in range(height)]
    
    # Draw buildings
    x = 0
    while x < width:
        b_width = random.randint(3, 8)
        b_height = random.randint(5, 18)
        
        # Draw building
        for i in range(height - b_height, height):
            for j in range(x, min(x + b_width, width)):
                if j == x or j == min(x + b_width - 1, width - 1) or i == height - b_height:
                    skyline[i][j] = '#'
                else:
                    # Add windows
                    if random.random() > 0.7:
                        skyline[i][j] = '.'
                    else:
                        skyline[i][j] = '|'
        x += b_width + 1
        
    return "\n".join(["".join(row) for row in skyline])

def draw_tree():
    """Procedurally generates a tree."""
    width = 40
    height = 20
    canvas = [[' ' for _ in range(width)] for _ in range(height)]
    
    # Trunk
    trunk_x = width // 2
    for i in range(height - 5, height):
        canvas[i][trunk_x] = '|'
        
    # Branches
    for i in range(height - 10, height - 5):
        spread = (height - i) // 2
        for j in range(trunk_x - spread, trunk_x + spread + 1):
            if random.random() > 0.3:
                canvas[i][j] = '*'
                
    return "\n".join(["".join(row) for row in canvas])

if __name__ == "__main__":
    print("--- Procedural City Skyline ---")
    print(draw_city_skyline())
    print("\n--- Procedural Tree ---")
    print(draw_tree())
