import pygame
import asyncio
from Apple import Apple
from Ghost import Ghost
from Player import Player
from Button import Button

class Game:
    
    # pygame setup
    def __init__(self):
        pygame.init()
        self.ghost_list : list[Ghost] = []
        self.apple_list : list[Apple] = []
        self.score = 0
        self.mouse_down = False
        self.difficulty = 200
        self.running = True
        self.state = "MENU"
        self.clock = pygame.time.Clock()
        self.hard = 600
        self.medium = 450
        self.easy = 300
        
        


    def setup_and_reset(self):
        self.ghost_list = []
        self.apple_list = []
        self.score = 0
        self.mouse_down = False

    
    async def play(self):
        self.screen = pygame.display.set_mode((1280, 720))
        player = Player(self.screen, 30, 375)
        font = pygame.font.Font('freesansbold.ttf', 28)
        easy_color = "dark red"
        medium_color = "dark red"
        hard_color = "dark red"
        difficulty_color = "grey"
        dt = 0

        while self.running:
            # poll for events
            # pygame.QUIT event means the user clicked X to close your window
            self.mouse_down = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.mouse_down = True

            self.screen.fill("dark grey")

            if self.state == "OPTIONS":
                pygame.mouse.set_visible(True)
                mouse = pygame.mouse.get_pos()

                # EASY
                
                easy_button = Button(self.screen, (self.screen.get_width() / 2, self.screen.get_height() / 2 - 50), 140, 40, font, easy_color)
                easy_button.draw("EASY")
                if easy_button.click():
                    easy_color = "red"
                    if self.mouse_down:
                        self.setup_and_reset()
                        self.state = "RUNNING"
                        player.pos = pygame.Vector2(self.screen.get_width() / 2, self.screen.get_height() / 2)
                        self.difficulty = self.easy
                else:
                    easy_color = "dark red"
                        

                # MEDIUM
                medium_button = Button(self.screen, (self.screen.get_width() / 2, self.screen.get_height() / 2), 
                                       140, 40, font, medium_color)
                medium_button.draw("MEDIUM")
                if medium_button.click():
                    medium_color = "red"
                    if self.mouse_down:
                        self.state = "RUNNING"
                        self.setup_and_reset()
                        player.pos = pygame.Vector2(self.screen.get_width() / 2, self.screen.get_height() / 2)
                        self.difficulty = self.medium
                        
                else:
                    medium_color = "dark red"
                # HARD
                hard_button = Button(self.screen, (self.screen.get_width() / 2, self.screen.get_height() / 2 + 50), 
                                     140, 40, font, hard_color)
                hard_button.draw("HARD")
                if hard_button.click():
                    hard_color = "red"
                    if self.mouse_down:
                        self.state = "RUNNING"
                        self.setup_and_reset()
                        player.pos = pygame.Vector2(self.screen.get_width() / 2, self.screen.get_height() / 2)
                        self.difficulty = self.hard
                else:
                    hard_color = "dark red"

            if self.state == "MENU":
                pygame.mouse.set_visible(True)
                mouse = pygame.mouse.get_pos()
                color = "grey"
                
                if (mouse[0] > self.screen.get_width() / 2 - 70) and mouse[0] < self.screen.get_width() / 2 + 70:
                    if mouse[1] > self.screen.get_height() / 2 and mouse[1] < self.screen.get_height() / 2 + 40:
                        color = "light grey"
                    
                        if self.mouse_down:
                            self.state = 'OPTIONS'                        

                retry_button = pygame.draw.rect(self.screen, color, [self.screen.get_width()/2 - 70,self.screen.get_height()/2,
                                                                     140,40])
                text = font.render("Play", True, (0, 0, 0))
                textRect = text.get_rect()
                
                textRect.center = (self.screen.get_width()/2,self.screen.get_height()/2 + 20)
                self.screen.blit(text, textRect)

            if self.state == 'RUNNING':
            # fill the screen with a color to wipe away anything from last frame
                
                # hide the mouse
                pygame.mouse.set_visible(False)
                
                # player control 
                player.move(dt)

                # spawning ghosts             
                for ghost in self.ghost_list:
                    ghost.state = player.check_collisions(ghost)
                    ghost.draw_ghost()
                    ghost.move(dt)

                    # player movement  
                    player.draw()

                    # ghost edge collision
                    ghost.ghost_boundries()
                   
                    if ghost.state:
                        self.state = 'GAME OVER'
                

                # spawning apples
                if len(self.apple_list) < 5:
                    self.apple_list.append(Apple(pygame, self.screen, self.screen.get_width(), self.screen.get_height(), 15))

                for apple in self.apple_list:
                        apple.draw_apple()
                        apple.state = player.check_collisions(apple)
                        if apple.state:
                            self.apple_list.remove(apple)
                            self.score += 1
                

                # Spawning ghosts 
                if len(self.ghost_list) <= self.score / 3:

                # if pygame.key.get_pressed()[pygame.K_1]:
                    self.ghost_list.append(Ghost(self.screen, 20, "blue", self.difficulty, player.pos))

                # display score 
                score_text = font.render(str(self.score), True, (0, 0, 0))
                score_rect = score_text.get_rect()
                score_rect.center = (self.screen.get_width() / 2, 28)
                
                self.screen.blit(score_text, score_rect)

                # display FPS 
                text = font.render("FPS: " + str(int(self.clock.get_fps())), True, (0, 0, 0))
                textRect = text.get_rect()
                
                textRect.center = (self.screen.get_width() - textRect.left - textRect.right / 2, 20)
                self.screen.blit(text, textRect)

                
                # limits FPS to 60
                # dt is delta time in seconds since last frame, used for framerate-
                # independent physics.
                dt = self.clock.tick(60) / 1000

            if self.state == "GAME OVER":
                pygame.mouse.set_visible(True)
                mouse = pygame.mouse.get_pos()
                color = "grey"
                

                if (mouse[0] > self.screen.get_width() / 2 - 70) and mouse[0] < self.screen.get_width() / 2 + 70:
                    if mouse[1] > self.screen.get_height() / 2 and mouse[1] < self.screen.get_height() / 2 + 40:
                        color = "light grey"
                    
                        if self.mouse_down:
                            self.state = 'RUNNING'
                            self.setup_and_reset()
                            player.pos = pygame.Vector2(self.screen.get_width() / 2, self.screen.get_height() / 2)
                            

                retry_button = pygame.draw.rect(self.screen, color, [self.screen.get_width()/2 - 70, self.screen.get_height()/2, 
                                                                     140,40])
                text = font.render("Retry", True, (0, 0, 0))
                textRect = text.get_rect()
                
                textRect.center = (self.screen.get_width()/2, self.screen.get_height()/2 + 20)
                self.screen.blit(text, textRect)

                change_difficulty_button = Button(self.screen, (self.screen.get_width() / 2, self.screen.get_height() / 2 - 25), 
                                                  140, 40, font, difficulty_color)
                change_difficulty_button.draw("Difficulty")
                if change_difficulty_button.click():
                    difficulty_color = "light grey"
                    if self.mouse_down:
                        self.state = "OPTIONS"
                else:
                    difficulty_color = "grey"

        # flip() the display to put your work on screen  
            pygame.display.flip()
            await asyncio.sleep(0)

        pygame.quit()
