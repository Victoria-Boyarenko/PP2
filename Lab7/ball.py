import pygame
import sys

pygame.init()

WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Moving Ball")

WHITE = (255, 255, 255)
RED = (255, 0, 0)

ball_radius = 25
ball_x = WIDTH // 2
ball_y = HEIGHT // 2
ball_speed = 20

clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        ball_x -= ball_speed
    if keys[pygame.K_RIGHT]:
        ball_x += ball_speed
    if keys[pygame.K_UP]:
        ball_y -= ball_speed
    if keys[pygame.K_DOWN]:
        ball_y += ball_speed

     
    if ball_x - ball_radius < 0:
        ball_x = ball_radius
    if ball_x + ball_radius > WIDTH:
        ball_x = WIDTH - ball_radius
    if ball_y - ball_radius < 0:
        ball_y = ball_radius
    if ball_y + ball_radius > HEIGHT:
        ball_y = HEIGHT - ball_radius

   
    screen.fill(WHITE)
    pygame.draw.circle(screen, RED, (ball_x, ball_y), ball_radius)

    pygame.display.flip()
    clock.tick(60)
