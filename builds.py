import pygame
import random

# Настройки
WIDTH, HEIGHT = 600, 900
BLOCK_SIZE = 30
COLUMNS = WIDTH // BLOCK_SIZE
ROWS = HEIGHT // BLOCK_SIZE

# Цвета
colors = [
    (0, 0, 0),       # пусто
    (255, 0, 0),     # красный
    (0, 255, 0),     # зелёный
    (0, 0, 255),     # синий
    (255, 255, 0),   # жёлтый
    (255, 165, 0),   # оранжевый
    (128, 0, 128),   # фиолетовый
    (0, 255, 255)    # голубой
]

# Фигуры
figures = [
    [[1, 1, 1, 1]],  # I
    [[1, 1], [1, 1]],  # O
    [[0, 1, 0], [1, 1, 1]],  # T
    [[1, 0, 0], [1, 1, 1]],  # J
    [[0, 0, 1], [1, 1, 1]],  # L
    [[1, 1, 0], [0, 1, 1]],  # S
    [[0, 1, 1], [1, 1, 0]]   # Z
]

# Класс фигуры
class Tetromino:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.shape = random.choice(figures)
        self.color = random.randint(1, len(colors) - 1)

    def rotate(self):
        self.shape = [list(row) for row in zip(*self.shape[::-1])]

# Проверка столкновений
def check_collision(board, shape, offset):
    off_x, off_y = offset
    for y, row in enumerate(shape):
        for x, cell in enumerate(row):
            if cell:
                if x + off_x < 0 or x + off_x >= COLUMNS or y + off_y >= ROWS:
                    return True
                if board[y + off_y][x + off_x]:
                    return True
    return False

# Добавление фигуры на поле
def merge(board, shape, offset, color):
    off_x, off_y = offset
    for y, row in enumerate(shape):
        for x, cell in enumerate(row):
            if cell:
                board[y + off_y][x + off_x] = color

# Удаление заполненных линий
def clear_lines(board):
    new_board = [row for row in board if any(cell == 0 for cell in row)]
    lines_cleared = ROWS - len(new_board)
    for _ in range(lines_cleared):
        new_board.insert(0, [0] * COLUMNS)
    return new_board, lines_cleared

# Класс уровней
class LevelManager:
    def __init__(self):
        self.levels = {
            i: {
                "speed": max(120, 500 - i * 20),
                "lines": i * 10,
                "score": i * 1000,
                "difficulty": ["Easy", "Normal", "Hard", "Very Hard", "Insane", "Extreme", "Impossible"][min(i // 3, 6)]
            } for i in range(1, 21)
        }
        self.current_level = 1
        self.total_lines = 0
        self.total_score = 0

    def update(self, lines_cleared, score_gained):
        self.total_lines += lines_cleared
        self.total_score += score_gained
        for level in range(1, 21):
            if (self.total_lines >= self.levels[level]["lines"] and
                self.total_score >= self.levels[level]["score"]):
                self.current_level = level

    def get_speed(self):
        return self.levels[self.current_level]["speed"]

    def get_level(self):
        return self.current_level

    def get_difficulty(self):
        return self.levels[self.current_level]["difficulty"]

# Основной цикл
def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("BlockDrop")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 24)

    board = [[0] * COLUMNS for _ in range(ROWS)]
    current = Tetromino(COLUMNS // 2 - 2, 0)
    fall_time = 0
    score = 0
    level_manager = LevelManager()
    speed = level_manager.get_speed()

    running = True
    while running:
        screen.fill((0, 0, 0))
        fall_time += clock.get_rawtime()
        clock.tick()

        # Падение фигуры
        if fall_time > speed:
            fall_time = 0
            if not check_collision(board, current.shape, (current.x, current.y + 1)):
                current.y += 1
            else:
                merge(board, current.shape, (current.x, current.y), current.color)
                board, lines_cleared = clear_lines(board)
                score_gained = lines_cleared * 100
                score += score_gained
                level_manager.update(lines_cleared, score_gained)
                speed = level_manager.get_speed()
                current = Tetromino(COLUMNS // 2 - 2, 0)
                if check_collision(board, current.shape, (current.x, current.y)):
                    running = False  # Game Over

        # События
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if not check_collision(board, current.shape, (current.x - 1, current.y)):
                        current.x -= 1
                elif event.key == pygame.K_RIGHT:
                    if not check_collision(board, current.shape, (current.x + 1, current.y)):
                        current.x += 1
                elif event.key == pygame.K_DOWN:
                    if not check_collision(board, current.shape, (current.x, current.y + 1)):
                        current.y += 1
                elif event.key == pygame.K_UP:
                    rotated = [list(row) for row in zip(*current.shape[::-1])]
                    if not check_collision(board, rotated, (current.x, current.y)):
                        current.shape = rotated

        # Отрисовка поля
        for y in range(ROWS):
            for x in range(COLUMNS):
                color = colors[board[y][x]]
                pygame.draw.rect(screen, color, (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)

        # Отрисовка текущей фигуры
        for y, row in enumerate(current.shape):
            for x, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(screen, colors[current.color],
                                     ((current.x + x) * BLOCK_SIZE, (current.y + y) * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)

        # Отображение текста
        level_text = font.render(f"Level: {level_manager.get_level()}", True, (255, 255, 255))
        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        difficulty_text = font.render(f"Difficulty: {level_manager.get_difficulty()}", True, (255, 100, 100))

        screen.blit(level_text, (10, 10))
        screen.blit(score_text, (10, 40))
        screen.blit(difficulty_text, (10, 70))

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
