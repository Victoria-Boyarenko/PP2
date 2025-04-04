import pygame
import random

# Цвета
colorWHITE = (255, 255, 255)
colorGRAY = (200, 200, 200)
colorBLACK = (0, 0, 0)
colorRED = (255, 0, 0)
colorGREEN = (0, 255, 0)
colorBLUE = (0, 0, 255)
colorYELLOW = (255, 255, 0)

# Инициализация Pygame
pygame.init()

# Размеры окна
WIDTH = 600
HEIGHT = 600
CELL = 30

# Создание окна
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")
pygame.display.set_icon(pygame.image.load("iconsnake.png"))


# Отрисовка клетчатого поля
def draw_grid_chess():
    colors = [colorWHITE, colorGRAY]
    for i in range(WIDTH // CELL):
        for j in range(HEIGHT // CELL):
            pygame.draw.rect(screen, colors[(i + j) % 2], (i * CELL, j * CELL, CELL, CELL))

# Класс точки (координаты)
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

# Класс змейки
class Snake:
    def __init__(self):
        self.body = [Point(10, 11), Point(10, 12), Point(10, 13)]
        self.dx = 1  # движение по x
        self.dy = 0  # движение по y

    def move(self):
        # Движение тела змейки
        for i in range(len(self.body) - 1, 0, -1):
            self.body[i].x = self.body[i - 1].x
            self.body[i].y = self.body[i - 1].y
        # Движение головы
        self.body[0].x += self.dx
        self.body[0].y += self.dy

    def draw(self):
        head = self.body[0]
        pygame.draw.rect(screen, colorRED, (head.x * CELL, head.y * CELL, CELL, CELL))
        for segment in self.body[1:]:
            pygame.draw.rect(screen, colorYELLOW, (segment.x * CELL, segment.y * CELL, CELL, CELL))

    def check_collision(self, food):
        head = self.body[0]
        if head.x == food.pos.x and head.y == food.pos.y:
            self.body.append(Point(head.x, head.y))
            return True
        return False

    def check_wall_collision(self):
        head = self.body[0]
        if head.x < 0 or head.x >= WIDTH // CELL or head.y < 0 or head.y >= HEIGHT // CELL:
            return True
        return False

# Класс еды
class Food:
    def __init__(self, snake):
        self.pos = self.generate_random_position(snake)

    def generate_random_position(self, snake):
        while True:
            x = random.randint(0, WIDTH // CELL - 1)
            y = random.randint(0, HEIGHT // CELL - 1)
            if all(segment.x != x or segment.y != y for segment in snake.body):
                return Point(x, y)

    def draw(self):
        pygame.draw.rect(screen, colorGREEN, (self.pos.x * CELL, self.pos.y * CELL, CELL, CELL))

# Отображение очков и уровня
font = pygame.font.SysFont("Arial", 24)
def draw_score_and_level(score, level):
    text = font.render(f"Score: {score}  Level: {level}", True, colorBLACK)
    screen.blit(text, (10, 10))

# Инициализация
clock = pygame.time.Clock()
score = 0
level = 1
FPS = 5

snake = Snake()
food = Food(snake)

# Обновление уровня
def update_level(score):
    return 1 + score // 4

# Игровой цикл
running = True
while running:
    screen.fill(colorWHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Управление змейкой
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT and snake.dx != -1:
                snake.dx = 1
                snake.dy = 0
            elif event.key == pygame.K_LEFT and snake.dx != 1:
                snake.dx = -1
                snake.dy = 0
            elif event.key == pygame.K_DOWN and snake.dy != -1:
                snake.dx = 0
                snake.dy = 1
            elif event.key == pygame.K_UP and snake.dy != 1:
                snake.dx = 0
                snake.dy = -1

    draw_grid_chess()

    # Движение и проверка
    snake.move()

    if snake.check_wall_collision():
        print("Game Over! You hit the wall.")
        running = False

    if snake.check_collision(food):
        score += 1
        food = Food(snake)

    # Проверка и обновление уровня
    new_level = update_level(score)
    if new_level > level:
        level = new_level
        FPS += 2
        print(f"Level up! Now level {level}")

    # Отрисовка объектов
    snake.draw()
    food.draw()
    draw_score_and_level(score, level)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
