import pygame
from settings import *
from debug import debug
from datetime import datetime


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, obstacle_sprites):
        super().__init__(groups)
        self.image = pygame.image.load('Sprites/Character/walk/walk up4.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (128, 128))
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(-108, -112)

        self.import_player_assets()
        self.status = 'up'
        self.frame_index = 0
        self.animation_speed = 0.15

        self.direction = pygame.math.Vector2()
        self.speed = 5
        self.camera_speed = 3.2

        self.attacking = False
        self.attack_cooldown = 300
        self.attack_time = None

        now = datetime.now()
        self.curent_name = ''
        self.curent_point = 0
        self.curent_date = now.strftime("%m/%d/%Y, %H:%M:%S")

        self.stats = {'health': 100, 'points' : 0}
        self.win = 0

        self.top_players = []

        self.obstacle_sprites = obstacle_sprites

    def import_player_assets(self):
        character_path = 'Sprites/Character'
        self.animations = {'up': [], 'down': [],'left': [], 'right': [],
                           'a_up': [], 'a_down': [], 'a_left': [], 'a_right': []}

        self.animations['right'] = [pygame.image.load("Sprites/Character/walk/walk right1.png").convert_alpha(),
                                    pygame.image.load("Sprites/Character/walk/walk right2.png").convert_alpha(),
                                    pygame.image.load("Sprites/Character/walk/walk right3.png").convert_alpha(),
                                    pygame.image.load("Sprites/Character/walk/walk right4.png").convert_alpha()]
        self.animations['left'] = [pygame.image.load("Sprites/Character/walk/walk left1.png").convert_alpha(),
                                    pygame.image.load("Sprites/Character/walk/walk left2.png").convert_alpha(),
                                    pygame.image.load("Sprites/Character/walk/walk left3.png").convert_alpha(),
                                    pygame.image.load("Sprites/Character/walk/walk left4.png").convert_alpha()]
        self.animations['down'] = [pygame.image.load("Sprites/Character/walk/walk down1.png").convert_alpha(),
                                    pygame.image.load("Sprites/Character/walk/walk down2.png").convert_alpha(),
                                    pygame.image.load("Sprites/Character/walk/walk down3.png").convert_alpha(),
                                    pygame.image.load("Sprites/Character/walk/walk down4.png").convert_alpha()]
        self.animations['up'] = [pygame.image.load("Sprites/Character/walk/walk up1.png").convert_alpha(),
                                    pygame.image.load("Sprites/Character/walk/walk up2.png").convert_alpha(),
                                    pygame.image.load("Sprites/Character/walk/walk up3.png").convert_alpha(),
                                    pygame.image.load("Sprites/Character/walk/walk up4.png").convert_alpha()]

        self.animations['a_right'] = [pygame.image.load("Sprites/Character/attack/attack right1.png").convert_alpha(),
                                    pygame.image.load("Sprites/Character/attack/attack right2.png").convert_alpha(),
                                    pygame.image.load("Sprites/Character/attack/attack right3.png").convert_alpha(),
                                    pygame.image.load("Sprites/Character/attack/attack right4.png").convert_alpha()]
        self.animations['a_left'] = [pygame.image.load("Sprites/Character/attack/attack left1.png").convert_alpha(),
                                    pygame.image.load("Sprites/Character/attack/attack left2.png").convert_alpha(),
                                    pygame.image.load("Sprites/Character/attack/attack left3.png").convert_alpha(),
                                    pygame.image.load("Sprites/Character/attack/attack left4.png").convert_alpha()]
        self.animations['a_down'] = [pygame.image.load("Sprites/Character/attack/attack down1.png").convert_alpha(),
                                    pygame.image.load("Sprites/Character/attack/attack down2.png").convert_alpha(),
                                    pygame.image.load("Sprites/Character/attack/attack down3.png").convert_alpha(),
                                    pygame.image.load("Sprites/Character/attack/attack down4.png").convert_alpha()]
        self.animations['a_up'] = [pygame.image.load("Sprites/Character/attack/attack up1.png").convert_alpha(),
                                    pygame.image.load("Sprites/Character/attack/attack up2.png").convert_alpha(),
                                    pygame.image.load("Sprites/Character/attack/attack up3.png").convert_alpha(),
                                    pygame.image.load("Sprites/Character/attack/attack up4.png").convert_alpha() ]

        self.animations['death'] = [pygame.image.load("Sprites/Character/death/death1.png").convert_alpha(),
                                   pygame.image.load("Sprites/Character/death/death2.png").convert_alpha(),
                                   pygame.image.load("Sprites/Character/death/death3.png").convert_alpha(),
                                   pygame.image.load("Sprites/Character/death/death4.png").convert_alpha()]

        for key in self.animations:
            for i in range(4):
                self.animations[key][i] = pygame.transform.scale(self.animations[key][i], (128, 128))

    def input(self):
        keys = pygame.key.get_pressed()

        # перемещение
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.direction.y = -1
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.direction.y = 1
        else:
            self.direction.y = 0

        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.direction.x = 1
        elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.direction.x = -1
        else:
            self.direction.x = 0

        # атака
        if keys[pygame.K_SPACE] and not self.attacking:
            self.attacking = True
            self.attack_time = pygame.time.get_ticks()
            WORLD_MAP[0][0] = ' '

    def get_status(self):

        if (self.direction.x == 0 and self.direction.y == 0) or (self.direction.x == 0 and self.direction.y == -1):
            if self.attacking or self.win == 1:
                self.status = 'a_up'
            else:
                self.status = 'up'

        if self.direction.x == 1 or self.win == 1:
            if self.attacking:
                self.status = 'a_right'
            else:
                self.status = 'right'

        if self.direction.x == -1 or self.win == 1:
            if self.attacking:
                self.status = 'a_left'
            else:
                self.status = 'left'

        if self.direction.y == 1 or self.win == 1:
            if self.attacking:
                self.status = 'a_down'
            else:
                self.status = 'down'

        if self.stats['health'] == 0:
            self.status = 'death'

    def animate(self):
        animation = self.animations[self.status]

        self.frame_index += self.animation_speed
        if self.frame_index >= 3:
            self.frame_index = 0

        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center = self.hitbox.center)

    def move(self, speed, camera_speed):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        self.hitbox.x += self.direction.x * speed
        self.collisison('horizontal')
        self.hitbox.y += self.direction.y * speed - camera_speed
        self.collisison('vertical')
        self.rect.center = self.hitbox.center

    def collisison(self, direction):
        if direction == 'horizontal':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    self.stats['health' ] -= 2
                    if self.direction.x > 0:
                        self.hitbox.right = sprite.hitbox.left
                    if self.direction.x < 0:
                        self.hitbox.left = sprite.hitbox.right

        if direction == 'vertical':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    self.stats['health'] -= 2
                    if self.direction.y >= 0:
                        self.hitbox.bottom = sprite.hitbox.top
                    if self.direction.y <= 0:
                        self.hitbox.top = sprite.hitbox.bottom

    def cooldowns(self):
        current_time = pygame.time.get_ticks()

        if self.attacking:
            if current_time - self.attack_time >= self.attack_cooldown:
                self.attacking = False

    def update(self):
        self.input()
        self.move(self.speed, self.camera_speed)
        self.cooldowns()
        self.get_status()
        self.animate()
        if self.win == 0:
            s = 'Здоровье: ' + str(self.stats['health']) + ' Очки: ' + str(self.stats['points'])
            debug(s, 20, WIDHTH // 2 - 150)
        else:
            s = '__________________________________'
            debug(s, 120, 460)
            if self.win == -1:
                s = 'ПРОИГРЫШ'
            elif self.win == 1:
                s = 'ПОБЕДА!'
            debug(s, 170, 580)
            s = 'Нажмите R, чтобы начать игру снова'
            debug(s, 220, 460)
            s = '__________________________________'
            debug(s, 270, 460)
            s = 'Имя: ' + str(self.curent_name) + ' Дата и время: ' + str(self.curent_date) + ' Очки: ' + str(self.curent_point)
            debug(s, 420, 400)

            s = 'ТОП ИГРОКОВ'
            debug(s, 470, 580)

            s = '1. Имя: ' + str(self.top_players[0][0]) + ' Дата и время: ' + str(self.top_players[0][2]) + ' Очки: ' + str(
                self.top_players[0][1])
            debug(s, 500, 380)
            s = '2. Имя: ' + str(self.top_players[1][0]) + ' Дата и время: ' + str(self.top_players[1][2]) + ' Очки: ' + str(
                self.top_players[1][1])
            debug(s, 530, 380)
            s = '3. Имя: ' + str(self.top_players[2][0]) + ' Дата и время: ' + str(self.top_players[2][2]) + ' Очки: ' + str(
                self.top_players[2][1])
            debug(s, 560, 380)
            s = '4. Имя: ' + str(self.top_players[3][0]) + ' Дата и время: ' + str(self.top_players[3][2]) + ' Очки: ' + str(
                self.top_players[3][1])
            debug(s, 590, 380)
            s = '5. Имя: ' + str(self.top_players[4][0]) + ' Дата и время: ' + str(self.top_players[4][2]) + ' Очки: ' + str(
                self.top_players[4][1])
            debug(s, 620, 380)

            ##print(self.top_players)


