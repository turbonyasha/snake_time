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

    def __init__(self, position, body_color):  # инициализация объекта
        self.position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.body_color = (0, 0, 0)

    def draw(self):  # метод отрисовки объекта, пустой
        pass


class Snake(GameObject):  # класс, описывающий объект Змейка
    """Класс змейки"""
    lenght = 1
    positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]  # список позиций змейки
    direction = RIGHT
    next_direction = None

    def __init__(self):
        self.position = self.get_head_position()
        self.body_color = SNAKE_COLOR
        self.last = self.get_last_position()

    def update_direction(self):  # изменение направления
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):  # обновляет позицию змейки
        self.last = self.get_last_position()
        self.snake_head = self.get_head_position()  # голова
        self.head_x, self.head_y = self.snake_head
        if self.next_direction:
            self.x, self.y = self.next_direction  # направление
        elif self.next_direction is None:
            self.x, self.y = self.direction
        self.new_direction = (((self.head_x + self.x * GRID_SIZE) % SCREEN_WIDTH),
                              ((self.head_y + self.y * GRID_SIZE) % SCREEN_HEIGHT))
        # добавляем новую координату в список позиций
        self.positions.insert(0, self.new_direction)
        # удаляем последнюю координату из списка
        self.positions.pop()


    def collapse_check(self):  # проверяем на столкновение
        snake_head = self.get_head_position()
        if snake_head in self.positions[1:]:
            return True
        else:
            return False
        
    def add_next_snake_piece(self):  # добавляем квардат в змейку
        self.lenght += 1
        self.positions.append(self.positions[-1])


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

    def get_last_position(self):  # возвращаем последний кусок змеи
        return self.positions[-1]

    def reset(self):  # сброс змейки в начальное состояние
        self.positions = Snake.positions
        return self.positions


class Apple(GameObject):  # класс, описывающий объект Яблоко
    """Класс яблока"""
    
    def __init__(self):
        self.body_color = APPLE_COLOR
        self.position = self.randomize_position()
        

    def randomize_position(self):  # рандомит координаты и выдает их кортежем
        return (
            (randint(0, GRID_WIDTH) * GRID_SIZE) % SCREEN_WIDTH,
            (randint(0, GRID_HEIGHT) * GRID_SIZE) % SCREEN_HEIGHT
        )


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
    apple = Apple()
    snake = Snake()

    while running:

        # проверяем генерацию яблока на змейке
        if apple.position in snake.positions:
            apple.position = apple.randomize_position()
            apple.draw()
        else:
            apple.draw()
        snake.draw()
        handle_keys(snake)
        snake.update_direction()
        snake.move()
        
        # проверяем на съедение
        if apple.position == snake.get_head_position():
            apple.position = apple.randomize_position()
            snake.add_next_snake_piece()


        # проверяем на врезание
        if snake.collapse_check():
            snake.positions = snake.reset()

        pygame.display.update()
        clock.tick(5)
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
