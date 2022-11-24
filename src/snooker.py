import os, sys, math, pygame, pygame.mixer
import random
import euclid
import itertools
from pygame.locals import *

black = 0,0,0
white = 255, 255, 255
red = 255, 0, 0
green = 0,255,0
blue = 0,0,255

initial_velocity = 50

MAX_VELOCITY = 1000

colors = [black, red, green, blue]

class Border:
    def __init__(self,left=100, top=50, width=236, height=137,color=black):
        self.color = color
        self.left = left
        self.top = top
        self.width = width
        self.height = height
        self.rectangle = pygame.Rect(left,top,width,height)
    
    def display(self):
        pygame.draw.rect(screen, self.color, self.rectangle,width = 1)

class Ball:
    def __init__(self, radius, color, width,position=euclid.Vector2(0,0), velocity=euclid.Vector2(0,0)):
        self.position = position
        self.velocity = velocity
        self.radius = radius
        self.color = color
        self.width = width
        self.mass = math.pi*self.radius**2

    def move(self):
        self.position += self.velocity * dtime_s
        self.collisionWithWall()

    def change_velocity(self, velocity):
        self.velocity = velocity

    def display(self):
        rx, ry = int(self.position.x), int(self.position.y)
        pygame.draw.circle(screen,self.color, (rx, ry), self.radius,self.width)

    def collisionWithWall(self): # simple collision detection
        if (self.position.x <= self.radius) or (self.position.x >= screen_width - self.radius):
            self.velocity.x = -self.velocity.x

        if (self.position.y <= self.radius) or (self.position.y >= screen_height - self.radius):
            self.velocity.y = -self.velocity.y

    def velocitiesAfterCollision(self, ball):
        normal = self.velocity - ball.velocity
        normal.normalize()
        tangent = euclid.Vector2(-normal.y, normal.x)

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

    def collisionWithBall(self, ball):
        distance = (self.position - ball.position).magnitude()
        if distance <= self.radius + ball.radius:
            self.velocitiesAfterCollision(ball)




def get_random_position(size):
    x = random.randint(size,screen_width-size)
    y = random.randint(size,screen_height-size)
    return euclid.Vector2(x,y)

def get_random_velocity():
    angle = random.uniform(0, 2*math.pi)
    vx = math.cos(angle)
    vy = math.sin(angle)
    random_velocity = euclid.Vector2(vx, vy)
    random_velocity *= initial_velocity
    return random_velocity

def update_random_ball_velocity():
    ball = random.choice(balls)
    new_velocity = get_random_velocity()
    ball.change_velocity(new_velocity)

def scanPotentialCollisions():
    for ball1, ball2 in itertools.combinations(balls, 2):
        ball1.collisionWithBall(ball2)



screen_size = screen_width, screen_height = 600, 400

# Setting screen size
screen = pygame.display.set_mode(screen_size)

# Getting Clock object
clock = pygame.time.Clock()

# Setting title to window
pygame.display.set_caption("Snooker!")

# Setting snooker table
border  = Border()

num_of_balls = 10
balls = []

for i in range(num_of_balls):
    color = random.choice(colors)
    width = 1
    size = random.randint(10,40)
    position = get_random_position(size)
    velocity = get_random_velocity()
    ball = Ball(size,color,width, position,velocity)
    balls.append(ball)

direction_tick = 0

# Defining variables for fps and running
fps_limit = 60
run = True
while run:
    # limit the framerate
    dtime_ms = clock.tick(fps_limit)
    dtime_s = dtime_ms / 1000

    direction_tick += dtime_s

    if direction_tick > 1:
        direction_tick = 0
        update_random_ball_velocity()



    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
    # Clear the screen
    screen.lock() # when locked the surface can be modified
    screen.fill(white)

    #border.display()

    # check for collision between balls
    #scanPotentialCollisions()

    for ball in balls:
        ball.move()
        ball.display()

    screen.unlock()
    # Display everything in the screen
    pygame.display.flip()

pygame.quit()
sys.exit()


    




