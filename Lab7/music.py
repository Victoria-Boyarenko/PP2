import pygame
import sys

pygame.init()

WIDTH, HEIGHT = 800, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Music Player")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

font = pygame.font.SysFont("Comic Sans MS", 36)

playlist = ["Sans.mp3", "Ruins.mp3", "Memory.mp3"]
current_song = 0

pygame.mixer.music.load(playlist[current_song])
is_playing = False

clock = pygame.time.Clock()

def draw_text(text, y):
    render = font.render(text, True, BLACK)
    rect = render.get_rect(center=(WIDTH // 2, y))
    screen.blit(render, rect)

while True:
    screen.fill(WHITE)

    draw_text(f"Now Playing: {playlist[current_song]}", HEIGHT // 2 - 30)
    draw_text("P: Play/Pause | S: Stop | N: Next | R: Previous", HEIGHT // 2 + 30)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                if not is_playing:
                    pygame.mixer.music.play()
                    is_playing = True
                else:
                    pygame.mixer.music.pause()
                    is_playing = False

            elif event.key == pygame.K_s:
                pygame.mixer.music.stop()
                is_playing = False

            elif event.key == pygame.K_n:
                current_song = (current_song + 1) % len(playlist)
                pygame.mixer.music.load(playlist[current_song])
                pygame.mixer.music.play()
                is_playing = True

            elif event.key == pygame.K_r:
                current_song = (current_song - 1) % len(playlist)
                pygame.mixer.music.load(playlist[current_song])
                pygame.mixer.music.play()
                is_playing = True

    pygame.display.flip()
    clock.tick(30)
