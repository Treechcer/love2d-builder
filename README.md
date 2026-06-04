# Love2d builder

This is an app that is used mostly for scripts that are meant for game dev in love2d or any other graphics library / game engine.

## Current features

Now this can only automatically make `.png` from `.aseprite` / `.ase` file and preserve the file structure.

## Config

All your projects have to their own config file. It has to be in `./love2d-builder/config.json`. It should have the same json structure, if it doesn't it can default into some values which may do something you're not anticipating, be careful.

```json
{
    "asepriteFolder" : "aseprite",
    "outputFolder" : "assets",
    "asepriteCommand" : "C:\ase\aseprite.exe"
}
```

- `asepriteFolder` is folder where you store your aseprite files you want to save to your preferred type.
- `outputFolder` is folder where you images will be save into.
- `asepriteCommand` is command used for accessing aseprite. You have to own aseprite. This can be in form of absolute path for you `aseprite.exe` file or shell variable.
- `convertType` type of file you want to convert aseprite into. Defaults to `.png`.

>NOTE: all of these can be changed into ay value by just running the script will shell input, everything has the same name as in config except you have to use `--`, so to change convertType you have to use `--convertType .jpg`.

## Logging

Things that this script are logged. It's logged into file `./love2d-builder/logger.txt`. Errors / exceptions are logged, file exports etc.

## State

- This is in development, not really active, it's side project, any issues will be answered.
