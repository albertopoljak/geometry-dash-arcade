import arcade
from views.game import GameView
from constants import SCREEN_WIDTH, SCREEN_HEIGHT
from threading import Thread
import time


class LoadingView(arcade.View):
    def __init__(self, *, level: int):
        super().__init__()
        self.total = 0
        self.progress = 0
        self.background = None
        self.star = None
        self.progress_message = None
        self.setup()

    def setup(self):
        self.total = 3  # temp hardcoded for testing
        self.progress = 0
        self.background = arcade.load_texture(":resources:images/backgrounds/stars.png")
        self.star = arcade.Sprite(":resources:images/items/star.png", 1.5)
        self.star.center_x = SCREEN_WIDTH * 0.1
        self.star.center_y = SCREEN_HEIGHT // 2
        self.star.change_angle = -3
        self.progress_message = "test"

    def on_show(self):
        Thread(target=self.start_loading).start()

    def start_loading(self):
        game_view = GameView()
        for message in game_view.setup(1):
            self.progress_message = message
            self.progress += 1
            time.sleep(0.3)  # to get loading effect in case of fast load

        self.window.show_view(game_view)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_lrwh_rectangle_textured(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, self.background)
        arcade.draw_text("Loading", SCREEN_WIDTH//2, SCREEN_HEIGHT*0.8,
                         arcade.color.WHITE, font_size=50, anchor_x="center")

        arcade.draw_text(self.progress_message, SCREEN_WIDTH//2, SCREEN_HEIGHT*0.6,
                         arcade.color.WHITE, font_size=18, anchor_x="center")

        color1 = (255, 215, 0, 255)
        color2 = (255, 215, 0, 0)
        colors = (color2, color1, color1, color2)

        rectangle_x_left = SCREEN_WIDTH * 0.1
        rectangle_y_down = SCREEN_HEIGHT * 0.45
        rectangle_y_up = SCREEN_HEIGHT * 0.55

        progress_x = SCREEN_WIDTH * (self.progress / self.total) * 0.9 + SCREEN_WIDTH * 0.1

        points = ((rectangle_x_left, rectangle_y_down),
                  (progress_x, rectangle_y_down),
                  (progress_x, rectangle_y_up),
                  (rectangle_x_left, rectangle_y_up))

        rect = arcade.create_rectangle_filled_with_colors(points, colors)
        rect.draw()

        self.star.center_x = progress_x
        self.star.draw()

    def on_update(self, delta_time: float):
        self.star.update()
