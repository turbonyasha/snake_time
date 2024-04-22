"""Файл с реализацией игры Змейка"""

from random import randint
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
    """Класс игрового объекта игры Змейка"""

    def __init__(self, position, body_color):  # инициализация объекта
        """Инициализация объекта класса GameObject"""
        self.position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.body_color = BOARD_BACKGROUND_COLOR

    def draw_cell(self, position):
        """Метод отрисовки одного элемента объекта (клетки)"""
        rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

    def draw(self):  # метод отрисовки объекта, пустой
        """Абстрактный метод draw для отрисовки объектов"""
        pass


class Snake(GameObject):
    """Класс объекта Змейка, дочерний от GameObject"""

    # длина змейки
    lenght = 1
    # список списков позиций змейки
    positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
    # дефолтное направление движения
    direction = RIGHT
    # задаваемое направление движения
    next_direction = None

    def __init__(self):
        """Инициализация объекта Змейка"""
        self.position = self.get_head_position()
        self.body_color = SNAKE_COLOR
        self.last = self.get_last_position()

    def update_direction(self):
        """Изменение направления змейки"""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Метод, описывающий движение змейки по полю"""
        # опреляем хвост и голову
        self.last = self.get_last_position()
        self.snake_head = self.get_head_position()
        # раскладываем голову на координаты
        self.head_x, self.head_y = self.snake_head
        # проверяем направление движения
        if self.next_direction:
            self.x, self.y = self.next_direction
        elif self.next_direction is None:
            self.x, self.y = self.direction
        # вычисляем новую координату движения головы змейки
        self.new_direction = (((self.head_x + self.x * GRID_SIZE)
                               % SCREEN_WIDTH),
                              ((self.head_y + self.y * GRID_SIZE)
                               % SCREEN_HEIGHT))
        # добавляем новую координату в список позиций
        self.positions.insert(0, self.new_direction)
        # удаляем последнюю координату из списка позиций
        self.positions.pop()

    def collapse_check(self):
        """Метод, проверяющий столкновение змеи и самой собой"""
        snake_head = self.get_head_position()
        if snake_head in self.positions[2:]:
            self.reset()

    def add_next_snake_piece(self):
        """Метод, добавляющий в змейку новый элемент"""
        self.lenght += 1
        self.positions.append(self.positions[-1])

    def draw(self):
        """Метод, отрисовывающий змейку на игровом поле"""
        for position in self.positions:
            self.draw_cell(position)

    # затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def get_head_position(self):
        """Метод, возвращающий координаты головы змейки"""
        return self.positions[0]

    def get_last_position(self):
        """Метод, возвращающий координаты хвоста змейки"""
        return self.positions[-1]

    def reset(self):
        """Метод, сбрасывающий змейку в начальное состояние"""
        # обновляем поле
        screen.fill(BOARD_BACKGROUND_COLOR)
        # обновляем нулевую позицию согласно тз
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        # обновляем длину змеи
        self.lenght = Snake.lenght
        # обновляем направление змеи на стандартное
        self.direction = Snake.direction
        self.new_direction = Snake.next_direction


class Apple(GameObject):
    """Класс, описывающий отъект Яблоко, дочерний от GameObject"""

    def __init__(self):
        """Инициализация объекта Яблоко"""
        self.body_color = APPLE_COLOR
        self.position = self.randomize_position()

    def randomize_position(self):
        """Метод, определяющий позицию яблока"""
        return (
            (randint(0, GRID_WIDTH) * GRID_SIZE) % SCREEN_WIDTH,
            (randint(0, GRID_HEIGHT) * GRID_SIZE) % SCREEN_HEIGHT
        )

    def draw(self):
        """Метод отрисовки яблока"""
        self.draw_cell(self.position)


def handle_keys(game_object):
    """Функция обработки действий пользователя"""
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
    # переменная для продолжения игры
    running = True
    # создаем объекты обоих классов
    apple = Apple()
    snake = Snake()

    while running:

        # проверяем генерацию яблока на змейке и рисуем его
        if apple.position in snake.positions:
            apple.position = apple.randomize_position()
            apple.draw()
        else:
            apple.draw()
        # рисуем змейку
        snake.draw()
        # проверяем полученное новое направление
        handle_keys(snake)
        # меняем направление змейки
        snake.update_direction()
        # двигаем змейку в новом направлении
        snake.move()

        # проверяем на съедение змейкой яблока
        if apple.position == snake.get_head_position():
            apple.position = apple.randomize_position()
            snake.add_next_snake_piece()

        # проверяем на врезание змейки в себя
        if snake.collapse_check():
            snake.reset()

        pygame.display.update()
        clock.tick(SPEED)


"""Выполнение main"""
if __name__ == '__main__':
    main()
