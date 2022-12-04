
import math

def get_red_ball_at(screen_width, screen_height, index, level, radius, GAP):
    x = 3/4 * screen_width + math.sqrt(3)/2*(radius+ GAP)*level
    y = 1/2 * screen_height + (2*index - level) * (radius + GAP)
    return x, y

def get_red_ball_positions(screen_width, screen_height, radius, GAP):
    positions = []
    for level in range(1,6):
        for index in range(level):
            positions.append(get_red_ball_at(screen_width, screen_height, level, index, radius, GAP))
    return positions

if __name__ == "__main__":
    GAP = 1
    screen_height = 180
    screen_width = 360
    radius  = 5
    red_balls = get_red_ball_positions(screen_width, screen_height, radius, GAP)
