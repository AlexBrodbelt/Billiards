import os, sys, math, random, pygame, itertools
from red_ball_positions import get_red_ball_positions
from collision_detection import sweep_and_prune
from regions import get_region
from constants import *
#import pygame.mixer
#from pygame.locals import *

pygame.init()

id = 0 # a counter that asigns an iuseful for debugging purposes 

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
    id_iter = itertools.count()
    def __init__(self, radius, color, position=pygame.math.Vector2(0,0), velocity=pygame.math.Vector2(0,0), id=None, width=0):
        self.radius = radius
        self.color = color
        self.position = position
        self.reset_position = position # useful to reset the position of the ball
        self.velocity = velocity
        self.width = width
        self.mass = 1 # math.pi*self.radius**2
        self.id = id if id else next(Ball.id_iter)
        print(self.id)
        
    def move(self):
        self.position += self.velocity * dtime_s
        #self.friction()
        self.collision_with_wall()
        
    def friction(self, dtime):
        """method to take cloth-ball friction into account"""
        friction_coefficient = 0.2 # friction
        stopping_threshold = 5**2
        if self.velocity.magnitude_squared() != 0:
            self.velocity -= self.velocity * (friction_coefficient * dtime) # a * dt = (F / m) * dt = dv/dt * dt
            if self.velocity.magnitude_squared() <= stopping_threshold: 
                print("ball", self.id, "is stationary")
                self.velocity.update(0,0) 

    def change_velocity(self, velocity):
        self.velocity = velocity

    def display(self):
        rx, ry = int(self.position.x), int(self.position.y)
        pygame.draw.circle(screen, self.color, (rx, ry), self.radius, self.width)

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

    def velocities_after_collision(self, other):
        normal = (self.position - other.position).normalize() # vector from center of one ball to the center of the other ball
        if normal.magnitude() == 0:
            run = False
            raise ValueError(f"balls {self.id} and {other.id} are in the same position")
        tangent = pygame.math.Vector2(-normal.y, normal.x)
        # tangent components of velocity before and after collision
        v1_tangent = self.velocity.project(tangent)
        v2_tangent = other.velocity.project(tangent)
        # initial normal components of the velocity
        v1_normal_scalar_0 = self.velocity.dot(normal)
        v2_normal_scalar_0 = other.velocity.dot(normal)  
        combined_mass = other.mass + self.mass # combined mass of both balls
        # normal components of the velocity after the elastic collision
        v1_normal_scalar = (v1_normal_scalar_0*(self.mass - other.mass) + 2*other.mass*v2_normal_scalar_0) / combined_mass
        v2_normal_scalar = (v2_normal_scalar_0*(other.mass - self.mass) + 2*self.mass*v1_normal_scalar_0) / combined_mass
        # normal components after collision
        v1_normal = v1_normal_scalar * normal
        v2_normal = v2_normal_scalar * normal

        # update velocities
        self.change_velocity(v1_tangent + v1_normal)
        other.change_velocity(v2_tangent + v2_normal)

    def collision_with_ball(self, other):
        if self.distance_to_other(other) <= 0:
            self.velocities_after_collision(other)
        
class Cue_ball(Ball):
    pass


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

def reset_positions():
    pass

def set_up_cue_ball(position, in_game): # must correct ids
    global balls
    if len(balls) == 22: # all balls are placed
                balls.pop()
    pos = pygame.mouse.get_pos()
    region  = get_region(pos)
    if region == INSIDE_BAULK_D: # pre-visualize where the cue ball is placed
        cue_ball = Ball(BALL_SIZE, WHITE, pos)
        balls.append(cue_ball)
        #state = PLAYING
    if pygame.mouse.get_pressed() == (1,0,0): # set the cue ball to the position
        state = PLAYING
    
    




"""BALL SETUP"""
# non-red balls
green_ball  = Ball(BALL_SIZE, GREEN, pygame.math.Vector2( X_BAULK_LINE, Y_BAULK_D))
brown_ball  = Ball(BALL_SIZE, BROWN, pygame.math.Vector2( X_BAULK_LINE, screen_height/2))
yellow_ball = Ball(BALL_SIZE, YELLOW, pygame.math.Vector2( X_BAULK_LINE, 2 * Y_BAULK_D))
blue_ball   = Ball(BALL_SIZE, BLUE, pygame.math.Vector2( 1/2 * screen_width, screen_height / 2 ))
pink_ball   = Ball(BALL_SIZE, PINK, pygame.math.Vector2( 3/4 * screen_width, screen_height / 2 ))
black_ball  = Ball(BALL_SIZE, BLACK, pygame.math.Vector2( 7/8 * screen_width, screen_height / 2 ))
# red balls
red_balls = [ Ball(BALL_SIZE, RED, pygame.math.Vector2(x + GAP ,y)) for x,y in get_red_ball_positions(screen_width, screen_height, BALL_SIZE, GAP) ] 
# creating a list containing all balls
balls = [green_ball, brown_ball, yellow_ball, blue_ball, pink_ball, black_ball]
balls.extend(red_balls)
# cue ball
cue_ball = Ball(BALL_SIZE, WHITE, pygame.math.Vector2(X_BAULK_D, screen_height / 2), pygame.math.Vector2(300,0), id=22)
balls.append(cue_ball)

# Defining variables for fps and running
fps_limit = 60
run = True
state = PLAYING
while run:
    # limit the framerate
    dtime_ms = clock.tick(fps_limit)
    dtime_s = dtime_ms / 1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        
        if state == CUE_BALL_SETUP: #  and 
            if len(balls) == 22: # all balls are placed
                balls.pop()
            pos = pygame.mouse.get_pos()
            region  = get_region(pos)
            if region == INSIDE_BAULK_D:
                cue_ball = Ball(BALL_SIZE, WHITE, pos)
                balls.append(cue_ball)
                #state = PLAYING
            if pygame.mouse.get_pressed() == (1,0,0):
                #cue_ball.change_velocity(pygame.math.Vector2(300,0))
                state = PLAYING
            #print(f"inside region {region}") 
    
    # Clear the screen
    screen.lock() # when locked the surface can be modified
    set_up_background()

    #border.display()

    # update position of balls
    for i, ball in enumerate(balls):
        ball.move()
        ball.friction(dtime_s)
        for other in balls[i+1:]: # update velocity of balls
            ball.collision_with_ball(other)
        ball.display()

    # update velocity of balls
    """for i, j in sweep_and_prune(balls):
        ball = balls[i]
        other = balls[j]
        ball.collision_with_ball(other)"""

    screen.unlock()
    # Display everything in the screen
    pygame.display.flip()

pygame.quit()
sys.exit()


    




