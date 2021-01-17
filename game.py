import pygame
import os
import sys
import random


FPS = 7
WIDTH = 768
HEIGHT = 576
STEP = 32


pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

player = None
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


def load_level(filename):
    filename = "data/" + filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))

    # дополняем каждую строку пустыми клетками ('.')
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == 'L':
                Tile('fon_u_l', x, y)
            elif level[y][x] == 'R':
                Tile('fon_u_r', x, y)
            elif level[y][x] == 'l':
                Tile('fon_d_l', x, y)
            elif level[y][x] == 'r':
                Tile('fon_d_r', x, y)
            elif level[y][x] == 'u':
                Tile('fon_up', x, y)
            elif level[y][x] == 'd':
                Tile('fon_down', x, y)
    return x, y


tile_images = {
    'wall': load_image('wall.png'),
    'empty': load_image('grass.png'),
    'fon_d_l': load_image('fon_d_l_angle.png'),
    'fon_d_r': load_image('fon_d_r_angle.png'),
    'fon_u_l': load_image('fon_u_l_angle.png'),
    'fon_u_r': load_image('fon_u_r_angle.png'),
    'fon_up': load_image('fon_up.png'),
    'fon_down': load_image('fon_down.png'),
}


tile_width = tile_height = STEP


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


class Snake(pygame.sprite.Group):
    def __init


pygame.display.set_caption('Змейка')
running = True
level_x, level_y = generate_level(load_level('map.txt'))
# прогружаем карту

flag = True
while flag:
    sx = random.randrange(0, WIDTH - STEP, STEP)
    sy = random.randrange(64, HEIGHT - STEP, STEP)
    apple_x = random.randrange(0, WIDTH, STEP)
    apple_y = random.randrange(64, HEIGHT, STEP)
    if sx != apple_x and sy != apple_y:
        flag = False
# генерируем положение змейки и яблока
# также осуществляется проверка на различное положение змейки и яблока.

snake = [(sx,sy)]
snake.append((sx + STEP, sy + STEP))
snake_len = 2
x_change = 0
y_change = 0
# задаём положение змейки, её длину
# также добавляем переменные, которые в дальнейшем помогут определить направление змейки

apple_sprite = pygame.sprite.Sprite()
apple_sprite.image = load_image('apple.png')
apple_sprite.rect = apple_sprite.image.get_rect()
apple_pos = (apple_x, apple_y)
apple_sprite.rect.x, apple_sprite.rect.y = apple_pos
all_sprites.add(apple_sprite)
# добавляем спрайт яблока, назначаем его положение, размеры. добавляем в общую группу спрайтов.

score = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and x_change != STEP:
                x_change = -STEP
                y_change = 0
            elif event.key == pygame.K_RIGHT and x_change != -STEP:
                x_change = STEP
                y_change = 0
            elif event.key == pygame.K_UP and y_change != STEP:
                x_change = 0
                y_change = -STEP
            elif event.key == pygame.K_DOWN and y_change != -STEP:
                x_change = 0
                y_change = STEP
    # управление змейкой. также добавляем проверку, чтобы змейка не могла повернуть в противоположное направление

    if snake[-1] == apple_pos:
        all_sprites.remove(apple_sprite)
        flag = True
        while flag:
            apple_pos = random.randrange(0, WIDTH, STEP), random.randrange(64, HEIGHT, STEP)
            for i in snake:
                if i == apple_pos:
                    break
            flag = False
        apple_sprite.rect.x, apple_sprite.rect.y = apple_pos
        fortune = random.randint(0, 30)
        if fortune in (5, 13, 17, 23, 28):
            apple_sprite.image = load_image('gold_apple.png')
            snake_len += 2
            FPS += 4
            score += random.randrange(30, 70, 2)
        else:
            apple_sprite.image = load_image('apple.png')
            score += 4
            snake_len += 1
        all_sprites.add(apple_sprite)
    # поедание змейкой яблока. также добавлено дополнительное(золотое) яблоко, которое выпадает игроку рандомно
    if (snake[0][0] < 0) or (snake[0][1] < 64) or (snake[0][0] > WIDTH - 32) or (snake[0][1] > HEIGHT - 32):
        running = False
    sx += x_change
    sy += y_change
    snake.append([sx,sy])
    snake = snake[-snake_len:]
    # увеличиваем змейку
    tiles_group.draw(screen)
    all_sprites.draw(screen)
    for i, j in snake:
        (pygame.draw.rect(screen, pygame.Color('red'), (i, j, STEP, STEP)))
    # прорисовываем карту, яблоки и змейку.
    text_font = pygame.font.Font('freesansbold.ttf', 64)
    score_text = text_font.render(str(score), True, (0, 0, 0))
    screen.blit(score_text, [8, 4])
    pygame.display.flip()
    clock.tick(FPS)
pygame.quit()
