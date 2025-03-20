import pygame
import sys
import math
from datetime import datetime


pygame.init()

WIDTH, HEIGHT = 800, 600
CENTER = (WIDTH // 2, HEIGHT // 2)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mickey Clock")

background = pygame.image.load("clock.png").convert_alpha()
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

minute_hand = pygame.image.load("min_hand.png").convert_alpha()
minute_hand = pygame.transform.scale(minute_hand, (800, 600))

second_hand = pygame.image.load("sec_hand.png").convert_alpha()
second_hand = pygame.transform.scale(second_hand, (800, 600))

clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    now = datetime.now()
    minute = now.minute
    second = now.second

    minute_angle = -(minute / 60) * 360
    second_angle = -(second / 60) * 360

    rotated_minute = pygame.transform.rotate(minute_hand, minute_angle)
    rotated_second = pygame.transform.rotate(second_hand, second_angle)

    minute_rect = rotated_minute.get_rect(center=CENTER)
    second_rect = rotated_second.get_rect(center=CENTER)

    screen.blit(background, (0, 0))
    screen.blit(rotated_minute, minute_rect.topleft)
    screen.blit(rotated_second, second_rect.topleft)

    pygame.display.flip()
    clock.tick(60)   