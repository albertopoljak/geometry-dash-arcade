import arcade
from constants import SCREEN_WIDTH, SCREEN_HEIGHT


class HoverButton(arcade.TextButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.theme:
            self.mouse_hover = False

    def set_mouse_hover(self, x, y):
        """Set mouse_hover attribute to True if coordinates hover over the button, False othervise."""
        if x > self.center_x + self.width / 2 or x < self.center_x - self.width / 2:
            self._on_hover_out()
            return
        if y > self.center_y + self.height / 2 or y < self.center_y - self.height / 2:
            self._on_hover_out()
            return

        self._on_hover_in()

    def _on_hover_in(self):
        if self.theme:
            self.mouse_hover = True

    def _on_hover_out(self):
        if self.theme:
            self.mouse_hover = False

    def draw_texture_theme(self):
        if self.pressed:
            arcade.draw_texture_rectangle(self.center_x, self.center_y, self.width, self.height, self.clicked_texture)
        elif self.mouse_hover:
            arcade.draw_texture_rectangle(self.center_x, self.center_y, self.width, self.height, self.hover_texture)
        else:
            arcade.draw_texture_rectangle(self.center_x, self.center_y, self.width, self.height, self.normal_texture)


class ActionButton(HoverButton):
    def __init__(self, action_function: callable,
                 x=SCREEN_WIDTH//2,
                 y=0.55*SCREEN_HEIGHT,
                 width=160, height=80,
                 theme=None):
        """
        :param action_function: Callable function reference to call on button press.
        """
        super().__init__(x, y, width, height, "Play", theme=theme)
        self.action_function = action_function

    def on_press(self):
        self.action_function()
