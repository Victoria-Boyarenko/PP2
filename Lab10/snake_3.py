import pygame
import random
import time
import psycopg2
from datetime import datetime

# Параметры подключения к базе данных PostgreSQL
DB_PARAMS = {
    "database": "PP2",
    "user": "postgres",
    "password": "V12$34i67#89v",
    "host": "localhost",
    "port": "5432"
}

# Получение данных пользователя по имени
def get_user_data(username):
    conn = psycopg2.connect(**DB_PARAMS)
    cur = conn.cursor()
    cur.execute("SELECT id FROM users WHERE username = %s", (username,))
    user = cur.fetchone()
    if user:
        # Если пользователь найден, получаем его последний результат
        user_id = user[0]
        cur.execute("""
            SELECT score, level FROM user_score
            WHERE user_id = %s ORDER BY saved_at DESC LIMIT 1
        """, (user_id,))
        last_game = cur.fetchone()
        conn.close()
        if last_game:
            print(f"Welcome back, {username}! Last Level: {last_game[1]}, Last Score: {last_game[0]}")
        else:
            print(f"Welcome back, {username}! Starting fresh.")
        return user_id, (0, 0)
    else:
        # Если пользователь новый, создаём его
        cur.execute("INSERT INTO users (username) VALUES (%s) RETURNING id", (username,))
        user_id = cur.fetchone()[0]
        conn.commit()
        conn.close()
        print(f"New player created: {username}. Starting at Level 0.")
        return user_id, (0, 0)

# Сохраняем результат игры пользователя
def save_game(user_id, score, level):
    conn = psycopg2.connect(**DB_PARAMS)
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO user_score (user_id, score, level, saved_at)
        VALUES (%s, %s, %s, %s)
    """, (user_id, score, level, datetime.now()))
    conn.commit()
    conn.close()

# Получение топ-N результатов игроков
def get_top_scores(limit=5):
    conn = psycopg2.connect(**DB_PARAMS)
    cur = conn.cursor()
    cur.execute("""
        SELECT u.username, MAX(s.score) as max_score
        FROM users u JOIN user_score s ON u.id = s.user_id
        GROUP BY u.username ORDER BY max_score DESC LIMIT %s
    """, (limit,))
    result = cur.fetchall()
    conn.close()
    return result

# Ввод имени игрока
username = input("Enter your username: ")
user_id, (score, level) = get_user_data(username)
death_reason = ""

# Цвета
colorWHITE = (255, 255, 255)
colorGRAY = (200, 200, 200)
colorBLACK = (0, 0, 0)
colorRED = (255, 0, 0)
colorGREEN = (0, 255, 0)
colorBLUE = (0, 0, 255)
colorYELLOW = (255, 255, 0)
colorPURPLE = (160, 32, 240)

# Инициализация Pygame и установка размеров экрана
pygame.init()
GRID_WIDTH = 20
CELL = 30
WIDTH = GRID_WIDTH * CELL + 200
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")
font = pygame.font.SysFont("Arial", 24)

# Класс точки на игровом поле
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

# Класс змейки
class Snake:
    def __init__(self):
        self.body = [Point(10, 11), Point(10, 12), Point(10, 13)]
        self.dx = 1
        self.dy = 0

    # Движение змейки
    def move(self):
        for i in range(len(self.body) - 1, 0, -1):
            self.body[i].x = self.body[i - 1].x
            self.body[i].y = self.body[i - 1].y
        self.body[0].x += self.dx
        self.body[0].y += self.dy

    # Отрисовка змейки
    def draw(self):
        pygame.draw.rect(screen, colorRED, (self.body[0].x * CELL, self.body[0].y * CELL, CELL, CELL))
        for segment in self.body[1:]:
            pygame.draw.rect(screen, colorYELLOW, (segment.x * CELL, segment.y * CELL, CELL, CELL))

    # Проверка столкновения с едой
    def check_collision(self, food):
        head = self.body[0]
        if head.x == food.pos.x and head.y == food.pos.y:
            for _ in range(food.weight):
                self.body.append(Point(head.x, head.y))
            return True
        return False

    # Проверка выхода за границы поля
    def check_wall_collision(self):
        head = self.body[0]
        return head.x < 0 or head.x >= GRID_WIDTH or head.y < 0 or head.y >= HEIGHT // CELL

# Класс еды
class Food:
    def __init__(self, snake):
        self.pos = self.generate_random_position(snake)
        self.weight = random.choice([1, 2, 3])
        self.spawn_time = time.time()
        self.color = {1: colorGREEN, 2: colorBLUE, 3: colorPURPLE}[self.weight]

    # Генерация позиции еды
    def generate_random_position(self, snake):
        while True:
            x = random.randint(0, GRID_WIDTH - 1)
            y = random.randint(0, HEIGHT // CELL - 1)
            if all(segment.x != x or segment.y != y for segment in snake.body):
                return Point(x, y)

    # Отрисовка еды
    def draw(self):
        pygame.draw.rect(screen, self.color, (self.pos.x * CELL, self.pos.y * CELL, CELL, CELL))

    # Исчезновение еды
    def is_expired(self, timeout=7):
        return time.time() - self.spawn_time > timeout

# Отрисовка шахматной сетки
def draw_grid():
    colors = [colorWHITE, colorGRAY]
    for i in range(GRID_WIDTH):
        for j in range(HEIGHT // CELL):
            pygame.draw.rect(screen, colors[(i + j) % 2], (i * CELL, j * CELL, CELL, CELL))

# Панель управления (пауза)
def draw_controls_panel():
    pygame.draw.rect(screen, (220, 220, 220), (WIDTH - 160, 20, 130, 50))
    pygame.draw.rect(screen, colorBLACK, (WIDTH - 160, 20, 130, 50), 2)
    text = font.render("Pause (P)", True, colorBLACK)
    screen.blit(text, (WIDTH - 145, 35))

# Отрисовка стен-барьеров
def draw_walls(walls):
    for wall in walls:
        pygame.draw.rect(screen, colorBLACK, (wall[0] * CELL, wall[1] * CELL, CELL, CELL))

# Отрисовка текущего счёта, уровня и скорости + ТОП игроков

def draw_score_and_level(score, level):
    text1 = font.render(f"Score: {score}", True, colorBLACK)
    text2 = font.render(f"Level: {level}", True, colorBLACK)
    speed = levels_data.get(level, levels_data[0])["speed"]
    text3 = font.render(f"Speed: {speed}", True, colorBLACK)
    screen.blit(text1, (WIDTH - 145, 90))
    screen.blit(text2, (WIDTH - 145, 120))
    screen.blit(text3, (WIDTH - 145, 150))

    # ТОП игроков
    top_scores = get_top_scores()
    header = font.render("Top Players:", True, colorBLACK)
    screen.blit(header, (WIDTH - 145, 190))
    for i, (name, top_score) in enumerate(top_scores):
        entry = font.render(f"{i+1}. {name[:6]}: {top_score}", True, colorBLACK)
        screen.blit(entry, (WIDTH - 145, 220 + i * 25))


# Настройки уровней: скорость и препятствия
levels_data = {
    0: {"speed": 3, "walls": []},
    1: {"speed": 4, "walls": [(10, 5)]},
    2: {"speed": 4, "walls": [(5, 8), (15, 12)]},
    3: {"speed": 5, "walls": [(3, 5), (6, 8), (14, 10)]},
    4: {"speed": 6, "walls": [(3, 9), (16, 10)]},
    5: {"speed": 7, "walls": [(5, y) for y in range(5, 15)]},
    6: {"speed": 8, "walls": [(10, y) for y in range(0, 10)] + [(15, y) for y in range(10, 20)]},
    7: {"speed": 9, "walls": [(x, 10) for x in range(5, 20)]}
}

# Установка скорости и инициализация игры
FPS = levels_data.get(level, levels_data[0])["speed"]
clock = pygame.time.Clock()
snake = Snake()
food = Food(snake)

# Ожидание нажатия ENTER для старта
waiting_to_start = True
while waiting_to_start:
    screen.fill(colorWHITE)
    title = font.render("Press ENTER to start the game", True, colorBLACK)
    screen.blit(title, (WIDTH // 2 - 180, HEIGHT // 2))
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            waiting_to_start = False

# Основной игровой цикл
running = True
while running:
    screen.fill(colorWHITE)
    draw_grid()
    draw_controls_panel()
    draw_score_and_level(score, level)

    # Обработка нажатий клавиш
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT and snake.dx != -1:
                snake.dx = 1; snake.dy = 0
            elif event.key == pygame.K_LEFT and snake.dx != 1:
                snake.dx = -1; snake.dy = 0
            elif event.key == pygame.K_DOWN and snake.dy != -1:
                snake.dx = 0; snake.dy = 1
            elif event.key == pygame.K_UP and snake.dy != 1:
                snake.dx = 0; snake.dy = -1
            elif event.key == pygame.K_p:
                # Пауза и сохранение игры
                save_game(user_id, score, level)
                paused = True
                pause_text = font.render("Game Paused. Press P to continue.", True, colorBLACK)
                screen.blit(pause_text, (WIDTH // 2 - 180, HEIGHT // 2))
                pygame.display.flip()
                while paused:
                    for pause_event in pygame.event.get():
                        if pause_event.type == pygame.QUIT:
                            paused = False
                            running = False
                        elif pause_event.type == pygame.KEYDOWN and pause_event.key == pygame.K_p:
                            paused = False
            elif event.key == pygame.K_ESCAPE:
                running = False

    snake.move()
    walls = levels_data.get(level, {}).get("walls", [])
    draw_walls(walls)
    food.draw()
    snake.draw()

    # Проверка на проигрыш
    head = snake.body[0]
    if snake.check_wall_collision():
        death_reason = "You hit the wall."
        running = False
    elif (head.x, head.y) in walls:
        death_reason = "You hit an obstacle."
        running = False
    elif head.x >= GRID_WIDTH:
        death_reason = "You hit the side panel."
        running = False

    # Проверка съедена ли еда
    if snake.check_collision(food):
        score += food.weight
        food = Food(snake)

    # Проверка исчезла ли еда
    if food.is_expired():
        food = Food(snake)

    # Переход на следующий уровень
    if score // 5 > level and level + 1 in levels_data:
        level += 1
        FPS = levels_data[level]["speed"]

    pygame.display.flip()
    clock.tick(FPS)

# Отображение экрана окончания игры
screen.fill(colorWHITE)
text1 = font.render("GAME OVER", True, colorRED)
text2 = font.render(death_reason, True, colorBLACK)
text3 = font.render(f"Your score: {score}  Level: {level}", True, colorBLACK)
text4 = font.render("Press ESC to exit", True, colorBLACK)

screen.blit(text1, (WIDTH // 2 - 100, HEIGHT // 2 - 60))
screen.blit(text2, (WIDTH // 2 - 140, HEIGHT // 2 - 20))
screen.blit(text3, (WIDTH // 2 - 140, HEIGHT // 2 + 20))
screen.blit(text4, (WIDTH // 2 - 140, HEIGHT // 2 + 60))
pygame.display.flip()

# Ожидание закрытия игры
waiting = True
while waiting:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            waiting = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            waiting = False

pygame.quit()

