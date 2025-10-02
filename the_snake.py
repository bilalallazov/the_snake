import random
import pygame
import sys
import time

# Инициализация Pygame
pygame.init()

# Константы
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
BOARD_BACKGROUND_COLOR = (0, 0, 0)
SNAKE_COLOR = (0, 255, 0)
APPLE_COLOR = (255, 0, 0)
TEXT_COLOR = (255, 255, 255)

# Направления движения
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Настройка экрана
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Змейка")
clock = pygame.time.Clock()

# Шрифты
font = pygame.font.Font(None, 36)
large_font = pygame.font.Font(None, 72)


class GameObject:
    """Базовый класс для игровых объектов."""
    
    def __init__(self, position=None, body_color=None):
        """
        Инициализирует базовые атрибуты объекта.
        
        Args:
            position (tuple): Позиция объекта на игровом поле
            body_color (tuple): Цвет объекта в формате RGB
        """
        self.position = position or (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.body_color = body_color
    
    def draw(self, surface):
        """
        Абстрактный метод для отрисовки объекта.
        
        Args:
            surface: Поверхность для отрисовки
        """
        pass


class Apple(GameObject):
    """Класс для представления яблока."""
    
    def __init__(self):
        """Инициализирует яблоко с красным цветом и случайной позицией."""
        super().__init__(body_color=APPLE_COLOR)
        self.randomize_position()
    
    def randomize_position(self, snake_positions=None):
        """Устанавливает случайное положение яблока на игровом поле."""
        if snake_positions is None:
            snake_positions = []
        
        while True:
            x = random.randint(0, GRID_WIDTH - 1) * GRID_SIZE
            y = random.randint(0, GRID_HEIGHT - 1) * GRID_SIZE
            self.position = (x, y)
            
            # Проверяем, что яблоко не появляется на змейке
            if self.position not in snake_positions:
                break
    
    def draw(self, surface):
        """
        Отрисовывает яблоко на игровой поверхности.
        
        Args:
            surface: Поверхность для отрисовки
        """
        rect = pygame.Rect(self.position[0], self.position[1], 
                          GRID_SIZE, GRID_SIZE)
        pygame.draw.rect(surface, self.body_color, rect)
        # Добавляем небольшой круг для эффекта объема
        inner_rect = pygame.Rect(
            self.position[0] + GRID_SIZE // 4,
            self.position[1] + GRID_SIZE // 4,
            GRID_SIZE // 2,
            GRID_SIZE // 2
        )
        pygame.draw.ellipse(surface, (200, 0, 0), inner_rect)


class Snake(GameObject):
    """Класс для представления змейки."""
    
    def __init__(self):
        """Инициализирует змейку в начальном состоянии."""
        super().__init__(body_color=SNAKE_COLOR)
        self.reset()
    
    def update_direction(self):
        """Обновляет направление движения змейки."""
        if self.next_direction is not None:
            # Проверяем, что змейка не может двигаться назад
            if (self.length == 1 or 
                (self.next_direction[0] * -1, self.next_direction[1] * -1) != self.direction):
                self.direction = self.next_direction
            self.next_direction = None
    
    def move(self):
        """
        Обновляет позицию змейки.
        
        Returns:
            bool: True если движение успешно, False если змейка столкнулась с собой
        """
        head_x, head_y = self.positions[0]
        new_head_x = (head_x + self.direction[0] * GRID_SIZE) % SCREEN_WIDTH
        new_head_y = (head_y + self.direction[1] * GRID_SIZE) % SCREEN_HEIGHT
        new_head = (new_head_x, new_head_y)
        
        # Проверяем столкновение с собой
        if new_head in self.positions:
            return False
        
        self.positions.insert(0, new_head)
        
        # Удаляем хвост, если змейка не выросла
        if len(self.positions) > self.length:
            self.positions.pop()
        
        return True
    
    def draw(self, surface):
        """
        Отрисовывает змейку на экране.
        
        Args:
            surface: Поверхность для отрисовки
        """
        for i, position in enumerate(self.positions):
            rect = pygame.Rect(position[0], position[1], GRID_SIZE, GRID_SIZE)
            
            # Голова змейки другого цвета
            if i == 0:
                pygame.draw.rect(surface, (0, 200, 0), rect)  # Более темный зеленый для головы
                # Глаза змейки
                eye_size = GRID_SIZE // 5
                if self.direction == RIGHT:
                    pygame.draw.circle(surface, (0, 0, 0), 
                                      (position[0] + GRID_SIZE - eye_size, position[1] + eye_size*2), 
                                      eye_size)
                    pygame.draw.circle(surface, (0, 0, 0), 
                                      (position[0] + GRID_SIZE - eye_size, position[1] + GRID_SIZE - eye_size*2), 
                                      eye_size)
                elif self.direction == LEFT:
                    pygame.draw.circle(surface, (0, 0, 0), 
                                      (position[0] + eye_size, position[1] + eye_size*2), 
                                      eye_size)
                    pygame.draw.circle(surface, (0, 0, 0), 
                                      (position[0] + eye_size, position[1] + GRID_SIZE - eye_size*2), 
                                      eye_size)
                elif self.direction == UP:
                    pygame.draw.circle(surface, (0, 0, 0), 
                                      (position[0] + eye_size*2, position[1] + eye_size), 
                                      eye_size)
                    pygame.draw.circle(surface, (0, 0, 0), 
                                      (position[0] + GRID_SIZE - eye_size*2, position[1] + eye_size), 
                                      eye_size)
                elif self.direction == DOWN:
                    pygame.draw.circle(surface, (0, 0, 0), 
                                      (position[0] + eye_size*2, position[1] + GRID_SIZE - eye_size), 
                                      eye_size)
                    pygame.draw.circle(surface, (0, 0, 0), 
                                      (position[0] + GRID_SIZE - eye_size*2, position[1] + GRID_SIZE - eye_size), 
                                      eye_size)
            else:
                pygame.draw.rect(surface, self.body_color, rect)
                
                # Добавляем легкий градиент для тела
                inner_rect = pygame.Rect(
                    position[0] + 2,
                    position[1] + 2,
                    GRID_SIZE - 4,
                    GRID_SIZE - 4
                )
                pygame.draw.rect(surface, (0, 230, 0), inner_rect)
    
    def get_head_position(self):
        """
        Возвращает позицию головы змейки.
        
        Returns:
            tuple: Координаты головы змейки
        """
        return self.positions[0]
    
    def reset(self):
        """Сбрасывает змейку в начальное состояние."""
        self.length = 1
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction = RIGHT
        self.next_direction = None
        self.score = 0


def draw_score(surface, score, high_score):
    """Отрисовывает счет на экране."""
    score_text = font.render(f"Счет: {score}", True, TEXT_COLOR)
    high_score_text = font.render(f"Рекорд: {high_score}", True, TEXT_COLOR)
    surface.blit(score_text, (10, 10))
    surface.blit(high_score_text, (SCREEN_WIDTH - high_score_text.get_width() - 10, 10))


def draw_game_over(surface, score):
    """Отрисовывает экран завершения игры."""
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    overlay.set_alpha(180)
    overlay.fill((0, 0, 0))
    surface.blit(overlay, (0, 0))
    
    game_over_text = large_font.render("ИГРА ОКОНЧЕНА", True, (255, 0, 0))
    score_text = font.render(f"Ваш счет: {score}", True, TEXT_COLOR)
    restart_text = font.render("Нажмите R для перезапуска", True, TEXT_COLOR)
    quit_text = font.render("Нажмите Q для выхода", True, TEXT_COLOR)
    
    surface.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 3))
    surface.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, SCREEN_HEIGHT // 2))
    surface.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, SCREEN_HEIGHT // 2 + 50))
    surface.blit(quit_text, (SCREEN_WIDTH // 2 - quit_text.get_width() // 2, SCREEN_HEIGHT // 2 + 100))


def handle_keys(snake, game_paused, game_over):
    """
    Обрабатывает нажатия клавиш для изменения направления змейки и управления игрой.
    
    Returns:
        tuple: (game_paused, should_restart, should_quit)
    """
    should_restart = False
    should_quit = False
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                snake.next_direction = UP
            elif event.key == pygame.K_DOWN:
                snake.next_direction = DOWN
            elif event.key == pygame.K_LEFT:
                snake.next_direction = LEFT
            elif event.key == pygame.K_RIGHT:
                snake.next_direction = RIGHT
            elif event.key == pygame.K_p:
                game_paused = not game_paused
            elif event.key == pygame.K_r and game_over:
                should_restart = True
            elif event.key == pygame.K_q and game_over:
                should_quit = True
    
    return game_paused, should_restart, should_quit


def main():
    """Основная функция игры."""
    snake = Snake()
    apple = Apple()
    game_paused = False
    game_over = False
    high_score = 0
    
    # Убедимся, что яблоко не появляется на змейке
    apple.randomize_position(snake.positions)
    
    while True:
        # Обработка событий
        game_paused, should_restart, should_quit = handle_keys(snake, game_paused, game_over)
        
        if should_quit:
            pygame.quit()
            sys.exit()
        elif should_restart:
            snake.reset()
            apple.randomize_position(snake.positions)
            game_over = False
            continue
        
        if game_over or game_paused:
            # Отрисовка в режиме паузы или завершения игры
            screen.fill(BOARD_BACKGROUND_COLOR)
            snake.draw(screen)
            apple.draw(screen)
            draw_score(screen, snake.score, high_score)
            
            if game_paused:
                pause_text = font.render("ПАУЗА - Нажмите P для продолжения", True, TEXT_COLOR)
                screen.blit(pause_text, (SCREEN_WIDTH // 2 - pause_text.get_width() // 2, SCREEN_HEIGHT // 2))
            
            if game_over:
                draw_game_over(screen, snake.score)
            
            pygame.display.update()
            clock.tick(10)  # Низкий FPS в режиме паузы/завершения
            continue
        
        # Обновление направления движения
        snake.update_direction()
        
        # Движение змейки
        if not snake.move():
            game_over = True
            if snake.score > high_score:
                high_score = snake.score
            continue
        
        # Проверка съедания яблока
        if snake.get_head_position() == apple.position:
            snake.length += 1
            snake.score += 10
            apple.randomize_position(snake.positions)
        
        # Отрисовка
        screen.fill(BOARD_BACKGROUND_COLOR)
        snake.draw(screen)
        apple.draw(screen)
        draw_score(screen, snake.score, high_score)
        
        # Обновление экрана
        pygame.display.update()
        
        # Увеличиваем скорость с ростом счета
        base_speed = 10
        speed_increase = min(snake.score // 50, 10)  # Максимум +10 к скорости
        clock.tick(base_speed + speed_increase)


if __name__ == "__main__":
    main()
