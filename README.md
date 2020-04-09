# Geometry dash arcade learning

I made this game to practise Python [Arcade library](https://arcade.academy/) for the
upcoming Python Discord game jam.

It features main menu, loading screen, modular parallax background, traps, jump-pads etc

![alt text](https://raw.githubusercontent.com/albertopoljak/geometry-dash-arcade/master/game_preview.png)


Since it was made for practise and to learn Arcade this was never
intended to be fully playable game. However the first level is there altho there is no win 
condition.

If I feel like it I might update it in future to add new things.


# Map editor

Use [Tiled map editor](https://www.mapeditor.org/)

You can either edit the existing map, or create new one by following this guide:

Create new project, initial settings are:

> Orientation: Orthogonal
>
> Tile layer format: Base64 (zlib compressed)*
>
> Tile render order: Right Down*
>
> Map size
> - Fixed 
> - Width: your choice (this is your level "size")
> - Height: 20*
>
> Tile size: 32*32


\* mark means recommended, you can choose another option other than this.


After you created new map project create new layers:

Create new tile layer named `obstacles` -  these represent blocks that the player can collide with and stand on.

Create new tile layer named `traps` - these represents blocks that will kill the player.

Create new tile layer named `jump_pads` - these represent blocks that will propel player 
at 2x jump height if he touches them.

Create your tileset - choose `Collection of images` and check `Embed in map` to True

(note that the program will make the source path relative to the current tmx save directory)

You can start placing tiles, be sure to select proper layer when placing.

### Tile placing recommendations*:

Default player vertical jump height is around 2.5 block, so put platforms in the heights of 2.
If there's a jump-pad then he can jump up to 7 blocks.

The furthest the player can horizontally jump is 1 block, with jump-pad this becomes 2 blocks.

If you want to have a roof you need to have 4 tiles of space (if the player touches the roof the game
will register this as a collision and you will lose).

*these recommendations were done with default constants/level speed of 5 in mind.


# License

See [LICENSE.md](LICENSE.md)

Code is licensed under MIT (c)  Alberto Poljak

#### Assets attribution:

##### Art:
Forest parallax background: Digital Moons https://digitalmoons.itch.io/parallax-forest-background

Button art: https://craftpix.net/freebies/free-buttons-2d-game-objects/

##### Music:
"Guitar-Mayhem-5.mp3" by Eric Matyas www.soundimage.org

