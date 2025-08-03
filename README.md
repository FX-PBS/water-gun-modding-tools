# Water Gun Modding Tools

This repository offers scripts intended for modding equipment in Senran Kagura: Peach Beach Splash (PBS).

## Usage

### Project setup
Basic project setup goes as follows:
  - Make sure you have Python 3.13 or later installed
  - Download the project, which includes the scripts and their dependencies
  - <b>Open config.json in notepad and update "pbs_dir" to where your game is located.</b> The default path is set to "C:/Steam/steamapps/common/Senran Kagura Peach Beach Splash". If config.json paths are not valid, the script will fail
  - (Optional) Create backups for "WaterGunParam.bin" and "WaterTankParam.bin" before you modify them using this tool. Rename the backups to "WaterGunParam.bin.bak" and "WaterTankParam.bin.bak", respectively. They can be found in the game's folders (GameData/Binary/Equip/)

### Using the scripts
Scripts are located in the src folder of the project. The following ones are available at your disposal:
- Weapon parameter changer (wepc.py)
- Tank parameter changer (tapc.py)

The simplest way to run these scripts goes as follows:
- Open the command prompt and navigate to your folder. For help on basic command line use, read [here](https://www.geeksforgeeks.org/techtips/change-directories-in-command-prompt/)
- Run the script directly, which will print out a help message:

```
cd /path/to/water-gun-modding-tools/src
wepc.py
```

Changing weapon damage is as simple as passing a couple parameters. You need to specify the weapon, level and firing mode for this to work.
The following commands, which modify the level 10 assault rifle primary fire, will change close damage to 8 and far damage to 30:
```
wepc.py assault 10 1 -d 8
wepc.py assault 10 1 -D 30
```

This can be simplified into a simple command as follows:
```
wepc.py assault 10 1 -d 8 -D 30
```

Of course more fun things can be tweaked for the guns. Consider the following:
```
wepc.py sniper 10 1 -f 0 -r 3.5 -w 0.0
```

The above command changes level 10 sniper rifle primary to be an automatic, shoot faster and consume zero water.

If you want to be extra silly, try the following (I'll let you find out what this does):
```
wepc.py sniper 10 2 -c 5 -f 3 -a 0.75 -w 100 -p 1000 -B 2.5
```

The water tank script follows the similar syntax as wepc.py. Consider the following:
```
tapc.py grenade -c 3000 -d 1 -B 2.1 -r 0 -R 500
```
To sum it up: water capacity is tripled; dashes are disabled but the initial dash "blink" has increased speed; normal reload does nothing, but passive reload is increased greatly. Try it out in-game!

Note that, unlike in wepc.py, you do not specify weapon level and firing mode in tapc.py. This is because the water tank binary doesn't care about these things and applies its settings to all guns equally. In other words, a level 1 grenade launcher will have the exact same water tank properties in-game as a level 10 grenade launcher.

## Reverting changes
You can revert your changes in two ways:

1. Recover the backups you created earlier like so:
```
wepc.py load-backup
tapc.py load-backup
```

You of course need to make sure your backups are indeed clean and haven't been tampered with.

2. "Properties... -> Installed Files -> Verify integrity of game files" from the Steam library will recover all of the game's files to their original state.

Some notes regarding the file integrity method:
- it will not remove any user-created files (e.g., save data, scripts, files that are not read by PBS itself)
- if you have other active PBS mods installed, they will be overwritten by the integrity check
- if you eventually plan to play the game normally, especially for multiplayer, I strongly recommend following this method after using this tool

## Managing save data
I always test mods using in-game save data specifically created for modding purposes, and I recommend you do the same. That way you can sleep well at night knowing that, after you finish playing around with mods, your original save file is perfectly legitimate for the usual singleplayer / multiplayer fun.

## Disclaimer
My tools are intended for recreational use to explore different possibilities of experiencing PBS. I do not endorse the scripts to be used for malicious uses, such as deliberately cheating in multiplayer or even singleplayer. Use these scripts responsibly.
