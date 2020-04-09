import arcade
from constants import PLAYER_JUMP_SPEED


class Player(arcade.Sprite):
    ANGLE_CHANGE = 5  # has to be divisor of 90

    def __init__(self, image="assets/images/player.png", jump_sound="assets/sounds/jump.wav"):
        super().__init__(image)
        self.jump_sound = arcade.load_sound(jump_sound)

    def jump(self, *, big_jump=False):
        """
        Make the player jump and handles his rotation.
        :param big_jump: bool, if true the jump will be 1.6 times more powerful (useful for jump-pads)
        """
        if big_jump:
            self.change_y = PLAYER_JUMP_SPEED * 1.6
        else:
            self.change_y = PLAYER_JUMP_SPEED

        self.angle -= self.ANGLE_CHANGE  # to kick-start update
        self.change_angle = - self.ANGLE_CHANGE
        arcade.play_sound(self.jump_sound)

    def draw(self):
        super().draw()
        if self.angle % 90 == 0:
            self.change_angle = 0
