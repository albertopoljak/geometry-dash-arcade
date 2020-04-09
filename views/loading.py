import arcade
from views.game import GameView
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, GAME_LOAD_COUNT
from threading import Thread
import time


class LoadingView(arcade.View):
    def __init__(self, *, level: int):
        super().__init__()
        self.level = level
        self.progress = 0
        self.title_text = None
        self.background = None
        self.star = None
        self.progress_message = None
        self.setup()

    def setup(self):
        self.progress = 0
        self.title_text = arcade.draw_text("Loading", SCREEN_WIDTH//2, SCREEN_HEIGHT*0.8,
                                           arcade.color.WHITE, font_size=50, anchor_x="center")
        self.background = arcade.load_texture(":resources:images/backgrounds/stars.png")
        self.star = arcade.Sprite(":resources:images/items/star.png", 1.5)
        self.star.center_x = SCREEN_WIDTH * 0.1
        self.star.center_y = SCREEN_HEIGHT // 2
        self.star.change_angle = -3
        self.progress_message = "Initializing"

    def on_show(self):
        Thread(target=self.start_loading, args=(self.level,)).start()

    def start_loading(self, level: int):
        game_view = GameView()
        for message in game_view.setup(level):
            if self.progress < GAME_LOAD_COUNT:
                self.progress_message = message
                self.progress += 1
                time.sleep(1)  # to get loading effect in case of fast load
            else:
                self.progress_message = "Finishing.."

        self.window.show_view(game_view)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_lrwh_rectangle_textured(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, self.background)
        self.title_text.draw()

        arcade.draw_text(self.progress_message, SCREEN_WIDTH//2, SCREEN_HEIGHT*0.6,
                         arcade.color.WHITE, font_size=18, anchor_x="center")

        gradient_color1 = (255, 215, 0, 255)
        gradient_color2 = (255, 215, 0, 0)
        gradient_colors = (gradient_color2, gradient_color1, gradient_color1, gradient_color2)

        loading_bar_x_left = SCREEN_WIDTH * 0.1
        loading_bar_y_down = SCREEN_HEIGHT * 0.45
        loading_bar_y_up = SCREEN_HEIGHT * 0.55

        loading_bar_progress_x = SCREEN_WIDTH * 0.8 * (self.progress / GAME_LOAD_COUNT) + SCREEN_WIDTH * 0.1

        points = ((loading_bar_x_left, loading_bar_y_down),
                  (loading_bar_progress_x, loading_bar_y_down),
                  (loading_bar_progress_x, loading_bar_y_up),
                  (loading_bar_x_left, loading_bar_y_up))

        loading_bar = arcade.create_rectangle_filled_with_colors(points, gradient_colors)
        loading_bar.draw()

        self.star.center_x = loading_bar_progress_x
        self.star.draw()

    def on_update(self, delta_time: float):
        self.star.update()
