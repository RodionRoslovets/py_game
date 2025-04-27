import arcade
import math
from random import randint
from src.constants import SCREEN_HEIGHT, SCREEN_WIDTH
from src.classes.player import Player

class Enemy:
    def __init__(self, player:Player):
        self.player = player
        self.width = 50
        self.height = 50
        self.speed = 2
        self.health = 100
        self.texture = arcade.load_texture("./src/assets/images/enemy.png")
        self.last_damage_time = 0
        self.damage_interval = 2.0
        self.moving = True
        
        # Спавн справа от игрока с отступом 200 пикселей
        self.center_x = player.center_x + SCREEN_WIDTH + 200
        # Случайная позиция по Y с ограничениями игрока
        self.center_y = randint(
            int(self.height//2), 
            int((SCREEN_HEIGHT // 3 * 2) - self.height//3)
        )

    def update(self):
        # Расчет направления к игроку по обеим осям
        dx = self.player.center_x - self.center_x
        dy = self.player.center_y - self.center_y
        distance = math.hypot(dx, dy)

        if self.moving == True:
            if distance > 0:
                # Движение по обеим осям с нормализацией вектора
                self.center_x += self.speed * dx / distance
                self.center_y += self.speed * dy / distance
            
            # Вертикальные ограничения как у игрока
            self.center_y = max(
                self.height//2, 
                min((SCREEN_HEIGHT // 3 * 2) - self.height//3, 
                self.center_y
            ))
            
            # Горизонтальные ограничения игровой зоны
            self.center_x = max(
                self.width//2, 
                min(SCREEN_WIDTH * 3 - self.width//2, 
                self.center_x
            ))

    def draw(self):
        arcade.draw_texture_rect(
            self.texture,
            arcade.XYWH(self.center_x, self.center_y, self.width, self.height)
        )