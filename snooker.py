import os, sys, math, pygame, pygame.mixer
import random
import euclid
from pygame.locals import *

black = 0,0,0
white = 255, 255, 255
red = 255,0,0
green = 0,255,0
blue = 0,0,255

initial_velocity = 20

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

    def move(self):
        self.position += self.velocity * dtime_s

    def change_velocity(self, velocity):
        self.velocity = velocity

    def display(self):
        rx, ry = int(self.position.x), int(self.position.y)
        pygame.draw.circle(screen,self.color, (rx, ry), self.radius,self.width)

    def bounce(self):
        if (self.position.x <= self.radius) or (self.position.x >= screen_width - self.radius):
            self.velocity.x = -self.velocity.x

        if (self.position.y <= self.radius) or (self.position.y >= screen_height - self.radius):
            self.velocity.y = -self.velocity.y



def get_random_position():
    x = random.randint(size,screen_width-size)
    y = random.randint(size,screen_width)
    return euclid.Vector2(x,y)

def get_random_velocity():
    angle = random.uniform(0, 2*math.pi)
    vx = math.cos(angle)
    vy = math.sin(angle)
    random_velocity = euclid.Vector2(vx, vy)
    random_velocity *= initial_velocity
    return random_velocity

def update_random_ball_velocity():
    direction_tick = 0
    ball = random.choice(balls)
    new_velocity = get_random_velocity()
    ball.change_velocity(new_velocity)
    



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
size = 10
balls = []

for i in range(num_of_balls):
    color = random.choice(colors)
    width = 1
    position = get_random_position()
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

    #if direction_tick > 0:
    #    update_random_ball_velocity()



    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
    
    # Clear the screen
    screen.lock() # when locked the surface can be modified
    screen.fill(white)

    #border.display()

    for ball in balls:
        ball.move()
        ball.bounce()
        ball.display()

    screen.unlock()
    # Display everything in the screen
    pygame.display.flip()

pygame.quit()
sys.exit()


    




