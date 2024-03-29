from random import choice
from typing import Optional
from pygame.color import THECOLORS

import pygame as pg
import sys

pg.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
CENTER = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)
BOARD_BACKGROUND_COLOR = (0, 0, 0)
BORDER_COLOR = (93, 216, 228)
APPLE_BORDER_COLOR = (0, 100, 0)
APPLE_COLOR = (255, 0, 0)
ROTTEN_APPLE_BORDER_COLOR = (139, 69, 19)
ROTTEN_APPLE = (244, 164, 96)
SNAKE_COLOR = (255, 0, 255)
SNAKE_COLORS_POSITIONS = (
    (260, 120),
    (330, 120),
    (400, 120),
)
APPLE_COLORS_POSITIONS = (
    (260, 210),
    (330, 210),
    (400, 210),
)
DIFFICULT_POSITIONS = (
    (260, 280),
    (330, 280),
    (400, 280),
)
STONE_BORDER_COLOR = (220, 220, 220)
STONE_COLOR = (128, 128, 128)
SPEED = 20
DIRECTIONS = {
    (pg.K_UP, LEFT): UP,
    (pg.K_UP, RIGHT): UP,
    (pg.K_DOWN, LEFT): DOWN,
    (pg.K_DOWN, RIGHT): DOWN,
    (pg.K_LEFT, UP): LEFT,
    (pg.K_LEFT, DOWN): LEFT,
    (pg.K_RIGHT, UP): RIGHT,
    (pg.K_RIGHT, DOWN): RIGHT,
}
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
pg.display.set_caption('Змейка')
clock = pg.time.Clock()
font = pg.font.SysFont('couriernew', 30)


class StartMenu:
    def __init__(self) -> None:
        self.start_game = False
        self.start_button_position = ((215, 395), (230, 65))

    def draw(self, surface):
        text_set_color = font.render(
            str('Выберите цвет:'), True, THECOLORS['white'])
        text_set_speed = font.render(
            str('Выберите сложность:'), True, THECOLORS['white']
        )
        text_snake = font.render('Змея:', True, THECOLORS['white'])
        text_apple = font.render('Яблоко:', True, THECOLORS['white'])
        text_start = font.render('Начать игру', True, THECOLORS['white'])
        screen.blit(text_set_color, (190, 50))
        screen.blit(text_set_speed, (160, 270))
        screen.blit(text_snake, (100, 120))
        screen.blit(text_apple, (100, 210))
        screen.blit(text_start, (230, 410))
        rect = pg.Rect((215, 395), (230, 65))
        pg.draw.rect(surface, THECOLORS['gold'], rect, 10)


class MenuObject:
    def __init__(self) -> None:
        self.objects_names: tuple = ()
        self.objects_rectangles: dict = {}
        self.objects_description: dict = {}
        self.current_object = ''

    def draw(self, surface):
        for key in self.objects_names:
            rect = pg.Rect(self.objects_rectangles[key])
            pg.draw.rect(surface, self.objects_description[key], rect)

    def draw_border(self, surface, color=THECOLORS['white'], border=5):
        rect = pg.Rect(
            (self.objects_rectangles[self.current_object][0][0] - border,
             self.objects_rectangles[self.current_object][0][1] - border,
             ),
            (self.objects_rectangles[self.current_object][1][0] + border * 2,
             self.objects_rectangles[self.current_object][1][1] + border * 2
             ),
        )
        pg.draw.rect(surface, color, rect, border)

    def clear_border(self, surface, border=5):
        for rec in self.objects_rectangles:
            if rec != self.current_object:
                rect = pg.Rect(
                    (self.objects_rectangles[rec][0][0] - border,
                     self.objects_rectangles[rec][0][1] - border,
                     ),
                    (self.objects_rectangles[rec][1][0] + border * 2,
                     self.objects_rectangles[rec][1][1] + border * 2,
                     ),
                )
                pg.draw.rect(surface, BOARD_BACKGROUND_COLOR, rect, border)


class MenuSnakeObjects(MenuObject):
    def __init__(self) -> None:
        super().__init__()
        self.objects_names = ('snake_fuchsia', 'snake_aqua', 'snake_blue',)
        self.objects_rectangles = {'snake_fuchsia': ((260, 120), (40, 40)),
                                   'snake_aqua': ((330, 120), (40, 40)),
                                   'snake_blue': ((400, 120), (40, 40))
                                   }
        self.objects_description = {'snake_fuchsia': THECOLORS['fuchsia'],
                                    'snake_aqua': THECOLORS['aqua'],
                                    'snake_blue': THECOLORS['blue'],
                                    }
        self.current_object = 'snake_fuchsia'


class MenuAppleObjects(MenuObject):
    def __init__(self) -> None:
        super().__init__()
        self.objects_names = ('apple_red', 'apple_yellow', 'apple_lime',)
        self.objects_rectangles = {'apple_red': ((260, 210), (40, 40)),
                                   'apple_yellow': ((330, 210), (40, 40)),
                                   'apple_lime': ((400, 210), (40, 40)),
                                   }
        self.objects_description = {'apple_red': THECOLORS['red'],
                                    'apple_yellow': THECOLORS['yellow'],
                                    'apple_lime': THECOLORS['lime'],
                                    }
        self.current_object = 'apple_red'


class MenuDifficultObjects(MenuObject):
    def __init__(self) -> None:
        super().__init__()
        self.objects_names = ('light', 'medium', 'hard',)
        self.objects_rectangles = {'light': ((95, 325), (115, 45)),
                                   'medium': ((255, 325), (135, 45)),
                                   'hard': ((415, 325), (135, 45)),
                                   }
        self.objects_description = {
            'light': font.render('Лёгкая', True, THECOLORS['white']),
            'medium': font.render('Средняя', True, THECOLORS['white']),
            'hard': font.render('Сложная', True, THECOLORS['white']),
        }
        self.difficultes = {
            'light': 10,
            'medium': 20,
            'hard': 30,
        }
        self.current_object = 'medium'

    def draw(self, surface):
        surface.blit(self.objects_description['light'], (100, 330))
        surface.blit(self.objects_description['medium'], (260, 330))
        surface.blit(self.objects_description['hard'], (420, 330))

    def draw_border(self, surface, color=THECOLORS['silver'], border=7):
        return super().draw_border(surface, color, border)

    def clear_border(self, surface, border=7):
        return super().clear_border(surface, border)


class GameObject:
    '''Базовый класс, описывающий игровой объект.'''

    all_positions = set((x * GRID_SIZE, y * GRID_SIZE)
                        for x in range(GRID_WIDTH - 1)
                        for y in range(GRID_HEIGHT - 1))
    taken_positions: set[tuple[int, int]] = set()

    def __init__(
        self, body_color: tuple[int, int, int] = BOARD_BACKGROUND_COLOR
    ) -> None:
        self.position = CENTER
        self.body_color = body_color

    def draw(self, surface: pg.surface.Surface) -> None:
        '''Заготовка метода для отрисовки объекта на игровом поле.'''
        pass


class Apple(GameObject):
    '''Класс, описывающий игровой объект яблоко.'''

    def __init__(self, body_color: tuple[int, int, int] = APPLE_COLOR) -> None:
        super().__init__(body_color)
        self.randomize_position()

    def randomize_position(self) -> None:
        '''Метод, который устанавливает случайное положение яблока
        на игровом поле.
        '''
        GameObject.taken_positions.discard(self.position)
        self.position = choice(list(GameObject.all_positions
                                    - GameObject.taken_positions))
        GameObject.taken_positions.add(self.position)

    def draw(self, surface: pg.surface.Surface) -> None:
        '''Метод для отрисовки яблока на игровом поле.'''
        circle_center = (
            self.position[0] + GRID_SIZE // 2,
            self.position[1] + GRID_SIZE // 2,
        )
        pg.draw.circle(surface, APPLE_BORDER_COLOR,
                       circle_center, GRID_SIZE // 2)
        pg.draw.circle(surface, self.body_color,
                       circle_center, GRID_SIZE // 2 - 1)


class Rotten_apple(GameObject):
    '''Класс, описывающий игровой объект гнилое яблоко.'''

    def __init__(self,
                 body_color: tuple[int, int, int] = ROTTEN_APPLE
                 ) -> None:
        super().__init__(body_color)
        self.randomize_position()

    def randomize_position(self) -> None:
        '''Метод, который устанавливает случайное положение гнилого яблока
        на игровом поле.
        '''
        GameObject.taken_positions.discard(self.position)
        self.position = choice(list(GameObject.all_positions
                                    - GameObject.taken_positions))
        GameObject.taken_positions.add(self.position)

    def draw(self, surface: pg.surface.Surface) -> None:
        '''Метод для отрисовки яблока на игровом поле.'''
        circle_center = (
            self.position[0] + GRID_SIZE // 2,
            self.position[1] + GRID_SIZE // 2,
        )
        pg.draw.circle(
            surface, ROTTEN_APPLE_BORDER_COLOR, circle_center, GRID_SIZE // 2
        )
        pg.draw.circle(surface, self.body_color,
                       circle_center, GRID_SIZE // 2 - 1)


class Snake(GameObject):
    '''Класс, описывающий игровой объект змейку.'''

    def __init__(self, body_color: tuple[int, int, int] = SNAKE_COLOR) -> None:
        super().__init__(body_color)
        self.reset()
        self.last: Optional[tuple] = None

    def reset(self) -> None:
        '''Метод, который сбрасывает змейку
        и игровое поле в начальное состояние.
        '''
        self.length = 1
        self.positions = [CENTER]
        self.direction = RIGHT
        screen.fill(BOARD_BACKGROUND_COLOR)
        GameObject.taken_positions.clear()

    def update_direction(self, direction: Optional[tuple[int, int]]) -> None:
        '''Метод, который обновляет направление движения змейки'''
        if direction:
            self.direction = direction

    def move(self) -> None:
        '''Метод, который перемещает змейку на игровом поле'''
        head = self.get_head_position()
        # Получение новых координат головы змейки после перемещения.
        new_head = (
            (head[0] + self.direction[0] * GRID_SIZE) % SCREEN_WIDTH,
            (head[1] + self.direction[1] * GRID_SIZE) % SCREEN_HEIGHT,
        )
        # Проверка на столкновение змейки с самой собой.
        if new_head in self.positions[2:]:
            self.reset()
        else:
            # Изменение длины змейки для имитации движения по игровому полю.
            self.positions.insert(0, new_head)
            # Проверка на столкновение с яблоком.
            if len(self.positions) > self.length:
                self.last = self.positions.pop(-1)

    def draw(self, surface: pg.surface.Surface) -> None:
        '''Метод для отрисовки змейки на игровом поле.'''
        for position in self.positions[:-1]:
            rect = pg.Rect((position[0], position[1]), (GRID_SIZE, GRID_SIZE))
            pg.draw.rect(surface, self.body_color, rect)
            pg.draw.rect(surface, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки.
        head_rect = pg.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(surface, self.body_color, head_rect)
        pg.draw.rect(surface, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента.
        if self.last:
            last_rect = pg.Rect(
                (self.last[0], self.last[1]), (GRID_SIZE, GRID_SIZE))
            pg.draw.rect(surface, BOARD_BACKGROUND_COLOR, last_rect)

    def get_head_position(self) -> tuple:
        '''Метод, который возвращает позицию головы змейки.'''
        return self.positions[0]

    def remove_snake_piece(self):
        self.positions = self.positions[:-1]
        screen.fill(BOARD_BACKGROUND_COLOR)


class Stone(GameObject):
    '''Класс, описывающий игровой объект камень.'''

    def __init__(self, body_color: tuple[int, int, int] = STONE_COLOR) -> None:
        super().__init__(body_color)
        self.randomize_position()

    def randomize_position(self) -> None:
        '''Метод, который устанавливает случайное положение камня
        на игровом поле.
        '''
        GameObject.taken_positions.discard(self.position)
        self.position = choice(list(GameObject.all_positions
                                    - GameObject.taken_positions))
        GameObject.taken_positions.add(self.position)

    def draw(self, surface: pg.surface.Surface) -> None:
        '''Метод для отрисовки яблока на игровом поле.'''
        head_rect = pg.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(surface, self.body_color, head_rect)
        pg.draw.rect(surface, BORDER_COLOR, head_rect, 1)


def handle_keys(snake_object: Snake) -> None:
    '''Функция, которая обрабатывает нажатия клавиш,
    чтобы изменить направление движения змейки.
    '''
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
        if event.type == pg.KEYDOWN:
            snake_object.update_direction(
                DIRECTIONS.get((event.key, snake_object.direction))
            )


def handle_mouse(menu_object, *areas: MenuObject):
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button.
                # Check if the rect collides with the mouse pos.
                if pg.Rect(menu_object.start_button_position)\
                   .collidepoint(event.pos):
                    menu_object.start_game = True
                for area in areas:
                    for key, item in area.objects_rectangles.items():
                        if pg.Rect(item).collidepoint(event.pos):
                            area.current_object = key
                            area.clear_border(screen)
                            area.draw_border(screen)
                            print('Area clicked.')


def main():
    '''Функция, в которой происходит основной игровой цикл.'''
    start_menu = StartMenu()
    menu_snake_objects = MenuSnakeObjects()
    menu_apple_objects = MenuAppleObjects()
    menu_difficult_objects = MenuDifficultObjects()
    while not start_menu.start_game:
        clock.tick(SPEED)
        start_menu.draw(screen)
        menu_snake_objects.draw(screen)
        menu_snake_objects.draw_border(screen)
        menu_apple_objects.draw(screen)
        menu_apple_objects.draw_border(screen)
        menu_difficult_objects.draw(screen)
        menu_difficult_objects.draw_border(screen)
        handle_mouse(
            start_menu,
            menu_snake_objects,
            menu_apple_objects,
            menu_difficult_objects,
        )
        pg.display.update()
    snake = Snake(menu_snake_objects.objects_description
                  [menu_snake_objects.current_object])
    apple = Apple(menu_apple_objects.objects_description
                  [menu_apple_objects.current_object])
    rotten_apple = Rotten_apple()
    stone = Stone()
    while True:
        clock.tick(menu_difficult_objects.difficultes
                   [menu_difficult_objects.current_object])
        handle_keys(snake)
        snake.move()
        if apple.position == snake.get_head_position():
            snake.length += 1
            apple.randomize_position()
        if rotten_apple.position == snake.get_head_position():
            snake.length -= 1
            if snake.length >= 1:
                snake.remove_snake_piece()
            else:
                snake.reset()
            rotten_apple.randomize_position()
        if stone.position == snake.get_head_position():
            snake.reset()
            stone.randomize_position()
        snake.draw(screen)
        apple.draw(screen)
        rotten_apple.draw(screen)
        stone.draw(screen)
        pg.display.update()


if __name__ == '__main__':
    main()
