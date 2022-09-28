import pygame
from settings import *
from tile import Tile
from player import Player
from heal import Heal
import random
from debug import debug


class Level:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()

        self.visible_sprites = YSortCameraGroup()
        self.obstacles_sprites = pygame.sprite.Group()

        self.create_map()

    def create_map(self):
        # Создаём пустой список для случайной карты
        Random_World_Map = []

        # Вписываем в список конец карты с финишем
        for j in range(10):
            Random_World_Map.append(WORLD_MAP[j])

        # Заполнение списка случайными блоками
        for i in range(len(WORLD_MAP) // 10 - 2):
            i = random.randint(1, len(WORLD_MAP) // 10 - 2)
            for j in range(10):
                Random_World_Map.append(WORLD_MAP[j + i * 10])

        # Вписываем в список конец начало карты с персонажем
        for j in range(10):
            Random_World_Map.append(WORLD_MAP[j + (len(WORLD_MAP) // 10 - 1) * 10])

        # Отображение сгененрированной случайной карты на экране
        for row_index, row in enumerate(Random_World_Map):
            for col_index, col in enumerate(row):
                x = col_index * TILESIZE
                y = row_index * TILESIZE
                if col == 'x':
                    Tile((x, y), [self.visible_sprites, self.obstacles_sprites])
                elif col == 'p':
                    self.player = Player((x, y), [self.visible_sprites], self.obstacles_sprites)
                    print("0")
                elif col == 'a':
                    Heal((x, y), [self.visible_sprites])

    def run(self):
        self.visible_sprites.custom_draw(self.player)
        self.visible_sprites.update()

class YSortCameraGroup(pygame.sprite.Group):
    def __init__(self):

        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.half_width = self.display_surface.get_size()[0] // 2
        self.half_height = self.display_surface.get_size()[1] // 2
        self.offset = pygame.math.Vector2()



    def custom_draw(self, player):
        self.offset.x = player.rect.centerx - self.half_width
        self.offset.y = player.rect.centery - self.half_height

        #for sprite in self.sprites():
        for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery):
            offset_pos = sprite.rect.topleft - self.offset
            self.display_surface.blit(sprite.image, offset_pos)