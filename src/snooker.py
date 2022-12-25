import os, sys, math, random, pygame
from red_ball_positions import get_red_ball_positions
#import pygame.mixer
#from pygame.locals import *

pygame.init()

# Scale up/down of snooker table
SCALE = 3

# Real snooker table dimensions
SNOOKER_TABLE_WIDTH = 360
SNOOKER_TABLE_HEIGHT = 180

screen_size = screen_width, screen_height = SCALE*SNOOKER_TABLE_WIDTH, SCALE*SNOOKER_TABLE_HEIGHT

id = 0

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


initial_velocity = 70
MAX_VELOCITY = 1000
BALL_SIZE = SCALE*3
GAP = 1

colors = [BLACK, RED, GREEN, BLUE]

"""class Border:
    def __init__(self,left=100, top=50, width=236, height=137,color=BLACK):
        self.color = color
        self.left = left
        self.top = top
        self.width = width
        self.height = height
        self.rectangle = pygame.Rect(left, top, width, height)
    
    def display(self):
        pygame.draw.rect(screen, self.color, self.rectangle,width = 1)"""

class Ball:
    def __init__(self, radius, color, position=pygame.math.Vector2(0,0), velocity=pygame.math.Vector2(0,0), width=0):
        self.position = position
        self.velocity = velocity
        self.radius = radius
        self.color = color
        self.width = width
        self.mass = math.pi*self.radius**2
        global id
        self.id = id
        id += 1
        
    
        

    def move(self):
        self.position += self.velocity * dtime_s
        self.collision_with_wall()

    def change_velocity(self, velocity):
        self.velocity = velocity

    def display(self):
        rx, ry = int(self.position.x), int(self.position.y)
        pygame.draw.circle(screen,self.color, (rx, ry), self.radius,self.width)

    def collision_with_wall(self): # simple collision detection
        if (self.position.x <= self.radius) or (self.position.x >= screen_width - self.radius):
            self.velocity.x = -self.velocity.x

        if (self.position.y <= self.radius) or (self.position.y >= screen_height - self.radius):
            self.velocity.y = -self.velocity.y

    def distance_to_other(self, other):
        posA = self.position + self.velocity*dtime_s
        posB = other.position + other.velocity*dtime_s
        distance = (posA - posB).magnitude()
        sumOfRadii = self.radius + other.radius
        return distance - sumOfRadii

    def collide(self, other):
        collision_vector = self.position - other.position
        collision_vector.normalize()
        self.velocity = self.velocity.reflect(collision_vector)
        other.velocity = other.velocity.reflect(collision_vector)

    def velocities_after_collision(self, ball):
        normal = self.position - ball.position
        if normal.magnitude() == 0:
            print("ball in the same position", self.id, ball.id)
        normal.normalize()
        tangent = pygame.math.Vector2(-normal.y, normal.x)
        # tangent components of velocity before and after collision
        v1_tangent = self.velocity.project(tangent)
        v2_tangent = ball.velocity.project(tangent)
        # initial normal components of the velocity
        v1_normal_scalar_0 = self.velocity.dot(normal)
        v2_normal_scalar_0 = self.velocity.dot(normal)  
        combined_mass = ball.mass + self.mass # combined mass of both balls
        # normal components of the velocity after the elastic collision
        v1_normal_scalar = (v1_normal_scalar_0*(self.mass - ball.mass) + 2*ball.mass*v2_normal_scalar_0) / combined_mass
        v2_normal_scalar = (v2_normal_scalar_0*(ball.mass - self.mass) + 2*self.mass*v1_normal_scalar_0) / combined_mass
        # normal components after collision
        v1_normal = v1_normal_scalar * normal
        v2_normal = v2_normal_scalar * normal

        # update velocities
        self.change_velocity(v1_tangent + v1_normal)
        ball.change_velocity(v2_tangent + v2_normal)

    def collision_with_ball(self, other):
        if self.distance_to_other(other) <= 0:
            self.velocities_after_collision(other)


# Setting screen size
screen = pygame.display.set_mode(screen_size)

# Getting Clock object
clock = pygame.time.Clock()

# Setting title to window
pygame.display.set_caption("Snooker!")

# Setting snooker table
"""border  = Border()"""

num_of_balls = 5
balls = []
"""set up of starting position"""
def set_up_background():
    screen.fill(BACKGROUND_GREEN)
    # Baulk Line
    pygame.draw.line(screen, WHITE, (X_BAULK_LINE, 0), (X_BAULK_LINE, screen_height))
    # Baulk D
    pygame.draw.arc(screen, WHITE, (X_BAULK_D, Y_BAULK_D, 2*R_BAULK_D, 2*R_BAULK_D), 1/2 * math.pi, 3/2 * math.pi)
    return

def reset_poisitions():
    pass

"""BALL SETUP"""
# non-red balls
green_ball  = Ball(BALL_SIZE, GREEN, pygame.math.Vector2( X_BAULK_LINE, Y_BAULK_D))
brown_ball  = Ball(BALL_SIZE, BROWN, pygame.math.Vector2( X_BAULK_LINE, screen_height/2))
yellow_ball = Ball(BALL_SIZE, YELLOW, pygame.math.Vector2( X_BAULK_LINE, 2 * Y_BAULK_D))
blue_ball   = Ball(BALL_SIZE, BLUE, pygame.math.Vector2( 1/2 * screen_width, screen_height / 2 ))
pink_ball   = Ball(BALL_SIZE, PINK, pygame.math.Vector2( 3/4 * screen_width, screen_height / 2 ))
black_ball  = Ball(BALL_SIZE, BLACK, pygame.math.Vector2( 7/8 * screen_width, screen_height / 2 ))
# red balls
red_balls = [Ball(BALL_SIZE, RED, pygame.math.Vector2(x,y)) for x,y in get_red_ball_positions(screen_width, screen_height, BALL_SIZE, GAP)] 
# creating a list containing all balls
balls = [green_ball, brown_ball, yellow_ball, blue_ball, pink_ball, black_ball]
balls.extend(red_balls)
# cue ball
#cue_ball = Ball(BALL_SIZE, WHITE, pygame.math.Vector2(X_BAULK_D, screen_height / 2), pygame.math.Vector2(100,0))
#balls.append(cue_ball)
direction_tick = 0

# Defining variables for fps and running
fps_limit = 60
run = True
while run:
    # limit the framerate
    dtime_ms = clock.tick(fps_limit)
    dtime_s = dtime_ms / 1000

    direction_tick += dtime_s

    #if direction_tick > 1:
    #    direction_tick = 0
    #    update_random_ball_velocity()



    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
    # Clear the screen
    screen.lock() # when locked the surface can be modified
    set_up_background()

    #border.display()

    # check for collision between balls
    for i, ball_1 in enumerate(balls):
        ball_1.move()
        for ball_2 in balls[i+1:]:
            ball_1.collision_with_ball(ball_2)
        ball_1.display()

    screen.unlock()
    # Display everything in the screen
    pygame.display.flip()

pygame.quit()
sys.exit()


    




