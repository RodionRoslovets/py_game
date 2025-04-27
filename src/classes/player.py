import arcade
from src.constants import SCREEN_HEIGHT, SCREEN_WIDTH

class Player:
    def __init__(self):
        self.center_x = SCREEN_WIDTH // 2
        self.center_y = 100
        self.width = 50
        self.height = 50
        self.color = arcade.color.BLUE
        self.texture = arcade.load_texture("./src/assets/images/player.png")
        self.max_health = 100
        self.current_health = self.max_health
        
        self.change_x = 0
        self.change_y = 0

    def update(self):
        self.center_x += self.change_x
        self.center_y += self.change_y

        self.center_x = max(self.width/2, min(SCREEN_WIDTH * 3 - self.width/2, self.center_x))
        self.center_y = max(self.height/2, min((SCREEN_HEIGHT / 3 * 2) - self.height/3, self.center_y))

    def draw(self):
        arcade.draw_texture_rect(
            self.texture,
            arcade.XYWH(self.center_x, self.center_y, self.width, self.height),
        )