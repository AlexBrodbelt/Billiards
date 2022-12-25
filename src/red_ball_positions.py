
import math

def get_red_ball_at(screen_width, screen_height, index, level, radius, GAP):
    x_offset = 3/4 * screen_width
    y_offset = 1/2 * screen_height
    x = x_offset + math.sqrt(3)*(radius + GAP)*(level+1) # level: from left to right ; index: from down to up
    y = y_offset + (2*index - level) * (radius + GAP)
    return x, y

def get_red_ball_positions(screen_width, screen_height, radius, GAP):
    positions = []
    for level in range(5):
        for index in range(level + 1):
            positions.append(get_red_ball_at(screen_width, screen_height, index, level, radius, GAP))
    return positions

if __name__ == "__main__":
    GAP = 1
    screen_height = 180
    screen_width = 360
    radius  = 5
    red_balls = get_red_ball_positions(screen_width, screen_height, radius, GAP)
