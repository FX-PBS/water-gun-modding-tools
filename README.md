# Water Gun Modding Tools

This repository offers scripts intended for modding equipment in Senran Kagura: Peach Beach Splash (PBS).

## Usage

### Project setup
Basic project setup goes as follows:
  - Make sure you have Python 3.13 or later installed
  - Download the project, which includes the scripts (currently wepc.py) and its dependencies in the Data folder
  - Open config.json in notepad and update "pbs_path" to where your game is located. The default path is set to "C:/Steam/steamapps/common/Senran Kagura Peach Beach Splash". If config.json paths are not valid, the script will fail

### Using wepc.py
wepc.py can be called from the command line as follows:
  - Open the command prompt and navigate to your folder. For help on basic command line use, read [here](https://www.geeksforgeeks.org/techtips/change-directories-in-command-prompt/)
  - Launch wepc.py to view the help message, which describes available options and usage examples

```
> cd /path/to/water-gun-modding-tools
> wepc.py
```

Changing weapon damage is as simple as passing a couple parameters. You need to specify the weapon, level and firing mode for this to work.
The following commands, which modify the level 10 assault rifle primary fire, will change close damage to 8 and far damage to 30:
```
> wepc.py assault 10 1 -d 8
> wepc.py assault 10 1 -D 30
```

This can be simplified into a simple command as follows:
```
> wepc.py assault 10 1 -d 8 -D 30
```

Of course more fun things can be tweaked for the guns. Consider the following:
```
> wepc.py sniper 10 1 -f 0 -r 3.5 -w 0.0
```

The above command changes level 10 sniper rifle primary to be an automatic, shoot faster and consume zero water.

If you want to be extra silly, try the following:
```
> wepc.py sniper 10 2 -c 5 -f 3 -a 0.75 -w 100 -p 1000 -B 2.5
```

I will let you find out what this does. :^)


## Reverting changes
You can manage recovery of WaterGunParam.bin in two ways:

1. Making a backup of WaterGunParam.bin with a different name prior to making changes (e.g., WaterGunParam.bin.bak), then renaming it back after deleting the modded one.

Assuming you tweaked config.json and made a backup accordingly, you can also run the following command to revert changes for you:
```
> wepc.py --load-backup
```

2. "Properties... -> Installed Files -> Verify ingefrity of game files" from the Steam library will recover game files to their original state. Note that this can remove other mods that you may have installed for PBS

## Managing save data
I always test mods using in-game save data specifically created for modding purposes, and I recommend you do the same. That way you can sleep well at night knowing that, after you finish playing around with mods, your original save file is perfectly legitimate for the usual singleplayer / multiplayer fun.

## Disclaimer
My tools are intended for recreational use to explore different possibilities of experiencing PBS. I do not endorse the scripts to be used for malicious uses, such as deliberately cheating in multiplayer or even singleplayer. Use these scripts responsibly.
