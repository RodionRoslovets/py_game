import arcade
from random import randint
from src.constants import SCREEN_HEIGHT, SCREEN_WIDTH

class Beer:
    def __init__(self):
        self.width = 50
        self.height = 50
        self.texture = arcade.load_texture("./src/assets/images/beer.png")
        
        # Спавн справа от игрока с отступом 200 пикселей
        self.center_x = randint(
            SCREEN_WIDTH + 200, 
            int(SCREEN_WIDTH * 3)
        ) 
        # Случайная позиция по Y с ограничениями игрока
        self.center_y = randint(
            int(self.height//2), 
            int((SCREEN_HEIGHT // 3 * 2) - self.height//3)
        )

    def draw(self):
        arcade.draw_texture_rect(
            self.texture,
            arcade.XYWH(self.center_x, self.center_y, self.width, self.height)
        )