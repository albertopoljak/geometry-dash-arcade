import arcade
from views.main_menu import MenuView
from constants import TITLE, SCREEN_WIDTH, SCREEN_HEIGHT


def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, TITLE)
    window.show_view(MenuView())
    arcade.run()


if __name__ == "__main__":
    main()
