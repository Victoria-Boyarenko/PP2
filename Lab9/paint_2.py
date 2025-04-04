import pygame

def main():
    pygame.init()
    screen = pygame.display.set_mode((1000, 600))
    clock = pygame.time.Clock()

    # Основные переменные
    radius = 5
    color = (0, 0, 255)
    mode = 'freehand'  
    drawing = False
    start_pos = None
    last_pos = None

    font = pygame.font.SysFont(None, 24)
    pygame.display.set_caption("Paint")
    pygame.display.set_icon(pygame.image.load("iconpaint.png"))

    screen.fill((0, 0, 0))   
    
    while True:
        pressed = pygame.key.get_pressed()
        alt_held = pressed[pygame.K_LALT] or pressed[pygame.K_RALT]
        ctrl_held = pressed[pygame.K_LCTRL] or pressed[pygame.K_RCTRL]

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

            # Клавиш
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or (event.key == pygame.K_w and ctrl_held) or (event.key == pygame.K_F4 and alt_held):
                    return

                # Цвета
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

                # Режимы рисования
                elif event.key == pygame.K_f:
                    mode = 'freehand'
                elif event.key == pygame.K_t:
                    mode = 'rect'
                elif event.key == pygame.K_c:
                    mode = 'circle'
                elif event.key == pygame.K_e:
                    mode = 'eraser'
                elif event.key == pygame.K_s:
                    mode = 'square'
                elif event.key == pygame.K_h:
                    mode = 'rhombus'
                elif event.key == pygame.K_y:
                    mode = 'right_triangle'
                elif event.key == pygame.K_q:
                    mode = 'eq_triangle'

            elif event.type == pygame.MOUSEBUTTONDOWN:
                drawing = True
                start_pos = event.pos
                last_pos = event.pos

            elif event.type == pygame.MOUSEBUTTONUP:
                end_pos = event.pos
                drawing = False
                x1, y1 = start_pos
                x2, y2 = end_pos

                # Прямоугольник
                if mode == 'rect':
                    rect = pygame.Rect(start_pos, (x2 - x1, y2 - y1))
                    pygame.draw.rect(screen, color, rect, width=2)

                # Круг
                elif mode == 'circle':
                    radius = int(((x2 - x1)**2 + (y2 - y1)**2)**0.5)
                    pygame.draw.circle(screen, color, start_pos, radius, width=2)

                # Квадрат
                elif mode == 'square':
                    side = min(abs(x2 - x1), abs(y2 - y1))
                    pygame.draw.rect(screen, color, (x1, y1, side, side), width=2)

                # Равносторонний треугольник
                elif mode == 'eq_triangle':
                    height = (3 ** 0.5) / 2 * abs(x2 - x1)
                    pygame.draw.polygon(screen, color, [
                        (x1, y1),
                        (x2, y1),
                        ((x1 + x2) / 2, y1 - height)
                    ], width=2)

                # Прямоугольный треугольник
                elif mode == 'right_triangle':
                    pygame.draw.polygon(screen, color, [
                        (x1, y1),
                        (x2, y1),
                        (x1, y2)
                    ], width=2)

                # Ромб
                elif mode == 'rhombus':
                    center_x = (x1 + x2) / 2
                    center_y = (y1 + y2) / 2
                    dx = abs(x2 - x1) / 2
                    dy = abs(y2 - y1) / 2
                    pygame.draw.polygon(screen, color, [
                        (center_x, y1),  # top
                        (x2, center_y),  # right
                        (center_x, y2),  # bottom
                        (x1, center_y)   # left
                    ], width=2)

            # Свободное рисование или ластик
            elif event.type == pygame.MOUSEMOTION and drawing:
                if mode in ['freehand', 'eraser']:
                    end_pos = event.pos
                    draw_color = (0, 0, 0) if mode == 'eraser' else color
                    pygame.draw.line(screen, draw_color, last_pos, end_pos, radius)
                    last_pos = end_pos

        # Правая панель
        pygame.draw.rect(screen, (30, 30, 30), (800, 0, 200, 600))
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
        draw_text(screen, font, "S - Квадрат", 820, 305)
        draw_text(screen, font, "Y - Прям. треуг.", 820, 330)
        draw_text(screen, font, "Q - Равн. треуг.", 820, 355)
        draw_text(screen, font, "H - Ромб", 820, 380)

        draw_text(screen, font, "Esc - Выход", 810, 420)

        draw_text(screen, font, f"Текущий режим: {mode}", 810, 460)
        draw_text(screen, font, f"Цвет: {color}", 810, 485)

        pygame.display.flip()
        clock.tick(60)

# Вывод текста
def draw_text(surface, font, text, x, y, color=(255, 255, 255)):
    text_surface = font.render(text, True, color)
    surface.blit(text_surface, (x, y))

main()
