from debug import debug
import pygame, sys, time
from settings import *
from level import Level
import sqlite3

class Game():
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDHTH, HEIGHTH))
        pygame.display.set_caption('Petrov K. A.')
        self.clock = pygame.time.Clock()

        self.level = Level()



    def run(self):
        screen = pygame.display.set_mode((WIDHTH, HEIGHTH))
        font = pygame.font.Font(None, 40)
        clock = pygame.time.Clock()
        input_box = pygame.Rect(WIDHTH // 2 - 128, HEIGHTH // 2, 512, 32)
        color_inactive = pygame.Color('dodgerblue2')
        color = color_inactive
        active = True
        self.text = ''
        done = False

        #создание БД
        db = sqlite3.connect('server.db')
        sql = db.cursor()
        saved = False
        sql.execute("""CREATE TABLE IF NOT EXISTS saves (
                            name TEXT,
                            point BIGINT,
                            date TEXT
                        )""")
        db.commit()

        distance = 600

        while not done:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                if event.type == pygame.KEYDOWN:
                    if active:
                        if event.key == pygame.K_RETURN:
                            done = True
                            self.level.player.curent_name = self.text
                            self.text = ''
                            self.runing = True
                        elif event.key == pygame.K_BACKSPACE:
                            self.text = self.text[:-1]
                        elif event.unicode:
                            self.text += event.unicode

            screen.fill((30, 30, 30))
            txt_surface = font.render(self.text, True, color)
            width = max(200, txt_surface.get_width() + 10)
            input_box.w = width
            screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
            pygame.draw.rect(screen, color, input_box, 2)
            debug('Добеги до конца пустыни, управляя персонажем при помощи стрелок или WASD.', 140, 250)
            debug('При столкновении с кактусами у персонажа будет уменьшаться здоровье.', 180, 250)
            debug('Нажатие на стрелку вверх или клавишу W даёт дополнительные очки', 220, 250)
            debug('Вводи своё имя, нажимай клавишу Enter и побежали)', 300, 350)
            pygame.display.flip()
            clock.tick(FPS)

        while self.runing:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            # Если игра закончилась проверка на прохождение снова
            keys = pygame.key.get_pressed()
            if keys[pygame.K_r] and self.level.player.win != 0:
                Game().run()

            if 5400 - self.level.player.hitbox.y > distance:
                distance += 600
                self.level.player.stats['points'] += 1000

            if self.level.player.direction.y == -1:
                self.level.player.stats['points'] += 1

            if self.level.player.hitbox.y < 50 and self.level.player.win == 0:
                self.level.player.stats['points'] += 5000
                self.level.player.camera_speed = 0
                self.level.player.speed = 0
                self.level.player.win = 1

            if self.level.player.stats['health'] <= 0:
                self.level.player.camera_speed = 0
                self.level.player.speed = 0
                self.level.player.win = -1

            if self.level.player.win != 0 and saved == False:
                saved = True
                self.level.player.curent_point = self.level.player.stats['points']
                sql.execute(f"INSERT INTO saves VALUES (?, ?, ?)", (self.level.player.curent_name, self.level.player.curent_point, self.level.player.curent_date))
                db.commit()

                for value in sql.execute("""SELECT *
                FROM saves
                ORDER BY point DESC
                LIMIT 5"""):
                    self.level.player.top_players.append(value)

            self.screen.fill((208, 199, 130))
            self.level.run()
            pygame.display.update()
            self.clock.tick(FPS)

if __name__ == '__main__':
    game = Game()
    game.run()