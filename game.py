import pygame
import os
import sys
import random


FPS = 7
WIDTH = 736
HEIGHT = 544
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
    return x, y


tile_images = {
    'wall': load_image('wall.png'),
    'empty': load_image('grass.png')
}

tile_width = tile_height = STEP


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


pygame.display.set_caption('Змейка')
running = True
level_x, level_y = generate_level(load_level('map.txt'))
flag = True
while flag:
    sx = random.randrange(0, WIDTH - STEP, STEP)
    sy = random.randrange(0, HEIGHT - STEP, STEP)
    apple_x = random.randrange(0, WIDTH, STEP)
    apple_y = random.randrange(0, HEIGHT, STEP)
    if sx != apple_x and sy != apple_y:
        flag = False

rand_num = random.randint(0, 30)
apple_sprite = pygame.sprite.Sprite()
snake = [(sx,sy), (sx + STEP, sy + STEP)]
snake_len = 2
x_change = 0
y_change = 0

apple_sprite.image = load_image('apple.png')

apple_sprite.rect = apple_sprite.image.get_rect()
apple_pos = (apple_x, apple_y)
apple_sprite.rect.x = apple_x
apple_sprite.rect.y = apple_y
all_sprites.add(apple_sprite)

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
    if snake[-1] == apple_pos:
        apple_pos = random.randrange(0, WIDTH, STEP), random.randrange(0, HEIGHT, STEP)
        apple_sprite.rect.x, apple_sprite.rect.y = apple_pos

    sx += x_change
    sy += y_change
    snake.append([sx,sy])
    snake = snake[-snake_len:]
    tiles_group.draw(screen)
    all_sprites.draw(screen)
    for i, j in snake:
        (pygame.draw.rect(screen, pygame.Color('red'), (i, j, STEP, STEP)))
    pygame.display.flip()
    clock.tick(FPS)
pygame.quit()
