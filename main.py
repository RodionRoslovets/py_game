import arcade

# Настройки окна
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
SCREEN_TITLE = "Raven Rage: Soulburner's Last Chord"

class MyWindow(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        arcade.set_background_color(arcade.color.BLUE)  
    
    def on_draw(self):
        self.clear()  
        arcade.draw_text(
            "Howdy ho!",
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 2,
            arcade.color.WHITE,
            font_size=24,
            anchor_x="center"
        )

def main():
    MyWindow(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    arcade.run()

if __name__ == "__main__":
    main()