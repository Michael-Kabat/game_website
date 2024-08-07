import pygame
from pygame import Vector2
import random

class Ghost:

    def __init__(self, screen, radius, color, speed, player_pos) -> None:
        self.screen : pygame.display = screen
        self.radius = radius
        self.color = color
        self.state = False
        self.velocity : Vector2 = Vector2(random.randint(-speed, speed), random.randint(-speed, speed))
        rand_x = self.random_exclusion(self.radius * 2, self.screen.get_width() - self.radius * 2, 
                                       [x for x in range(int(player_pos.x - 50), int(player_pos.x + 50))])
        
        rand_y = self.random_exclusion(self.radius * 2, self.screen.get_height() - self.radius * 2, 
                                        [x for x in range(int(player_pos.y - 50), int(player_pos.y + 50))])
                                        
        self.pos : Vector2 = pygame.Vector2(rand_x, rand_y)
        
    def random_exclusion(self, start, stop, excluded) -> int:
        excluded = set(excluded)
        value = random.randint(start, stop - len(excluded))
        for exclusion in tuple(excluded):
            if value < exclusion:
                break
            value += 1
        return value
    
    def ghost_boundries(self):
        if self.pos.x < self.radius or self.pos.x > self.screen.get_width() - self.radius:
            self.velocity.x *= -1
        if self.pos.y < self.radius or self.pos.y > self.screen.get_height() - self.radius:
            self.velocity.y *= -1

    def move(self, dt):
        if dt  > 0.1:
            return
        self.pos += self.velocity * dt


    def draw_ghost(self):
        pygame.draw.circle(self.screen, self.color, self.pos, self.radius)
        

