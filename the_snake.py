"""Файл с реализацией игры Змейка."""
import sys
from random import choice, randint

import pygame as pg


SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

BOARD_BACKGROUND_COLOR = (0, 0, 0)

BORDER_COLOR = (93, 216, 228)

APPLE_COLOR = (255, 0, 0)

SNAKE_COLOR = (0, 255, 0)

DEFAULT_POSITION = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

SPEED = 20

screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

pg.display.set_caption('Змейка')

clock = pg.time.Clock()


class GameObject:
    """Класс игрового объекта игры Змейка."""

    def __init__(self, position=DEFAULT_POSITION,
                 body_color=BOARD_BACKGROUND_COLOR):
        """Инициализация объекта класса GameObject."""
        self.position = position
        self.body_color = body_color

    def draw_cell(self, position, body_color=BOARD_BACKGROUND_COLOR,
                  border_color=BORDER_COLOR):
        """Метод отрисовки одного элемента объекта (клетки)."""
        rect = (pg.Rect(position, (GRID_SIZE, GRID_SIZE)))
        pg.draw.rect(screen, body_color, rect)
        pg.draw.rect(screen, border_color, rect, 1)

    def draw(self):
        """Абстрактный метод draw для отрисовки объектов."""
        raise NotImplementedError(f'В классе'
                                  f'{self.__class__.__name__}'
                                  f'метод не переопределен!')


class Snake(GameObject):
    """Класс объекта Змейка, дочерний от GameObject."""

    def __init__(self):
        """Инициализация объекта Змейка."""
        super().__init__(body_color=SNAKE_COLOR)
        self.reset()

    def update_direction(self):
        """Изменение направления змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Метод, описывающий движение змейки по полю."""
        self.snake_head = self.get_head_position()
        self.head_x, self.head_y = self.snake_head
        if self.next_direction:
            self.x, self.y = self.next_direction
        elif self.next_direction is None:
            self.x, self.y = self.direction
        self.new_direction = (((self.head_x + self.x * GRID_SIZE)
                               % SCREEN_WIDTH),
                              ((self.head_y + self.y * GRID_SIZE)
                               % SCREEN_HEIGHT))
        self.positions.insert(0, self.new_direction)
        self.last = (None if len(self.positions) < self.lenght
                     else self.positions.pop())

    def draw(self):
        """Метод, отрисовывающий змейку на игровом поле."""
        self.draw_cell(self.get_head_position(), SNAKE_COLOR, BORDER_COLOR)

        if self.last:
            self.draw_cell(self.last, border_color=BOARD_BACKGROUND_COLOR)

    def get_head_position(self):
        """Метод, возвращающий координаты головы змейки."""
        return self.positions[0]

    def reset(self):
        """Метод, сбрасывающий змейку в начальное состояние."""
        self.positions = [self.position]
        self.last = None
        self.lenght = 1
        self.direction = RIGHT
        self.next_direction = None


class Apple(GameObject):
    """Класс, описывающий отъект Яблоко, дочерний от GameObject."""

    def __init__(self, position=DEFAULT_POSITION, body_color=None):
        """Инициализация объекта Яблоко."""
        super().__init__(body_color=APPLE_COLOR)
        self.randomize_position(position)

    def randomize_position(self, position=DEFAULT_POSITION):
        """Метод, определяющий позицию яблока."""
        # self.position = (
        #     (randint(0, GRID_WIDTH) * GRID_SIZE) % SCREEN_WIDTH,
        #     (randint(0, GRID_HEIGHT) * GRID_SIZE) % SCREEN_HEIGHT)
        # if isinstance(position, list):
        #     position = [DEFAULT_POSITION]
        # while self.position in position:
        self.position = (
            (randint(0, GRID_WIDTH) * GRID_SIZE) % SCREEN_WIDTH,
            (randint(0, GRID_HEIGHT) * GRID_SIZE) % SCREEN_HEIGHT)

    def draw(self):
        """Метод отрисовки яблока."""
        self.draw_cell(self.position, APPLE_COLOR)


def handle_keys(game_object):
    """Функция обработки действий пользователя."""
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit(0)
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pg.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pg.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pg.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT
            elif event.key == pg.K_ESCAPE:
                sys.exit('Нажата клавиша ESC, произведен выход.')


def main():
    """Логика игры."""
    pg.init()
    apple = Apple()
    snake = Snake()

    while True:

        apple.draw()
        snake.draw()
        handle_keys(snake)
        snake.update_direction()
        snake.move()

        if apple.position == snake.get_head_position():
            apple.randomize_position()
            snake.lenght += 1

        snake_head = snake.get_head_position()
        if snake_head in snake.positions[2:]:
            screen.fill(BOARD_BACKGROUND_COLOR)
            snake.reset()

        pg.display.update()
        clock.tick(SPEED)


"""Выполнение main."""
if __name__ == '__main__':
    main()
