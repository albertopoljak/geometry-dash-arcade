import arcade
from copy import copy
from constants import SCREEN_WIDTH
from typing import List


class ScrollingSpriteList(arcade.SpriteList):
    def __init__(self, scroll_x_speed, **kwargs):
        super().__init__(**kwargs)
        self.scroll_x_speed = scroll_x_speed

    def update(self):
        self.move(self.scroll_x_speed, 0)
        super().update()


class FullWidthSpriteList(arcade.SpriteList):
    """"
    These sprites will always cover the entire screen width and be dynamically constructed as you
    move viewport around meaning you will get 'infinite' scroll effect.
    """
    def __init__(self, sprite: arcade.Sprite, y_coord, **kwargs):
        super().__init__(**kwargs)
        self.base_sprite = sprite
        self.y_coord = y_coord
        self.construct_initial_array()

    def construct_initial_array(self):
        """
        Adds enough sprite blocks so that the entire window width is populated.

        """
        base_sprite_width = int(self.base_sprite.width)
        # + 2 to make sure we have at least 3 sprites (beginning, middle, end)
        sprite_count = round(SCREEN_WIDTH // base_sprite_width) + 2
        for x_coord in range(-base_sprite_width,
                             sprite_count * base_sprite_width,
                             base_sprite_width):
            sprite = copy(self.base_sprite)
            sprite.center_x = x_coord
            sprite.center_y = self.y_coord
            self.append(sprite)

    def draw(self, reference_view_left: int, **kwargs):
        """
        :param reference_view_left: Left border position (x) of view.
        """
        if self[0].center_x >= reference_view_left:
            # We scrolled left so need to add tile to left and remove from right
            self.pop()
            sprite = copy(self.base_sprite)
            sprite.center_x = reference_view_left - self[0].width
            sprite.center_y = self.y_coord
            self.insert(0, sprite)
        elif self[-1].center_x <= reference_view_left + SCREEN_WIDTH:
            # We scrolled right so need to add tile to right and remove from left
            self.pop(0)
            sprite = copy(self.base_sprite)
            sprite.center_x = reference_view_left + self[0].width + SCREEN_WIDTH
            sprite.center_y = self.y_coord
            self.append(sprite)
        super().draw(**kwargs)


class FullWidthScrollingSprite(ScrollingSpriteList, FullWidthSpriteList):
    pass


class ParallaxBackground:
    def __init__(self, background_parallax_list: List[dict]):
        self.sprite_list_list = []
        for data_dict in background_parallax_list:
            layer = arcade.Sprite(data_dict["sprite"])
            self.sprite_list_list.append(FullWidthScrollingSprite(scroll_x_speed=data_dict["scroll_x_speed"],
                                                                  sprite=layer,
                                                                  y_coord=data_dict["y_coord"]))

    def draw(self, reference_view_left):
        for sprite_list in self.sprite_list_list:
            sprite_list.draw(reference_view_left)

    def update(self):
        for sprite_list in self.sprite_list_list:
            sprite_list.update()
