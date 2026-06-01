# Love2d builder

This is an app that is used mostly for scripts that are meant for game dev in love2d or any other graphics library / game engine.

## Current features

Now this can only automatically make `.png` from `.aseprite` / `.ase` file and preserve the file structure.

## Config

```json
{
    "asepriteFolder" : "aseprite",
    "outputFolder" : "assets",
    "asepriteCommand" : "place where is your aseprite.exe file (or shell shortcut to it)"
}
```

- `asepriteFolder` is folder where you store your aseprite files you want to save to your preferred type.
- `outputFolder` is folder where you images will be save into.
- `asepriteCommand` is command used for accessing aseprite. You have to own aseprite. This can be in form of absolute path for you `aseprite.exe` file or shell variable.
- `convertType` type of file you want to convert aseprite into. Defaults to `.png`.

>NOTE: all of these can be changed into ay value by just running the script will shell input, everything has the same name as in config except you have to use `--`, so to change convertType you have to use `--convertType .jpg`.
