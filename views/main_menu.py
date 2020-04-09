import arcade
from views.loading import LoadingView
from utils.buttons import ActionButton, HoverButton
from constants import SCREEN_WIDTH, SCREEN_HEIGHT


class MenuView(arcade.View):
    def __init__(self):
        super().__init__()
        self.background = None
        self.button_theme = None
        self.setup()

    def setup(self):
        self.background = arcade.load_texture(":resources:images/backgrounds/abstract_1.jpg")
        self.setup_button_theme()
        self.button_list.append(ActionButton(action_function=self.play, button_text="Play", theme=self.button_theme))

    def setup_button_theme(self):
        self.button_theme = arcade.Theme()
        self.button_theme.set_font(26, arcade.color.WHITE)
        self._set_button_textures()

    def _set_button_textures(self):
        normal = "assets/images/main_button.png"
        hover = "assets/images/main_button_hover.png"
        self.button_theme.add_button_textures(normal, hover=hover)

    def on_mouse_motion(self, x: float, y: float, dx: float, dy: float):
        for button in self.button_list:
            if isinstance(button, HoverButton):
                button.set_mouse_hover(x, y)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_lrwh_rectangle_textured(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, self.background)
        arcade.draw_text("Geometry Dash", SCREEN_WIDTH/2, SCREEN_HEIGHT*0.8,
                         arcade.color.WHITE, font_size=50, anchor_x="center")
        super().on_draw()  # for buttons

    def play(self):
        self.window.show_view(LoadingView(level=1))
