import arcade
import time

# Настройки окна
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
SCREEN_TITLE = "Raven Rage: Soulburner's Last Chord"
BUTTON_WIDTH = 200
BUTTON_HEIGHT = 50

class GameWindow(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        arcade.set_background_color(arcade.color.BLACK)  

        self.current_screen = "fade"

        self.openinig_image = arcade.load_texture("./src/assets/images/placeholder.png")
        self.openinig_song = arcade.load_sound("./src/assets/sound/songs/raise_your_horns.wav", streaming=True)
        self.menu_background = arcade.load_texture("./src/assets/images/menu_bg.png")
        self.game_background = arcade.load_texture("./src/assets/images/game-bg.png")
        self.alpha = 255  
        self.start_time = time.time()
        self.fade_out_started = False
        self.button_textures = {
            "normal": arcade.load_texture("./src/assets/images/btn.png"),
            "hover": arcade.load_texture("./src/assets/images/btn_hover.png")
        }
        self.menu_buttons = [
            {"text": "Начать игру", "y": 400, "action": "game"},
            {"text": "Настройки", "y": 300, "action": "settings"},
            {"text": "Выход", "y": 200, "action": "exit"}
        ]

        self.openinig_song.play(volume=0.5)
    
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
        elif self.current_screen == "game":
            self.draw_game()

    def on_update(self, delta_time):
        current_time = time.time()

        if current_time - self.start_time >= 3 and not self.fade_out_started:
            self.fade_out_started = True
        
        if self.fade_out_started and self.alpha > 0:
            self.alpha -= 10  
            
        if self.alpha <= 0 and self.current_screen == "fade":
            self.alpha = 0
            self.current_screen = "menu"

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
            
            arcade.draw_text(
                button["text"],
                SCREEN_WIDTH//2, button["y"],
                arcade.color.BLACK, 24,
                anchor_x="center", anchor_y="center"
            )

    def draw_game(self):
        arcade.draw_texture_rect(
            self.game_background,
            arcade.XYWH(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, SCREEN_WIDTH, SCREEN_HEIGHT),
        )

    def on_mouse_press(self, x, y, button, modifiers):
            if button == arcade.MOUSE_BUTTON_LEFT:
                if self.is_mouse_over_button( self.menu_buttons[2], x, y):
                    self.handle_button_click("exit")
                elif self.is_mouse_over_button( self.menu_buttons[0], x, y):
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
            self.current_screen = "game"

def main():
    GameWindow(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    arcade.run()

if __name__ == "__main__":
    main()