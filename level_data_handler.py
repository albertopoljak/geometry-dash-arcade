import json
import logging
import arcade
from typing import List

logger = logging.getLogger(__name__)


class LevelDataHandler:
    DEFAULT_LEVEL_SPEED = -1

    def __init__(self):
        with open("level_settings.json") as f:
            self.level_settings = json.load(f)

    def get_level_speed(self, level_number: str) -> int:
        speed = self.level_settings[level_number]["level_speed"]
        if not isinstance(speed, int):
            logger.warning("Invalid data for level speed, using default speed.")
            return self.DEFAULT_LEVEL_SPEED
        elif speed > 0:
            logger.info("Obstacles need to move right to left! Inverting level speed to negative.")
            return -speed
        elif speed == 0:
            logger.info(f"Speed can't be 0, using default speed.")
            return self.DEFAULT_LEVEL_SPEED
        else:
            return speed

    def get_background_parallax_list(self, level_number: int) -> List[dict]:
        return self.level_settings[str(level_number)]["background_parallax_list"]


