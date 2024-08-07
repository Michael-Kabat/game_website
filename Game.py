import json
import sys
import pygame
from Apple import Apple
from Ghost import Ghost
from Player import Player
from Button import Button

DIFFICULTY_CONVERTER = {300: "Easy", 450: "Medium", 600: "Hard"}

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
        self.easy_high_score = 0
        self.medium_high_score = 0
        self.hard_high_score = 0
        self.name = ''
        


    def setup_and_reset(self):
        self.ghost_list = []
        self.apple_list = []
        self.score = 0
        self.mouse_down = False

    
    #async def play(self):
    def play(self):
        # variable inits
        leaderboard = []
        

        self.screen = pygame.display.set_mode((1280, 720))
        player = Player(self.screen, 30, 375)
        font = pygame.font.Font('freesansbold.ttf', 28)
        easy_color = "dark red"
        medium_color = "dark red"
        hard_color = "dark red"
        difficulty_color = "dark grey"
        retry_color = "dark grey"
        resume_color = "grey"
        quit_color = "grey"
        play_color = "grey"
        name_text_color = "grey"
        exit_color = "grey"
        user_input = "Name: "
        dt = 0
        background_color = "grey"
        typing = False
        # Game Loop
        while self.running:
            # poll for events
            # pygame.QUIT event means the user clicked X to close your window
            self.mouse_down = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN: 
                    self.mouse_down = True

                if event.type == pygame.KEYDOWN:
                    if typing:
                        if user_input == "Name: ":
                            user_input = ''
                            
                        if event.key == pygame.K_BACKSPACE:
                            user_input = user_input[:-1]
                        else:
                            user_input += event.unicode

            self.screen.fill(background_color)

            if self.state == "MENU":
                pygame.mouse.set_visible(True)
                play_button = Button(self.screen, (self.screen.get_width() / 2, self.screen.get_height() / 2 - 50), 
                                     140, 40, font, play_color)
                
                play_button.draw('Play')
                
                if play_button.click():
                    play_color = "light grey"
                    if self.mouse_down:
                        self.state = "OPTIONS"
                        self.mouse_down = False
                        self.name = user_input
                else:
                    play_color = "dark grey"                
                

                name_text = Button(self.screen, (self.screen.get_width() / 2, self.screen.get_height() / 2), 
                                     140, 40, font, name_text_color)
                

                name_text.draw(user_input)

                if name_text.click():
                    name_text_color = "light grey"
                    if self.mouse_down:
                        typing = True
                else:
                    if self.mouse_down:
                        typing = False
                    name_text_color = "dark grey"



                exit_button = Button(self.screen, (self.screen.get_width() / 2, self.screen.get_height() / 2 + 50), 
                                     140, 40, font, exit_color)
                exit_button.draw("Quit")
                
                if exit_button.click():
                    exit_color = "light grey"
                    if self.mouse_down:
                        self.state = "QUIT"
                        self.mouse_down = False
                else:
                    exit_color = "dark grey"

            if self.state == "PAUSED":
                pygame.mouse.set_visible(True)
                player.draw()
                for ghost in self.ghost_list:
                    ghost.draw_ghost()
                for apple in self.apple_list:
                        apple.draw_apple()


                resume_button = Button(self.screen, (self.screen.get_width() / 2, self.screen.get_height() / 2 - 25), 
                                                  140, 40, font, resume_color)
                resume_button.draw("Resume")

                if resume_button.click():
                    resume_color = "light grey"
                    if self.mouse_down:
                        self.state = "RUNNING"
                        background_color = "grey"
                        self.mouse_down = False
                else:
                    resume_color = "grey"

                quit_button = Button(self.screen, (self.screen.get_width() / 2, self.screen.get_height() / 2 + 25), 
                                                  140, 40, font, quit_color)
                quit_button.draw("Menu")

                if quit_button.click():
                    quit_color = "light grey"
                    if self.mouse_down:
                        self.state = "MENU"
                        background_color = "grey"
                        self.mouse_down = False
                else: 
                    quit_color = "grey"
            
            if self.state == "QUIT":
                 self.screen.fill("black")
                 self.running = False

            if self.state == "OPTIONS":
                pygame.mouse.set_visible(True)

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
                        self.mouse_down = False
                        try:
                            with open('easy_leaderboard.json', 'r') as l:
                                leaderboard = json.load(l)
                        except:
                            pass
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
                        self.mouse_down = False
                        try:
                            with open('medium_leaderboard.json', 'r') as t:
                                leaderboard = json.load(t)
                                print("leaderboard is medium ")
                        except:
                            pass
                        
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
                        self.mouse_down = False
                        try:
                            with open('hard_leaderboard.json', 'r') as f:
                                leaderboard = json.load(f)
                        except:
                            pass
                else:
                    hard_color = "dark red"
                
            if self.state == 'RUNNING':
            # fill the screen with a color to wipe away anything from last frame
                
                keys = pygame.key.get_pressed()
                if keys[pygame.K_ESCAPE]:
                    self.state = "PAUSED"
                    background_color = "dark grey"

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
                        #if self.score > leaderboard[-1]['score'] if leaderboard else self.score > 0:
                        name_found = False
                        for i in range(len(leaderboard)):
                            
                            if self.name == leaderboard[i]["name"]:
                                name_found = True
                                if self.score > leaderboard[i]["score"]:
                                    leaderboard[i] = ({'name': self.name, "Difficulty": DIFFICULTY_CONVERTER[self.difficulty], 'score': self.score})
                                    leaderboard.sort(key=lambda x: x['score'], reverse=True)
                                #leaderboard = leaderboard[:5]
                        if not name_found:
                            leaderboard.append({'name': self.name, "Difficulty": DIFFICULTY_CONVERTER[self.difficulty], 'score': self.score})
                        
                        file_name = ''
                        if self.difficulty == self.easy:
                            file_name = "easy_leaderboard.json"
                        if self.difficulty == self.medium:
                            file_name = "medium_leaderboard.json"
                        if self.difficulty == self.hard:
                            file_name = "hard_leaderboard.json"

                        with open(file_name, 'w') as f:
                            json.dump(leaderboard, f)

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

                leaderboard_text = ''
                for i, entry in enumerate(leaderboard):
                    if i <= 5:
                        leaderboard_text += f'{i + 1}. {entry["name"]}: {entry["score"]} on {entry["Difficulty"]}, '
                leaderboard_text = leaderboard_text.rstrip()
                leaderboard_rect = self.screen.get_rect(center=(self.screen.get_width() / 2, self.screen.get_height()/ 2))
                leaderboard_surface = font.render(leaderboard_text, True, (0,0,0))
                self.screen.blit(leaderboard_surface, leaderboard_rect)

                retry_button = Button(self.screen, (self.screen.get_width() / 2, self.screen.get_height() / 2 + 25), 
                                                  140, 40, font, retry_color)
                retry_button.draw("Retry")

                if retry_button.click():
                    retry_color = "light grey"
                    if self.mouse_down:    
                        self.state = 'RUNNING'
                        self.setup_and_reset()
                        player.pos = pygame.Vector2(self.screen.get_width() / 2, self.screen.get_height() / 2)
                        self.mouse_down = False
                else:
                    retry_color = "dark grey"
                        

                change_difficulty_button = Button(self.screen, (self.screen.get_width() / 2, self.screen.get_height() / 2 - 25), 
                                                  140, 40, font, difficulty_color)
                change_difficulty_button.draw("Difficulty")
                if change_difficulty_button.click():
                    difficulty_color = "light grey"
                    if self.mouse_down:
                        self.state = "OPTIONS"
                        self.mouse_down = False
                else:
                    difficulty_color = "dark grey"



        # flip() the display to put your work on screen  
            pygame.display.flip()
            # await asyncio.sleep(0)

        pygame.quit()
game = Game()
game.play()