import random
import pygame
import sys


# Инициализация Pygame
pygame.init()

# Константы
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Направления движения
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Настройка экрана
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Змейка")
clock = pygame.time.Clock()


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
        super().__init__(body_color=(255, 0, 0))
        self.randomize_position()
    
    def randomize_position(self):
        """Устанавливает случайное положение яблока на игровом поле."""
        x = random.randint(0, GRID_WIDTH - 1) * GRID_SIZE
        y = random.randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        self.position = (x, y)
    
    def draw(self, surface):
        """
        Отрисовывает яблоко на игровой поверхности.
        
        Args:
            surface: Поверхность для отрисовки
        """
        rect = pygame.Rect(self.position[0], self.position[1], 
                          GRID_SIZE, GRID_SIZE)
        pygame.draw.rect(surface, self.body_color, rect)


class Snake(GameObject):
    """Класс для представления змейки."""
    
    def __init__(self):
        """Инициализирует змейку в начальном состоянии."""
        super().__init__(body_color=(0, 255, 0))
        self.length = 1
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction = RIGHT
        self.next_direction = None
    
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
        for position in self.positions:
            rect = pygame.Rect(position[0], position[1], 
                              GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(surface, self.body_color, rect)
    
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


def handle_keys(snake):
    """
    Обрабатывает нажатия клавиш для изменения направления змейки.
    
    Args:
        snake (Snake): Объект змейки
    """
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


def main():
    """Основная функция игры."""
    snake = Snake()
    apple = Apple()
    
    # Убедимся, что яблоко не появляется на змейке
    while apple.position in snake.positions:
        apple.randomize_position()
    
    while True:
        # Обработка событий
        handle_keys(snake)
        
        # Обновление направления движения
        snake.update_direction()
        
        # Движение змейки
        if not snake.move():
            snake.reset()
            apple.randomize_position()
            # Убедимся, что яблоко не появляется на змейке после сброса
            while apple.position in snake.positions:
                apple.randomize_position()
            continue
        
        # Проверка съедания яблока
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position()
            # Убедимся, что яблоко не появляется на змейке
            while apple.position in snake.positions:
                apple.randomize_position()
        
        # Отрисовка
        screen.fill(BOARD_BACKGROUND_COLOR)
        snake.draw(screen)
        apple.draw(screen)
        
        # Обновление экрана
        pygame.display.update()
        clock.tick(20)


if __name__ == "__main__":
    main()