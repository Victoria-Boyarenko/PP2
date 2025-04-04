import pygame, sys
from pygame.locals import *
import random, time

# Инициализация Pygame
pygame.init()

# Загрузка и воспроизведение фоновой музыки
pygame.mixer.music.load("background.wav")
pygame.mixer.music.play(-1)

# Настройка FPS
FPS = 60
FramePerSec = pygame.time.Clock()

# Цвета
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Глобальные переменные
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
SPEED = 5  # Начальная скорость врага
SCORE = 0
COINS_COLLECTED = 0
COIN_SCORE = 0   
N = 5  # Кол-во монет, после которого враг ускоряется

# Шрифты
font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
game_over = font.render("Game Over", True, BLACK)

# Фон
background = pygame.image.load("AnimatedStreet.png")

# Окно
DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Racer")
pygame.display.set_icon(pygame.image.load("iconrace.png"))

# Класс врага
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Enemy.png")
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

    def move(self):
        global SCORE
        self.rect.move_ip(0, SPEED)
        if self.rect.top > SCREEN_HEIGHT:
            SCORE += 1
            self.rect.top = 0
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

# Класс игрока
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("Player.png")
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)

    def move(self):
        pressed_keys = pygame.key.get_pressed()
        if self.rect.left > 0 and pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
        if self.rect.right < SCREEN_WIDTH and pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)

# Класс монеты с весом
class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.value = random.choice([1, 3, 5])  # Случайный вес монеты
        self.set_image_by_value()   
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

    def set_image_by_value(self):
        if self.value == 1:
            img = pygame.image.load("Coin1.png")
        elif self.value == 3:
            img = pygame.image.load("Coin2.png")
        else:
            img = pygame.image.load("Coin3.png")
        self.image = pygame.transform.scale(img, (30, 30))

    def move(self):
        self.rect.move_ip(0, SPEED)
        if self.rect.top > SCREEN_HEIGHT:
            self.respawn()

    def respawn(self):
        self.value = random.choice([1, 3, 5])
        self.set_image_by_value()
        self.rect.top = 0
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

# Объекты
P1 = Player()
E1 = Enemy()
C1 = Coin()

# Группы спрайтов
enemies = pygame.sprite.Group()
enemies.add(E1)

coins = pygame.sprite.Group()
coins.add(C1)

all_sprites = pygame.sprite.Group()
all_sprites.add(P1, E1, C1)

# Игровой цикл
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    # Отрисовка фона
    DISPLAYSURF.blit(background, (0, 0))

    # Отображение счёта и монет
    score_text = font_small.render(f"Score: {SCORE}", True, BLACK)
    coin_text = font_small.render(f"Coins: {COINS_COLLECTED} (Points: {COIN_SCORE})", True, BLACK)
    DISPLAYSURF.blit(score_text, (10, 10))
    DISPLAYSURF.blit(coin_text, (10, 30))

    # Обновление и отрисовка спрайтов
    for entity in all_sprites:
        entity.move()
        DISPLAYSURF.blit(entity.image, entity.rect)

    # Проверка столкновения с врагом
    if pygame.sprite.spritecollideany(P1, enemies):
        pygame.mixer.Sound('crash.wav').play()
        time.sleep(1)
        DISPLAYSURF.fill(RED)
        DISPLAYSURF.blit(game_over, (30, 250))
        pygame.display.update()
        time.sleep(2)
        pygame.quit()
        sys.exit()

    # Проверка столкновения с монетой
    if pygame.sprite.spritecollideany(P1, coins):
        COINS_COLLECTED += 1
        COIN_SCORE += C1.value
        C1.respawn()

        # Ускоряем врага каждые N монет
        if COINS_COLLECTED % N == 0:
            SPEED += 1

    pygame.display.update()
    FramePerSec.tick(FPS)
