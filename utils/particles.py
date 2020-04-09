import arcade
from arcade.particle import Particle
from typing import cast
import random
from typing import Tuple


class EmitterOnDemand(arcade.Emitter):
    """
    Similar to base Emitter class only difference is that methods _emit() and update() are separated.
    Aka the update method no longer calls _emit() method, you need to do it manually.
    """

    def emit(self):
        """Makes _emit() public"""
        super()._emit()

    def update(self):
        self.center_x += self.change_x
        self.center_y += self.change_y
        self.angle += self.change_angle

        self._particles.update()
        particles_to_reap = [p for p in self._particles if cast(Particle, p).can_reap()]
        for dead_particle in particles_to_reap:
            dead_particle.kill()


class PlayerDashTrail(EmitterOnDemand):
    """
    Particle emitter built specifically for player dash trail.
    """
    PARTICLE_LIFETIME = 1.0

    def __init__(self, center_position: Tuple[float, float]):
        """
        :param center_position: tuple of x and y coordinates
        """
        super().__init__(center_xy=center_position,
                         emit_controller=arcade.EmitInterval(0.003),
                         particle_factory=lambda emitter: arcade.LifetimeParticle(
                             filename_or_texture=":resources:images/pinball/pool_cue_ball.png",
                             change_xy=arcade.rand_vec_spread_deg(180, 25, 1.0),
                             lifetime=random.uniform(self.PARTICLE_LIFETIME - 1.0, self.PARTICLE_LIFETIME),
                             scale=0.1,
                             alpha=32
                            )
                         )
