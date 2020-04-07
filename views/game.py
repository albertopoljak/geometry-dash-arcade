import arcade
from utils.debug import DebugView
from utils.sprites import ParallaxBackground
from utils.particles import PlayerDashTrail
from player import Player
from typing import Tuple
from level_data_handler import LevelDataHandler
from constants import SCREEN_WIDTH, SCREEN_HEIGHT, GRAVITY

level_data_handler = LevelDataHandler()
# How many pixels to keep as a minimum margin between the character and the edge of the screen.
BOTTOM_VIEWPORT_MARGIN = 16
TOP_VIEWPORT_MARGIN = 100

# Player start position
PLAYER_START_X = 0.2 * SCREEN_WIDTH
PLAYER_START_Y = 0.1 * SCREEN_HEIGHT


class GameView(DebugView):
    def __init__(self):
        super().__init__()
        self.view_bottom = 0
        self.view_left = 0
        self.obstacle_list = None
        self.trap_list = None
        self.background_list = None
        self.current_level = 1
        self.level_speed = 1
        self.player = None
        self.music = None
        self.physics_engine = None
        self.player_dash_trail = None

    def setup(self, level_number: int):
        # Used to keep track of our scrolling
        self.view_bottom = 0
        self.view_left = 0

        yield "Starting setup"
        self.obstacle_list = arcade.SpriteList()
        self.trap_list = arcade.SpriteList()

        self.level_speed = level_data_handler.get_level_speed(str(level_number))

        floor = arcade.Sprite("assets/images/floor.png", 2)
        floor.position = (SCREEN_WIDTH // 2, 0)
        self.obstacle_list.append(floor)

        for x in range(SCREEN_WIDTH//2, SCREEN_WIDTH//2 + 32*10, 32):
            obstacle = arcade.Sprite(":resources:images/tiles/planet.png", 0.25)
            obstacle.position = (x, 40)
            obstacle.change_x = self.level_speed
            self.obstacle_list.append(obstacle)
        """
        spikes = arcade.Sprite(":resources:images/tiles/spikes.png", 0.25)
        spikes.position = (SCREEN_WIDTH // 2 + 300, 100)
        spikes.change_x = self.level_speed
        self.trap_list.append(spikes)

        spikes2 = arcade.Sprite(":resources:images/tiles/spikes.png", 0.25)
        spikes2.position = (SCREEN_WIDTH // 2 + 150, 50)
        spikes2.change_x = self.level_speed
        self.trap_list.append(spikes2)

        spikes3 = arcade.Sprite(":resources:images/tiles/spikes.png", 0.25)
        spikes3.position = (SCREEN_WIDTH // 2 + 190, 50)
        spikes3.change_x = self.level_speed
        self.trap_list.append(spikes3)"""

        yield "Loading backgrounds.."
        background_parallax_list = level_data_handler.get_background_parallax_list(level_number)
        self.background_list = ParallaxBackground(background_parallax_list)

        self.player = Player()
        self.player.center_x = PLAYER_START_X
        self.player.center_y = PLAYER_START_Y

        self.player_dash_trail = PlayerDashTrail(self.get_player_dash_trail_position())

        yield "Loading music"
        self.music = arcade.load_sound("assets/sounds/Guitar-Mayhem-5.mp3")
        arcade.play_sound(self.music)

        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player, self.obstacle_list, GRAVITY)

    def get_player_dash_trail_position(self) -> Tuple[float, float]:
        # 0.85 because we don't want particle emitter to be at bottom bottom.
        return (self.player.center_x - self.player.width // 2,
                self.player.center_y - self.player.height * 0.85)

    def on_draw(self):
        arcade.start_render()
        self.background_list.draw(self.view_left)
        self.obstacle_list.draw()
        self.trap_list.draw()
        self.player_dash_trail.draw()
        self.player.draw()

    def on_key_press(self, key, modifiers: int):
        if key in (arcade.key.UP, arcade.key.W, arcade.key.SPACE):
            if self.physics_engine.can_jump():
                self.player.jump()

    def on_update(self, delta_time: float):
        # We're making obstacles move to player, the player X coordinate will be static.
        # For further comments this will be referred as 'player X coordinate hack'
        self.player.center_x = PLAYER_START_X
        if arcade.check_for_collision_with_list(self.player, self.trap_list):
            print("You felt into trap")
            self.reset_level()

        # Call engine update after collision check and player X coordinate hack in order for those to work properly.
        collision_sprite_list = self.physics_engine.update()
        for collision_sprite in collision_sprite_list:
            if collision_sprite in self.obstacle_list:
                self.player_dash_trail.emit()

        self.player_dash_trail.update()
        self.trap_list.update()

        # Using our player X coordinate hack when we hit a moving wall the Physics engine will try to move us
        # (since everything is scrolling right to left we will be moved left) but since we're resetting the player X
        # coordinate it will "teleport" us above the obstacle after it moves us a certain number of pixels to the left.
        # The 6 is not fixed it can be loose, I just choose it because it worked the best.
        if PLAYER_START_X > self.player.center_x + 6:
            print("You collided with obstacle")
            self.reset_level()

        # If player (somehow) falls of screen then reset level (invalid tmx file or users playing around with map code)
        if self.player.center_y <= -300:
            print("You somehow managed to fell off screen.")
            self.reset_level()

        self.background_list.update()
        self.viewport_update()

    def reset_level(self):
        arcade.stop_sound(self.music)
        # temporal for testing load view, exhaust generator
        for _ in self.setup(self.current_level):
            pass

    def viewport_update(self):
        changed = False

        # Scroll up
        top_boundary = self.view_bottom + SCREEN_WIDTH - TOP_VIEWPORT_MARGIN
        if self.player.top > top_boundary:
            self.view_bottom += self.player.top - top_boundary
            changed = True

        # Scroll down
        bottom_boundary = self.view_bottom + BOTTOM_VIEWPORT_MARGIN
        if self.player.bottom < bottom_boundary:
            self.view_bottom -= bottom_boundary - self.player.bottom
            changed = True

        if changed:
            # Only scroll to integers. Otherwise we end up with pixels that
            # don't line up on the screen
            self.view_bottom = int(self.view_bottom)
            self.view_left = int(self.view_left)

            # Do the scrolling
            arcade.set_viewport(self.view_left,
                                SCREEN_WIDTH + self.view_left,
                                self.view_bottom,
                                SCREEN_HEIGHT + self.view_bottom)
