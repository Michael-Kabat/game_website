import random
from pygame import Vector2

class Apple:
    def __init__(self, pygame, screen, width, height, radius) -> None:
        self.pygame = pygame
        self.screen = screen
        self.radius = radius
        self.color = "dark red"
        self.state = True

        self.pos = Vector2(random.randint(self.radius, width - self.radius), 
                           random.randint(self.radius, height - self.radius))
        

        
    
    def draw_apple(self):
        self.pygame.draw.circle(self.screen, self.color, self.pos, self.radius)