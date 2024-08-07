import pygame
from pygame import Vector2 
from pygame import display

class Player:
    def __init__(self, screen, radius, speed) -> None:
        self.screen : display  = screen
        self.pos : Vector2 = Vector2(self.screen.get_width() / 2, self.screen.get_height() / 2)
        self.color = "dark green"
        self.radius = radius
        self.speed : float|int = speed
        self.width = self.screen.get_width()
        self.height = self.screen.get_height()
    
    def draw(self):
        pygame.draw.circle(self.screen, self.color, self.pos, self.radius)

    def check_collisions(self, other):
        if self.pos.distance_to(other.pos) < self.radius + other.radius:
            return True
        return False
    
    def move(self, dt):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and (self.pos.y - (self.speed * dt) > self.radius):
            self.pos.y -= self.speed * dt
        if keys[pygame.K_s] and (self.pos.y + (self.speed * dt) < self.height - self.radius):
            self.pos.y += self.speed * dt
        if keys[pygame.K_a] and (self.pos.x - (self.speed * dt) > self.radius):
            self.pos.x -= self.speed * dt
        if keys[pygame.K_d] and (self.pos.x + (self.speed * dt) < self.width - self.radius):
            self.pos.x += self.speed * dt