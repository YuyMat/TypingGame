import json
import pygame
import random
from tkinter import font


class TypingGame(object):
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.width = 900
        self.height = 675
        self.title = "Typing Game"
        self.background_color = (220, 220, 220)
        self.screen_mode = "menu"
        self.rect_dict = {}
        self.difficulty = None
        self.words_json = {
            "easy" : "/Users/yuya/Desktop/MyWork/TypingGame/words/easy_words.json",
            "normal" : "/Users/yuya/Desktop/MyWork/TypingGame/words/normal_words.json",
            "hard" : "/Users/yuya/Desktop/MyWork/TypingGame/words/hard_words.json"
            }
        self.words_dict = None
        _ = [x for x in range(97, 123)]
        alphabet_list = [chr(i) for i in range(ord('a'), ord('z') + 1)]
        self.keyboard_dict = {n: alphabet for n, alphabet in zip(_, alphabet_list)}
        self.typing_sound = pygame.mixer.Sound("/Users/yuya/Desktop/MyWork/TypingGame/sounds/タイピング-メカニカル単2.mp3")
        self.correct_sound = pygame.mixer.Sound("/Users/yuya/Desktop/MyWork/TypingGame/sounds/決定音.mp3")

    def make_screen(self):
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(self.title)

    def init_screen(self):
        self.screen.fill(self.background_color)

    def menu_button(self, mode, rect_x, rect_y, mode_x, mode_y, width, height, color):
        font = pygame.font.SysFont(None, 30, italic=True)
        display_mode = font.render(mode, True, "white")
        rect = pygame.Rect(rect_x, rect_y, width, height)
        self.rect_dict[mode] = rect

        pygame.draw.rect(self.screen, color, rect)
        self.screen.blit(display_mode, (mode_x, mode_y))

    def menu_screen(self):
        font = pygame.font.SysFont(None, 80)

        title = font.render("Typing Game by PyGame!", True, "black")
        image = pygame.image.load("/Users/yuya/Desktop/MyWork/TypingGame/keyboard.png")
        image = pygame.transform.scale(image, (500, 300))
        
        self.menu_button("easy", 700, 400, 725, 410, 100, 40, (59, 175, 117))
        self.menu_button("normal", 700, 450, 713, 460, 100, 40, (0, 106, 182))
        self.menu_button("hard", 700, 500, 725, 510, 100, 40, (215, 29, 59))
        self.screen.blit(title, (20, 50))
        self.screen.blit(image, (40, 300))
        pygame.display.update()
    
    def json_to_dict(self):
        json_path = self.words_json[self.difficulty]
        with open(json_path, "r") as f:
            self.words_dict = json.load(f)

    def play_screen(self):
        self.init_screen()
        if self.i == 0:
            # decide typing word    
            self.word, self.romaji = random.choice(list(self.words_dict.items()))
            
        # settings
        word_font = pygame.font.SysFont("ヒラキノ角コシックw7", 80)
        romaji_font = pygame.font.SysFont(None, 40)
        
        word = word_font.render(self.word, True, "black")
        romaji = romaji_font.render(self.romaji, True, "black")
        word_width_mid = (self.width/2) - (word.get_width()/2)
        romaji_width_mid = (self.width/2) - (romaji.get_width()/2)

        # display
        self.screen.blit(word, (word_width_mid, 50))
        self.screen.blit(romaji, (romaji_width_mid, 150))
        pygame.display.update()

    def progress_bar(self, word):
        progress = (len(self.letter) / len(word)) * self.width
        rect = pygame.Rect(0, 210, progress, 10)

        pygame.draw.rect(self.screen, (255, 0, 0), rect)

    def game_run(self, event):
        font = pygame.font.SysFont(None, 80)
        romaji = self.romaji.replace(" ", "")
        # right typing
        if self.keyboard_dict[event] == romaji[self.i]:
            
            # make sound
            self.typing_sound.play()
            
            self.letter += romaji[self.i]
            
            # display typed letter
            letter = font.render(self.letter, True, "black")
            self.i += 1
            self.play_screen()
            self.screen.blit(letter, ((self.width/2) - (letter.get_width()/2), 400))
            self.progress_bar(romaji)
            pygame.display.update()

            # when complited
            if self.letter == romaji:
                self.correct_sound.set_volume(0.2)
                self.correct_sound.play()
                self.i = 0
                self.letter = ""
                self.play_screen()

    def result_screen(self):
        pass
    
    def display_screen(self):
        if self.screen_mode == "menu":
            self.menu_screen()
        if self.screen_mode == "play":
            self.play_screen()
        if self.screen_mode == "result":
            self.result_screen()

    def run(self):
        self.i = 0
        self.letter = ""
        self.make_screen()
        self.init_screen()
        self.menu_screen()
        running = True
        while running:
            for event in pygame.event.get():
                # exit
                if event.type == pygame.QUIT:
                    running = False
                
                # click
                elif event.type == pygame.MOUSEBUTTONDOWN and self.screen_mode == "menu":
                    if self.rect_dict["easy"].collidepoint(event.pos):
                        self.difficulty = "easy"
                        self.json_to_dict()
                        self.screen_mode = "play"
                    elif self.rect_dict["normal"].collidepoint(event.pos):
                        self.difficulty = "normal"
                        self.json_to_dict()
                        self.screen_mode = "play"
                    elif self.rect_dict["hard"].collidepoint(event.pos):
                        self.difficulty = "hard"
                        self.json_to_dict()
                        self.screen_mode = "play"
                    
                    self.display_screen()
                
                # push keyboard
                elif event.type == pygame.KEYDOWN:
                    # run game
                    if event.key > 96 and event.key < 123 and self.screen_mode == "play":
                        self.game_run(event.key)
                    # esc to finish the game
                    elif event.key == 27:
                        running = False

typing_game = TypingGame()
typing_game.run()