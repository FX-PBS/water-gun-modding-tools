# Water Gun Modding Tools

This repository offers scripts intended for modding equipment in Senran Kagura: Peach Beach Splash (PBS).
Currently the weapon parameter changer script (wepc.py) is in development, demonstrating changes on a level 10 assault rifle.

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

Changing weapon damage is as simple as passing a couple parameters. The following commands will change close damage to 8 and far damage to 30:
```
> wepc.py -d 8
> wepc.py -D 30
```

Water guns in PBS have a maximum water capacity of 1000. Below command will use up 1 water per shot:
```
> wepc.py -w 1.0
```

Options are still in development but can be combined. Below command combines close and far damage options, and adds an accuracy option at the end:
```
> wepc.py -d 33 -D 27 -a 0.66
```

## Reverting changes
The scripts will be designed with backup recovery in the future. In the meantime, you can manage recovery two ways:

1. Making a backup of WaterGunParam.bin with a different name prior to making changes (e.g., WaterGunParam.bin.bak), then renaming it back after deleting the modded one

2. "Properties... -> Installed Files -> Verify ingefrity of game files" from the Steam library will recover game files to their original state. Note that this can remove other mods that you may have installed for PBS

## Managing save data
I always test mods using in-game save data specifically created for modding purposes, and I recommend you do the same. That way you can sleep well at night knowing that, after you finish playing around with mods, your original save file is perfectly legitimate for the usual singleplayer / multiplayer fun.

## Disclaimer
My tools are intended for recreational use to explore different possibilities of experiencing PBS. I do not endorse the scripts to be used for malicious uses, such as deliberately cheating in multiplayer or even singleplayer. Use these scripts responsibly.
