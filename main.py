import arcade
import time

# Настройки окна
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
SCREEN_TITLE = "Raven Rage: Soulburner's Last Chord"

class MyWindow(arcade.Window):
    def __init__(self, width, height, title):
        super().__init__(width, height, title)
        arcade.set_background_color(arcade.color.BLACK)  

        self.openinig_image = arcade.load_texture("./src/assets/images/placeholder.png")
        self.openinig_song = arcade.load_sound("./src/assets/sound/songs/raise_your_horns.wav", streaming=True)
        self.alpha = 255  
        self.start_time = time.time()
        self.fade_out_started = False

        self.openinig_song.play(volume=0.5)
    
    def on_draw(self):
        self.clear()  
        arcade.draw_texture_rect(
            self.openinig_image,
            arcade.XYWH(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, SCREEN_WIDTH, SCREEN_HEIGHT),
            alpha=self.alpha
        )
        

    def on_update(self, delta_time):
        current_time = time.time()
        
        if current_time - self.start_time >= 3 and not self.fade_out_started:
            self.fade_out_started = True
        
        if self.fade_out_started and self.alpha > 0:
            self.alpha -= 2  
            
        if self.alpha <= 0:
            self.alpha = 0

def main():
    MyWindow(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    arcade.run()

if __name__ == "__main__":
    main()