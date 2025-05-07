import arcade
from src.constants import (SCREEN_HEIGHT,
                            SCREEN_WIDTH,
                            PLAYER_MAX_HEALTH,
                            PLAYER_ATTAC_DISTANCE,
                            CAGE_WIDTH,
                            BOSS_WIDTH)

class Player:
    def __init__(self):
        self.center_x = SCREEN_WIDTH // 2
        self.center_y = 100
        self.width = 50
        self.height = 50
        self.color = arcade.color.BLUE
        self.texture = arcade.load_texture("./src/assets/images/player.png")
        self.max_health = PLAYER_MAX_HEALTH
        self.current_health = self.max_health
        self.energy = 0
        self.last_damage_time = 0
        
        self.change_x = 0
        self.change_y = 0

        self.move_direction = None

        self.cage_ruined = False
        self.current_screen = None

    def update(self):
        if self.current_screen == 'game_1':
            if ((abs(self.center_x + PLAYER_ATTAC_DISTANCE) >= SCREEN_WIDTH * 3 - CAGE_WIDTH and 
                self.move_direction == 'right' and 
                not self.cage_ruined)):
                self.change_x = 0
                self.change_y = 0

        if self.current_screen == 'game_2':
            if (abs(self.center_x + PLAYER_ATTAC_DISTANCE) >= SCREEN_WIDTH * 3 - BOSS_WIDTH and 
                self.move_direction == 'right'):
                    self.change_x = 0
                    self.change_y = 0

        self.center_x += self.change_x
        self.center_y += self.change_y

        self.center_x = max(self.width/2, min(SCREEN_WIDTH * 3 - self.width/2, self.center_x))
        self.center_y = max(self.height/2, min((SCREEN_HEIGHT / 3 * 2) - self.height/3, self.center_y))

    def draw(self):
        arcade.draw_texture_rect(
            self.texture,
            arcade.XYWH(self.center_x, self.center_y, self.width, self.height),
        )