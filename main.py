import arcade
import time
from src.classes.player import Player
from src.classes.enemy import Enemy
from src.classes.beer import Beer 
from src.constants import (SCREEN_HEIGHT, 
                           SCREEN_TITLE, 
                           SCREEN_WIDTH, 
                           BUTTON_WIDTH, 
                           BUTTON_HEIGHT, 
                           PLAYER_SPEED, 
                           PLAYER_ATTAC_DISTANCE, 
                           PLAYER_MAX_HEALTH, 
                           BEERS_HEALTH_ADD, 
                           CAGE_WIDTH,
                           CAGE_HEIGHT)

CONTROLS = (arcade.key.LEFT, 
            arcade.key.RIGHT, 
            arcade.key.A, 
            arcade.key.D, 
            arcade.key.UP,
            arcade.key.W, 
            arcade.key.DOWN, 
            arcade.key.S)

class GameWindow(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        arcade.set_background_color(arcade.color.BLACK)  

        self.current_screen = "fade"

        self.openinig_image = arcade.load_texture("./src/assets/images/placeholder.png")
        self.openinig_song = arcade.load_sound("./src/assets/sound/songs/raise_your_horns.wav", streaming=True)
        self.menu_background = arcade.load_texture("./src/assets/images/menu_bg.png")
        self.game_background = arcade.load_texture("./src/assets/images/game-bg.png")
        self.game_background_2 = arcade.load_texture("./src/assets/images/game-bg-2.png")
        self.lose_background = arcade.load_texture("./src/assets/images/lose-bg.png")
        self.alpha = 255
        self.heart_texture = arcade.load_texture("./src/assets/images/heart.png")
        self.cage_texture = arcade.load_texture("./src/assets/images/cage.png")
        self.cage_health = 500
        self.friend_texture = arcade.load_texture("./src/assets/images/friend.png")
        self.heart_size = 30
        self.start_time = time.time()
        self.fade_out_started = False
        self.button_textures = {
            "normal": arcade.load_texture("./src/assets/images/btn.png"),
            "hover": arcade.load_texture("./src/assets/images/btn_hover.png")
        }
        self.menu_buttons = [
            {"text": "Начать игру", "y": 400, "action": "game_1"},
            {"text": "Настройки", "y": 300, "action": "settings"},
            {"text": "Выход", "y": 200, "action": "exit"}
        ]
        self.lose_buttons = [
            {"text": "Начать заново", "y": 400, "action": "game_1"},
            {"text": "Выход", "y": 300, "action": "exit"}
        ]
        
        self.player = Player()

        self.camera = arcade.Camera2D()

        self.openinig_song.play(volume=0.5)

        self.enemies = []
        self.beers = []
        for  i in range(2):
            self.beers.append(Beer())

        self.spawn_timer = 0
        self.spawn_interval = 2.0 

        self.super_power_tooltip_showed = False

        self.lose = False

    def on_draw(self):
        self.clear()  

        if self.current_screen == "fade":
            arcade.draw_texture_rect(
                self.openinig_image,
                arcade.XYWH(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, SCREEN_WIDTH, SCREEN_HEIGHT),
                alpha=self.alpha
            )
        elif self.current_screen == "menu":
            self.draw_menu()
        elif self.current_screen == "game_1" or self.current_screen == "game_2":
            self.draw_game()

    def on_update(self, delta_time):
        current_time = time.time()

        if self.current_screen == 'game_1' or self.current_screen == "game_2":
            self.player.update()
            self.update_enemies(delta_time)
            self.check_enemy_collisions()
            self.check_collisions()

        if current_time - self.start_time >= 3 and not self.fade_out_started:
            self.fade_out_started = True
        
        if self.fade_out_started and self.alpha > 0:
            self.alpha -= 10  
            
        if self.alpha <= 0 and self.current_screen == "fade":
            self.alpha = 0
            self.current_screen = "menu"

        if self.current_screen == 'game_1' or self.current_screen == "game_2":
            self.player.update()

        if self.player and self.player.center_x > SCREEN_WIDTH / 2 and self.player.center_x + SCREEN_WIDTH / 2 <= SCREEN_WIDTH * 3 :
            self.camera.position = (self.player.center_x, self.camera.position.y)

    def update_enemies(self, delta_time):
        if self.lose: 
            return

        self.spawn_timer += delta_time
        
        # Спавн только если игрок не у правой границы
        if (self.spawn_timer >= self.spawn_interval 
            and len(self.enemies) < 10
            and self.player.center_x < SCREEN_WIDTH * 2.5):
            
            self.spawn_timer = 0
            self.enemies.append(Enemy(self.player))
        
        for enemy in self.enemies:
            if enemy.health <= 0:
                if self.player.energy < 100:
                    self.player.energy += 10

                self.enemies.remove(enemy)
            else:
                enemy.update()

    def check_collisions(self):
        current_time = time.time()

        for beer in self.beers:
            if (abs(self.player.center_x - beer.center_x) < (self.player.width + beer.width)/2 and
                abs(self.player.center_y - beer.center_y) < (self.player.height + beer.height)/2):
                    
                    if self.player.current_health < PLAYER_MAX_HEALTH:
                        if self.player.current_health + BEERS_HEALTH_ADD < PLAYER_MAX_HEALTH:
                            self.player.current_health += BEERS_HEALTH_ADD
                        else:
                            self.player.current_health = PLAYER_MAX_HEALTH

                        self.beers.remove(beer)
        
        for enemy in self.enemies:
            # Проверяем коллизию с игроком
            if (abs(self.player.center_x - enemy.center_x) < (self.player.width + enemy.width)/2 and
                abs(self.player.center_y - enemy.center_y) < (self.player.height + enemy.height)/2):

                enemy.moving = False

                # Проверяем можно ли нанести урон
                if current_time - enemy.last_damage_time >= enemy.damage_interval:
                    self.player.current_health = max(0, self.player.current_health - 10)
                    enemy.last_damage_time = current_time
            else:
                enemy.moving = True

    def check_enemy_collisions(self):
        # Проверяем коллизии между всеми парами врагов
        for i in range(len(self.enemies)):
            enemy1 = self.enemies[i]
            for j in range(i+1, len(self.enemies)):
                enemy2 = self.enemies[j]
                
                # Расчет пересечения по осям
                dx = abs(enemy1.center_x - enemy2.center_x)
                dy = abs(enemy1.center_y - enemy2.center_y)
                combined_width = (enemy1.width + enemy2.width) / 2
                combined_height = (enemy1.height + enemy2.height) / 2
                
                if dx < combined_width and dy < combined_height:
                    # Вычисляем вектор отталкивания
                    overlap_x = combined_width - dx
                    overlap_y = combined_height - dy
                    
                    # Корректируем позиции врагов
                    if overlap_x > overlap_y:
                        if enemy1.center_x < enemy2.center_x:
                            enemy1.center_x -= overlap_x/2
                            enemy2.center_x += overlap_x/2
                        else:
                            enemy1.center_x += overlap_x/2
                            enemy2.center_x -= overlap_x/2
                    else:
                        if enemy1.center_y < enemy2.center_y:
                            enemy1.center_y -= overlap_y/2
                            enemy2.center_y += overlap_y/2
                        else:
                            enemy1.center_y += overlap_y/2
                            enemy2.center_y -= overlap_y/2

        for enemy in self.enemies:
            enemy.center_x = max(
                enemy.width//2, 
                min(SCREEN_WIDTH * 3 - enemy.width//2, 
                enemy.center_x
            ))
            enemy.center_y = max(
                enemy.height//2, 
                min((SCREEN_HEIGHT // 3 * 2) - enemy.height//3, 
                enemy.center_y
            ))

    def draw_menu(self):
        arcade.draw_texture_rect(
            self.menu_background,
            arcade.XYWH(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, SCREEN_WIDTH, SCREEN_HEIGHT),
        )
        
        for button in self.menu_buttons:
            texture = self.button_textures["hover" if self.is_mouse_over_button(button) else "normal"]
            
            arcade.draw_texture_rect(
                texture,
                arcade.XYWH(SCREEN_WIDTH / 2, button['y'], BUTTON_WIDTH, BUTTON_HEIGHT),
            )
            
            arcade.Text(
                button["text"],
                SCREEN_WIDTH//2, button["y"],
                arcade.color.BLACK, 24,
                anchor_x="center", anchor_y="center"
            ).draw()

    def draw_game(self):
        if self.current_screen == 'game_1':
            arcade.draw_texture_rect(
                self.game_background,
                arcade.XYWH(SCREEN_WIDTH * 3  / 2, SCREEN_HEIGHT / 2, SCREEN_WIDTH * 3, SCREEN_HEIGHT),
                alpha= 128 if self.lose else 255
            )
        elif self.current_screen == 'game_2':
            arcade.draw_texture_rect(
                self.game_background_2,
                arcade.XYWH(SCREEN_WIDTH * 3  / 2, SCREEN_HEIGHT / 2, SCREEN_WIDTH * 3, SCREEN_HEIGHT),
                alpha= 128 if self.lose else 255
            )

        self.player.draw()
        self.camera.use()

        for enemy in self.enemies:
            enemy.draw()

        for beer in self.beers:
            beer.draw()

        self.draw_palyer_info()

        arcade.draw_texture_rect(
            self.friend_texture,
            arcade.XYWH(SCREEN_WIDTH * 3 - 25, SCREEN_HEIGHT / 3, 50, 50),
        )

        if self.cage_health != 0:
            arcade.draw_texture_rect(
                self.cage_texture,
                arcade.XYWH(SCREEN_WIDTH * 3 - CAGE_WIDTH / 2, SCREEN_HEIGHT / 3, CAGE_WIDTH, CAGE_HEIGHT),
            )
        else:
            self.player.cage_ruined = True

        if self.player.current_health == 0:
            self.lose = True

            arcade.draw_texture_rect(
                self.lose_background,
                arcade.XYWH(self.camera.position.x, SCREEN_HEIGHT / 2, 577, 307),
            )

            for button in self.lose_buttons:
                texture = self.button_textures["hover" if self.is_mouse_over_button(button) else "normal"]
                
                arcade.draw_texture_rect(
                    texture,
                    arcade.XYWH(self.camera.position.x, button['y'], BUTTON_WIDTH, BUTTON_HEIGHT),
                )
                
                arcade.Text(
                    button["text"],
                    self.camera.position.x, button["y"],
                    arcade.color.BLACK, 24,
                    anchor_x="center", anchor_y="center"
                ).draw()

    def draw_palyer_info(self):
        start_x = self.camera.position.x - (SCREEN_WIDTH / 2) + 30
        start_y = SCREEN_HEIGHT - 50
        
        arcade.draw_texture_rect(
            self.heart_texture,
            arcade.XYWH(start_x, start_y, self.heart_size, self.heart_size)
        )

        arcade.Text(
            f"{self.player.current_health}",
            start_x + 50,
            start_y,
            arcade.color.BLACK,
            18,
            font_name="Arial",
            anchor_y="center").draw()
        
        arcade.draw_texture_rect(
            self.heart_texture,
            arcade.XYWH(start_x, start_y - 50, self.heart_size, self.heart_size)
        )
        
        arcade.Text(
            f"{self.player.energy}",
            start_x + 50,
            start_y - 50,
            arcade.color.BLACK,
            18,
            font_name="Arial",
            anchor_y="center"
        ).draw()

        if self.player.energy == 100 and not self.super_power_tooltip_showed:
            arcade.Text(
            f"Нажми F для использования суперспособности",
            start_x - self.heart_size / 2,
            start_y - 80,
            arcade.color.BLACK,
            10,
            font_name="Arial",
            anchor_y="center"
            ).draw()


    def on_mouse_press(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            if self.is_mouse_over_button( self.menu_buttons[2], x, y) or self.is_mouse_over_button( self.lose_buttons[1], x, y):
                self.handle_button_click("exit")
            elif self.is_mouse_over_button( self.menu_buttons[0], x, y) or self.is_mouse_over_button( self.lose_buttons[0], x, y):
                self.handle_button_click("start")
            
        
    def is_mouse_over_button(self, button, x=None, y=None):
        if x is None or y is None:
            x, y = self.mouse["x"], self.mouse["y"]
            
        return (SCREEN_WIDTH//2 - BUTTON_WIDTH//2 < x < SCREEN_WIDTH//2 + BUTTON_WIDTH//2 and
                button["y"] - BUTTON_HEIGHT//2 < y < button["y"] + BUTTON_HEIGHT//2)
    
    def handle_button_click(self, action):
        if action == "exit":
            arcade.close_window()
        elif action == "start":
            self.current_screen = "game_1"

            if self.lose:
                self.lose = False
                self.player.current_health = PLAYER_MAX_HEALTH
                self.player.energy = 0
                self.player.center_x = SCREEN_WIDTH // 2
                self.player.center_y = 100
                self.camera.position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT / 2)
                self.enemies = []

    def on_key_press(self, symbol, modifiers):
        if self.lose: 
            return

        if (self.current_screen == "game_1"  or self.current_screen == "game_2") and self.player:
            if symbol == arcade.key.LEFT or symbol == arcade.key.A:
                self.player.change_x = -PLAYER_SPEED
                self.player.move_direction = 'left'
            elif symbol == arcade.key.RIGHT or symbol == arcade.key.D:
                self.player.change_x = PLAYER_SPEED
                self.player.move_direction = 'right'
            elif symbol == arcade.key.UP or symbol == arcade.key.W:
                self.player.move_direction = 'up'
                self.player.change_y = PLAYER_SPEED
            elif symbol == arcade.key.DOWN or symbol == arcade.key.S:
                self.player.move_direction = 'down'
                self.player.change_y = -PLAYER_SPEED
            # Базовая атака
            if symbol == arcade.key.SPACE:
                for enemy in self.enemies:
                    if (abs(self.player.center_x + PLAYER_ATTAC_DISTANCE - enemy.center_x) < (self.player.width + PLAYER_ATTAC_DISTANCE + enemy.width)/2 and
                        abs(self.player.center_y + PLAYER_ATTAC_DISTANCE - enemy.center_y) < (self.player.height + PLAYER_ATTAC_DISTANCE + enemy.height)/2):

                        enemy.health -= 50

                if (abs(self.player.center_x + PLAYER_ATTAC_DISTANCE) >= SCREEN_WIDTH * 3 - CAGE_WIDTH and
                    self.player.center_y >= SCREEN_HEIGHT / 3 - CAGE_HEIGHT / 2 and
                    self.player.center_y < SCREEN_HEIGHT / 3 + CAGE_HEIGHT / 2 and
                    self.cage_health > 0):
                    self.cage_health -= 50

            # Особая атака
            elif symbol == arcade.key.F:
                if self.player.energy == 100:
                    for enemy in self.enemies:
                        if self.camera.point_in_view((enemy.center_x, enemy.center_y)):
                            enemy.health -= enemy.health
                        
                    self.player.energy = 0
                    self.super_power_tooltip_showed = True

    def on_key_release(self, symbol, modifiers):
        if (self.current_screen == "game_1"  or self.current_screen == "game_2") and self.player:
            if symbol in CONTROLS:
                self.player.change_x = 0
                self.player.change_y = 0
                self.player.move_direction = None

def main():
    GameWindow(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    arcade.run()

if __name__ == "__main__":
    main()