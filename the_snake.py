"""Файл с реализацией игры Змейка"""

from random import choice, randint
import pygame

# Инициализация PyGame:
pygame.init()

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()
# Тут опишите все классы игры.


class GameObject():  # класс, описывающий игровые объекты
    """Класс игрового объекта"""
    position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)  # централизуется позиция
    body_color = (0, 0, 0)  # дефолтный цвет

    def __init__(self, x_coord, y_coord):  # инициализация объекта
        self.x_coord = x_coord
        self.y_coord = y_coord

    def draw(self):  # метод отрисовки объекта, пустой
        pass


class Snake(GameObject):  # класс, описывающий объект Змейка
    """Класс змейки"""
    lenght = 1
    positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]  # список позиций змейки
    last = positions[:-1]
    direction = RIGHT
    next_direction = None

    def __init__(self, x_coord, y_coord):
        super().__init__(x_coord, y_coord)
        self.body_color = SNAKE_COLOR

    def update_direction(self):  # изменение направления
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):  # обновляет позицию змейки
        self.head = self.get_head_position()
        self.x, self.y = self.direction
        # получаем координату головы
        self.new_direction = ((self.head[0] + self.x), (self.head[1] + self.y))
        self.positions.insert(-1, self.new_direction)
        
        

    def draw(self):  # отрисовка головы змейки
        for position in self.positions[:-1]:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

    # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def get_head_position(self):  # возвращает голову, первый элемент
        return self.positions[0]

    def reset(self):  # сброс змейки в начальное состояние
        self.positions = Snake.positions
        return self.positions


class Apple(GameObject):  # класс, описывающий обхъект Яблоко
    """Класс яблока"""
    
    def __init__(self, x_coord, y_coord):
        super().__init__(x_coord, y_coord)
        self.body_color = APPLE_COLOR

    def randomize_position():  # рандомит координаты и выдает их кортежем
        x_coord = randint(0, GRID_WIDTH) * GRID_SIZE
        y_coord = randint(0, GRID_HEIGHT) * GRID_SIZE
        return (x_coord, y_coord)
    
    position = randomize_position()

    def draw(self):  # отрисовка яблока
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


def handle_keys(game_object):  # Функция обработки действий пользователя
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Логика игры"""
    # Тут нужно создать экземпляры классов.
    running = True
    apple = Apple(1, 1)
    snake = Snake(1, 1)

    while running:
        apple.draw()
        snake.draw()
        while handle_keys(snake):
            snake.update_direction()
            snake.move()
        pygame.display.update()
        clock.tick(SPEED)
        # Тут опишите основную логику игры.
        # ...

"""Выполнение main"""
if __name__ == '__main__':
    main()


# Метод draw класса Apple
# def draw(self):
#     rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
#     pygame.draw.rect(screen, self.body_color, rect)
#     pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

# # Метод draw класса Snake
# def draw(self):
#     for position in self.positions[:-1]:
#         rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
#         pygame.draw.rect(screen, self.body_color, rect)
#         pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

#     # Отрисовка головы змейки
#     head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
#     pygame.draw.rect(screen, self.body_color, head_rect)
#     pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

#     # Затирание последнего сегмента
#     if self.last:
#         last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
#         pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

# Функция обработки действий пользователя
# def handle_keys(game_object):
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             pygame.quit()
#             raise SystemExit
#         elif event.type == pygame.KEYDOWN:
#             if event.key == pygame.K_UP and game_object.direction != DOWN:
#                 game_object.next_direction = UP
#             elif event.key == pygame.K_DOWN and game_object.direction != UP:
#                 game_object.next_direction = DOWN
#             elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
#                 game_object.next_direction = LEFT
#             elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
#                 game_object.next_direction = RIGHT

# Метод обновления направления после нажатия на кнопку
# def update_direction(self):
#     if self.next_direction:
#         self.direction = self.next_direction
#         self.next_direction = None
