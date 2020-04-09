# Map editor

Use [Tiled](https://www.mapeditor.org/)

Create new project, initial settings are:

> Orientation: Orthogonal
>
> Tile layer format: Base64 (zlib compressed)*
>
> Tile render order: Right Down*

> Map size
> - Fixed 
> - Width: your choice (this is your level "size")
> - Height: 20*

> Tile size: 32*32


\* mark means recommended, you can choose another option other than this.


After you created new map project create new layers:

Create new tile layer named `obstacles` -  these represent blocks that the player can collide with and stand on.

Create new tile layer named `traps` - these represents blocks that will kill the player.

Create new tile layer named `jump_pads` - these represent blocks that will propel player 
at 2x jump height if he touches them.

Now load tiles to your tileset.

You can start placing tiles, be sure to select proper layer when placing.

Recommendations*:

Default player vertical jump height is around 2.5 block, so put platforms in the heights of 2.
If there's a jump-pad then he can jump up to 7 blocks.

The furthest the player can vertically jump is 1 block, with jump-pad this becomes 2 blocks.

If you want to have a roof you need to have 4 tiles of space (if the player touches the roof the game
will register this as a collision and you will lose).

*these recommendations were done with default constants/level speed of 5 in mind.