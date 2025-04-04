import pygame

def main():
    pygame.init()
    screen = pygame.display.set_mode((1000, 600))   
    clock = pygame.time.Clock()

    radius = 5
    color = (0, 0, 255)
    mode = 'freehand'   
    drawing = False
    start_pos = None
    last_pos = None

    # Шрифт для вывода текста
    font = pygame.font.SysFont(None, 24)
    pygame.display.set_caption("Paint")
    pygame.display.set_icon(pygame.image.load("iconpaint.png"))

    # Начальный черный фон
    screen.fill((0, 0, 0))

    while True:
        pressed = pygame.key.get_pressed()
        alt_held = pressed[pygame.K_LALT] or pressed[pygame.K_RALT]
        ctrl_held = pressed[pygame.K_LCTRL] or pressed[pygame.K_RCTRL]

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN:
                # Выход по ESC, Ctrl+W или Alt+F4
                if event.key == pygame.K_ESCAPE or (event.key == pygame.K_w and ctrl_held) or (event.key == pygame.K_F4 and alt_held):
                    return
                # Выбор цвета
                if event.key == pygame.K_r:
                    color = (255, 0, 0)
                elif event.key == pygame.K_g:
                    color = (0, 255, 0)
                elif event.key == pygame.K_b:
                    color = (0, 0, 255)
                elif event.key == pygame.K_k:
                    color = (0, 0, 0)
                elif event.key == pygame.K_w:
                    color = (255, 255, 255)
                # Выбор режима рисования
                elif event.key == pygame.K_f:
                    mode = 'freehand'
                elif event.key == pygame.K_t:
                    mode = 'rect'
                elif event.key == pygame.K_c:
                    mode = 'circle'
                elif event.key == pygame.K_e:
                    mode = 'eraser'

            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Запоминаем начальную точку при нажатии мыши
                drawing = True
                start_pos = event.pos
                last_pos = event.pos

            elif event.type == pygame.MOUSEBUTTONUP:
                # При отпускании мыши рисуем прямоугольник или круг
                end_pos = event.pos
                drawing = False
                if mode == 'rect':
                    rect = pygame.Rect(start_pos, (end_pos[0] - start_pos[0], end_pos[1] - start_pos[1]))
                    pygame.draw.rect(screen, color, rect, width=2)
                elif mode == 'circle':
                    center = start_pos
                    radius = int(((end_pos[0] - start_pos[0]) ** 2 + (end_pos[1] - start_pos[1]) ** 2) ** 0.5)
                    pygame.draw.circle(screen, color, center, radius, width=2)

            elif event.type == pygame.MOUSEMOTION and drawing:
                # Свободное рисование или ластик
                if mode == 'freehand' or mode == 'eraser':
                    end_pos = event.pos
                    draw_color = (0, 0, 0) if mode == 'eraser' else color
                    pygame.draw.line(screen, draw_color, last_pos, end_pos, radius)
                    last_pos = end_pos

        # Область справа для меню
        pygame.draw.rect(screen, (30, 30, 30), (800, 0, 200, 600))

        # Подсказки
        draw_text(screen, font, "Цвета:", 810, 20)
        draw_text(screen, font, "R - Красный", 820, 45)
        draw_text(screen, font, "G - Зелёный", 820, 70)
        draw_text(screen, font, "B - Синий", 820, 95)
        draw_text(screen, font, "K - Чёрный", 820, 120)
        draw_text(screen, font, "W - Белый", 820, 145)

        draw_text(screen, font, "Режимы:", 810, 180)
        draw_text(screen, font, "F - Кисть", 820, 205)
        draw_text(screen, font, "E - Ластик", 820, 230)
        draw_text(screen, font, "T - Прямоуг.", 820, 255)
        draw_text(screen, font, "C - Круг", 820, 280)

        draw_text(screen, font, "Esc - Выход", 810, 330)

        # Показ текущего режима и цвета
        draw_text(screen, font, f"Текущий режим: {mode}", 810, 380)
        draw_text(screen, font, f"Цвет: {color}", 810, 405)

        pygame.display.flip()
        clock.tick(60)

# Функция для вывода текста на экран
def draw_text(surface, font, text, x, y, color=(255, 255, 255)):
    text_surface = font.render(text, True, color)
    surface.blit(text_surface, (x, y))

main()
