import pygame
import random
import sys

# === Настройки ===
WIDTH, HEIGHT = 300, 600
BLOCK_SIZE = 30
COLUMNS = WIDTH // BLOCK_SIZE
ROWS = HEIGHT // BLOCK_SIZE

# === Цвета ===
colors = [
    (0, 0, 0), (255, 0, 0), (0, 255, 0),
    (0, 0, 255), (255, 255, 0), (255, 165, 0),
    (128, 0, 128), (0, 255, 255)
]

# === Фигуры ===
figures = [
    [[1, 1, 1, 1]],  # I
    [[1, 1], [1, 1]], # O
    [[0, 1, 0], [1, 1, 1]], # T
    [[1, 0, 0], [1, 1, 1]], # L
    [[0, 0, 1], [1, 1, 1]], # J
    [[1, 1, 0], [0, 1, 1]], # S
    [[0, 1, 1], [1, 1, 0]]  # Z
]

# --- Классы и функции игры (без изменений) ---

class Tetromino:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.shape = random.choice(figures)
        self.color = random.randint(1, len(colors) - 1)

class LevelManager:
    def __init__(self):
        self.current_level = 1
        self.lines_to_next_level = 10
        self.total_lines_cleared = 0
        self.speed = 500

    def update(self, lines_cleared):
        self.total_lines_cleared += lines_cleared
        if self.total_lines_cleared >= self.lines_to_next_level:
            self.current_level += 1
            self.lines_to_next_level += 10
            self.speed = max(100, self.speed - 25)
            return True
        return False

    def get_speed(self):
        return self.speed

    def get_level(self):
        return self.current_level

def check_collision(board, shape, offset):
    off_x, off_y = offset
    for y, row in enumerate(shape):
        for x, cell in enumerate(row):
            if cell:
                if not (0 <= x + off_x < COLUMNS and 0 <= y + off_y < ROWS):
                    return True
                if y + off_y < ROWS and board[y + off_y][x + off_x]:
                    return True
    return False

def merge(board, shape, offset, color):
    off_x, off_y = offset
    for y, row in enumerate(shape):
        for x, cell in enumerate(row):
            if cell:
                board[y + off_y][x + off_x] = color

def clear_lines(board):
    new_board = [row for row in board if any(cell == 0 for cell in row)]
    lines_cleared = ROWS - len(new_board)
    for _ in range(lines_cleared):
        new_board.insert(0, [0] * COLUMNS)
    return new_board, lines_cleared

def flash_level_up(screen):
    flash = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    flash.fill((255, 255, 255, 100))
    screen.blit(flash, (0, 0))
    pygame.display.flip()
    pygame.time.delay(150)

# --- НОВАЯ ФУНКЦИЯ ЭКРАНА УРОВНЕЙ ---
def levels_screen():
    screen = pygame.display.get_surface() # Используем уже созданный экран
    clock = pygame.time.Clock()
    
    title_font = pygame.font.SysFont("Arial", 40, bold=True)
    info_font = pygame.font.SysFont("Arial", 24)
    button_font = pygame.font.SysFont("Arial", 30)

    white = (255, 255, 255)
    yellow = (255, 255, 0)
    
    while True:
        screen.fill((10, 10, 20))

        title_text = title_font.render("Уровни", True, yellow)
        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 50))
        
        # Отображение информации о прогрессии уровней
        for i in range(1, 11): # Покажем первые 10 уровней
            lines_needed = (i - 1) * 10
            info_text_content = f"Уровень {i}: {lines_needed} линий"
            info_text = info_font.render(info_text_content, True, white)
            screen.blit(info_text, (WIDTH // 2 - info_text.get_width() // 2, 120 + i * 30))

        # Кнопка "Назад"
        back_text = button_font.render("Назад", True, white)
        back_button = back_text.get_rect(center=(WIDTH // 2, HEIGHT - 50))
        
        mouse_pos = pygame.mouse.get_pos()
        if back_button.collidepoint(mouse_pos):
            back_text = button_font.render("Назад", True, yellow)
        
        screen.blit(back_text, back_button)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.collidepoint(mouse_pos):
                    return # Возвращаемся в главное меню

        pygame.display.flip()
        clock.tick(30)

# --- ОБНОВЛЕННАЯ ФУНКЦИЯ МЕНЮ ---
def main_menu():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("BlockDrop | Меню")
    clock = pygame.time.Clock()

    title_font = pygame.font.SysFont("Arial", 50, bold=True)
    button_font = pygame.font.SysFont("Arial", 30)

    white = (255, 255, 255)
    yellow = (255, 255, 0)
    
    while True:
        screen.fill((10, 10, 20))

        title_text = title_font.render("BlockDrop", True, yellow)
        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 150))

        # --- Кнопки ---
        start_text = button_font.render("Начать игру", True, white)
        levels_text = button_font.render("Уровни", True, white) # Новая кнопка
        quit_text = button_font.render("Выход", True, white)
        
        start_button = start_text.get_rect(center=(WIDTH // 2, 300))
        levels_button = levels_text.get_rect(center=(WIDTH // 2, 350)) # Новая кнопка
        quit_button = quit_text.get_rect(center=(WIDTH // 2, 400)) # Сдвинули кнопку выхода

        mouse_pos = pygame.mouse.get_pos()
        if start_button.collidepoint(mouse_pos):
            start_text = button_font.render("Начать игру", True, yellow)
        if levels_button.collidepoint(mouse_pos):
            levels_text = button_font.render("Уровни", True, yellow)
        if quit_button.collidepoint(mouse_pos):
            quit_text = button_font.render("Выход", True, yellow)

        screen.blit(start_text, start_button)
        screen.blit(levels_text, levels_button) # Новая кнопка
        screen.blit(quit_text, quit_button)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button.collidepoint(mouse_pos):
                    main_game()
                if levels_button.collidepoint(mouse_pos):
                    levels_screen() # Вызываем новый экран
                if quit_button.collidepoint(mouse_pos):
                    pygame.quit()
                    sys.exit()

        pygame.display.flip()
        clock.tick(30)

def main_game():
    screen = pygame.display.get_surface()
    pygame.display.set_caption("BlockDrop")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 24)

    board = [[0] * COLUMNS for _ in range(ROWS)]
    current = Tetromino(COLUMNS // 2 - 1, 0)
    fall_time = 0
    score = 0
    level_manager = LevelManager()

    running = True
    while running:
        screen.fill((10, 10, 20))
        speed = level_manager.get_speed()
        fall_time += clock.get_rawtime()
        clock.tick(60) # Увеличим FPS для более плавной игры

        if fall_time > speed:
            fall_time = 0
            if not check_collision(board, current.shape, (current.x, current.y + 1)):
                current.y += 1
            else:
                merge(board, current.shape, (current.x, current.y), current.color)
                board, lines_cleared = clear_lines(board)
                score_gained = [0, 100, 300, 700, 1500][lines_cleared]
                score += score_gained
                if lines_cleared > 0:
                    if level_manager.update(lines_cleared):
                        flash_level_up(screen)
                current = Tetromino(COLUMNS // 2 - 1, 0)
                if check_collision(board, current.shape, (current.x, current.y)):
                    running = False 
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
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
                    rotated_shape = [list(row) for row in zip(*current.shape[::-1])]
                    if not check_collision(board, rotated_shape, (current.x, current.y)):
                        current.shape = rotated_shape
                        
        # Отрисовка
        for y in range(ROWS):
            for x in range(COLUMNS):
                if board[y][x] != 0:
                    color = colors[board[y][x]]
                    pygame.draw.rect(screen, color, (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)
                pygame.draw.rect(screen, (50, 50, 50), (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 1)

        for y, row in enumerate(current.shape):
            for x, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(screen, colors[current.color],
                                     ((current.x + x) * BLOCK_SIZE, (current.y + y) * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)

        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        level_text = font.render(f"Level: {level_manager.get_level()}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))
        screen.blit(level_text, (10, 40))

        pygame.display.flip()

# === ТОЧКА ВХОДА В ИГРУ ===
if __name__ == "__main__":
    main_menu()