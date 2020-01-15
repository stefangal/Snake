import pygame
from pygame.locals import *
from pygame import *
from constants import *
import random

class Snake:

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((W, H))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.x = self.screen.get_rect().x + 390
        self.y = self.screen.get_rect().y + 380
        self.FPS = FPS
        self.speedY = 0
        self.speedX = 30
        self.emptyboard = True
        self.foodX = 0
        self.foodY = 0
        self.hamburger_img = pygame.image.load('img/hamburger.png').convert_alpha()
        self.apple_img = pygame.image.load('img/apple.png').convert_alpha()
        self.grow = False
        self.path = []
        self.counter = 1
        self.killed = False
        self.best = self.get_best_score()
        self.food = self.hamburger_img
        self.foods = []
        self.apple_qty = 0
        self.hamburger_qty = 0

    def get_best_score(self):
        with open('bestscore.db', 'r') as f:
            return f.read()

    def add_food(self):
        if self.emptyboard:
            self.foodX = random.randrange(0, W-30, 30)
            self.foodY = random.randrange(80, H-30, 30)
            self.food = random.choice([self.hamburger_img, self.apple_img])
            self.emptyboard = False
        if self.food == self.hamburger_img:
            self.screen.blit(self.food, (self.foodX+1, self.foodY+4))
        else:
            self.screen.blit(self.food, (self.foodX+1, self.foodY))


    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.speedX = -30
                    self.speedY = 0
                if event.key == pygame.K_RIGHT:
                    self.speedX = 30
                    self.speedY = 0
                if event.key == pygame.K_UP:
                    self.speedY = -30
                    self.speedX = 0
                if event.key == pygame.K_DOWN:
                    self.speedY = 30
                    self.speedX = 0
                if event.key == pygame.K_KP_PLUS:
                    self.FPS += 5
                if event.key == pygame.K_KP_MINUS:
                    self.FPS -= 5
        self.x += self.speedX
        self.y += self.speedY

    def board(self):
        for x in range(0,W,30):
            for y in range(80,H,30):
                pygame.draw.rect(self.screen, BLACK, [x,y,30,30], 1)

    def show_header(self):
        countTitleFont = pygame.font.SysFont(None, 32)
        countNrFont = pygame.font.SysFont(None, 64)
        countTitle = countTitleFont.render("Score", True, RED)
        countNr = countNrFont.render(str(self.counter-1), True, RED)
        self.screen.blit(countTitle, (W-100,10))
        self.screen.blit(countNr, (W-100,35))

        bestTitleFont = pygame.font.SysFont(None, 32)
        bestNrFont = pygame.font.SysFont(None, 64)
        bestTitle = bestTitleFont.render("Best score", True, RED)
        bestNr = bestNrFont.render(str(self.best), True, RED)
        self.screen.blit(bestTitle, (20,10))
        self.screen.blit(bestNr, (25,35))

        foodFont = pygame.font.SysFont(None, 22)
        applePoints = foodFont.render("+1   SPEED: Fast", True, GOLD)
        appleQty = foodFont.render(str(self.apple_qty)+"x", True, GOLD)
        hamburgerQty = foodFont.render(str(self.hamburger_qty)+"x", True, GOLD)
        hamburgerPoints = foodFont.render("+3   SPEED: Normal", True, GOLD)
        self.screen.blit(hamburgerQty, (255, 15))
        self.screen.blit(appleQty, (255, 49))
        self.screen.blit(self.hamburger_img, (290, 10))
        self.screen.blit(self.apple_img, (290, 39))
        self.screen.blit(hamburgerPoints, (327,15))
        self.screen.blit(applePoints, (327,49))

    def snake(self):
        body = []
        if self.grow:
            if self.foods[-1] == self.hamburger_img:
                self.hamburger_qty += 1
                self.counter += 3
                self.FPS = 10
            elif self.foods[-1] == self.apple_img:
                self.apple_qty += 1
                self.counter += 1
                self.FPS = 15

            if int(self.best) < self.counter:
                self.best = self.counter-1
                with open('bestscore.db', 'w') as f:
                    f.write(str(self.best))

            self.grow = False
        self.path.append((self.x, self.y))
        body = self.path[-self.grow+1:][-self.counter:]
        if body:
            for x, y in body:
                self.snake_body = pygame.draw.rect(self.screen, STEELBLUE, [x+2, y+2, 26, 26], 0)

        if body.count((self.x, self.y)) > 1:
            self.killed = True

        pygame.draw.rect(self.screen, GOLD, [self.x+2, self.y+2, 26, 26], 0)
        pygame.draw.rect(self.screen, BLACK, [self.x+5, self.y+5, 5, 5], 0)
        pygame.draw.rect(self.screen, BLACK, [self.x+20, self.y+5, 5, 5], 0)

        if self.killed:
            for _ in range(5):
                pygame.draw.rect(self.screen, YELLOW, [0, 0, W, 80], 0)
                self.show_header()
                pygame.time.delay(300)
                pygame.display.flip()
                pygame.draw.rect(self.screen, BLACK, [0, 0, W, 80], 0)
                self.show_header()
                pygame.time.delay(300)
                pygame.display.flip()

    def set_limits(self):
        if self.y > H-30: self.y = 80
        elif self.y < 80: self.y = H-30
        if self.x < 0: self.x = W-30
        elif self.x > W-30: self.x = 0

    def collision(self):
        self.food_rect = pygame.Rect([self.foodX, self.foodY,30,30])
        self.head_rect = pygame.Rect(self.x, self.y, 30, 30)
        #to finish collision
        if self.food_rect.colliderect(self.head_rect):
            self.emptyboard = True
            self.grow = True
            self.foods.append(self.food)

    def play_again(self):
        yFont = pygame.font.SysFont(None, 32)
        goFont =pygame.font.SysFont(None, 96)
        y_again = yFont.render('Press "Y" for play again', True, GOLD)
        go = goFont.render("GAME OVER", True, GOLD)
        self.screen.blit(go, (W/2-190,290))
        self.screen.blit(y_again, (W/2-100, 360))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_y:
                    self.killed = False
                    snake = Snake()
                    snake.run()

    def game_loop(self):
        self.clock.tick(self.FPS)
        self.screen.fill(DARKSLATEGRAY)
        self.board()
        self.show_header()
        self.events()
        self.set_limits()
        self.add_food()
        self.snake()
        self.collision()
        pygame.display.flip()

    def run(self):
        play = True
        while not self.killed and play:
            self.game_loop()
            while self.killed:
                self.play_again()
                pygame.display.flip()
        pygame.quit()

if __name__ == "__main__":
    snake = Snake()
    snake.run()