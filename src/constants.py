# Scale up/down of snooker table
SCALE = 3

# Real snooker table dimensions
SNOOKER_TABLE_WIDTH = 360
SNOOKER_TABLE_HEIGHT = 180

screen_size = screen_width, screen_height = SCALE*SNOOKER_TABLE_WIDTH, SCALE*SNOOKER_TABLE_HEIGHT

# States - FSM
CUE_BALL_SETUP = 0
PLAYING = 1

IN_GAME = False




# Color Palette
BLACK = 0, 0, 0
WHITE = 255, 255, 255
YELLOW = 255, 174, 66
RED = 255, 0, 0
BLUE = 0, 0, 255
GREEN = 0, 255, 0
PINK = 255, 20, 147
BROWN = 139, 69, 19
BACKGROUND_GREEN = 10, 108, 3

# Snooker table features
X_BAULK_LINE = screen_width / 5 # x coordinate for Baulk Line
R_BAULK_D = screen_height / 6 # radius of Baulk D
X_BAULK_D = X_BAULK_LINE - R_BAULK_D
Y_BAULK_D = screen_height / 3

# table regions
RIGHT_OF_BAULK_LINE = 1
OUTSIDE_BAULK_D = 2 # to the left of baulk line
INSIDE_BAULK_D = 3

initial_velocity = 70
MAX_VELOCITY = 1000
BALL_SIZE = SCALE*3 # size of balls
GAP = 1 # gap between balls

colors = [BLACK, RED, GREEN, BLUE]