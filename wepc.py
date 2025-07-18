
#############################
###                       ###
###        wepc.py        ###
###                       ###
#############################

# - A script for modding Senran Kagura: Peach Beach Splash
# - Changes contents of the WaterGunParam.bin file
# - Currently intended for command line use

import sys
import struct
import json

PBS_PATH = ''
WATER_GUN_PARAM_PATH = ''
DATA_PATH = ''

valid_options = ['-d', '-D', '-r', '-w', '-a']

# ---------------------------------------------------------

def print_help():
    """Print a help message to the console."""

    help_str = ('\nwepc - Weapon parameter changer\n\n'
                'DESCRIPTION\n'
                '  Modifies various parts the WaterGunParam.bin file based on arguments provided by the user.\n\n'
                '  The script is currently in a very primitive state, with the following limitations:\n'
                '  - script is hard-coded to write to level 10 assault rifle primary fire only\n'
                '  - must be run from command line\n'
                '  - limited error checking\n\n'
                '  *IMPORTANT* Be sure change the pbs_path field in config.json to match the location for your\n'
                '      copy of PBS, otherwise the script will fail.\n\n'

                'USAGE\n'
                '  wepc.py [option] [value]\n\n'

                'OPTIONS\n'
                '  -d       [float]     Damage value triggered before damage falloff\n'
                '  -D       [float]     Damage value triggered after damage falloff\n'
                '  -r       [float]     Changes base fire rate\n'
                '  -w       [float]     How much water is consumed per shot\n'
                '  -a       [float]     Accuracy value (0.0 - 1.0); 1.0 means 100% accuracy, 0.5 is 50%, etc.\n\n'

                'EXAMPLES\n'
                '  wepc.py -d 8 -D 30       Shots deal 8 damage up close and 30 from afar\n'
                '  wepc.py -r 99            Allows the water gun to fire 99 shots per second\n'
                '  wepc.py -w 0 -a 0.85     Firing does not consume water (infinite ammo) and accuracy is set to 80%\n\n'

                'NOTES\n'
                '  You have to restart the game to see your changes.')

    print(help_str)


def check_user_option_validity(options):
    """Verifies that user options can be understood by the script."""
    pass

def load_config():
    global PBS_PATH
    global WATER_GUN_PARAM_PATH
    global DATA_PATH

    with open('config.json') as config:
        config_json = json.load(config)

        PBS_PATH = config_json[0]['pbs_path']
        WATER_GUN_PARAM_PATH = config_json[0]['water_gun_param_path']
        DATA_PATH = config_json[0]['data_path']

def load_address_data():
    """Load the necessary JSON files for searching WaterGunParam.bin"""

    adds_json = None
    offs_json = None

    with open(DATA_PATH + 'WaterGunParam_addresses.json') as adds:
        adds_json = json.load(adds)
    with open(DATA_PATH + 'WaterGunParam_offsets.json') as offs:
        offs_json = json.load(offs)

    return (adds_json, offs_json)


def restore_backup():
    """Replaces WaterGunParam.bin with its backup."""
    pass

def display_current_values(weapon):
    """Displays current parameters for a specific weapon."""
    pass

def display_header(weapon):
    """Displays values for a weapon at the header."""
    pass

def assign_value(wgp, addresses, offsets, option, level, firing_mode, value):
    """
    Modifies WaterGunParam.bin based with a value based on the option\nNOTE: only level 10 assault rifle is modified in this version
    - wgp (file)
    - addresses (JSON)
    - offsets (JSON)
    - option (string)
    - level (string)
    - firing_mode (string)
    - value (string)
    """

    before = None
    after = None

    # NOTE: value is a string that is cast based on a matched option
    match option:
        case '-d':
            value = float(value)
            before, after = assign_param(addresses, offsets, 'close_damage', wgp, value, level, firing_mode, '<f')
            print_changes('Close damage', before, after, 'float')

        case '-D':
            value = float(value)
            before, after = assign_param(addresses, offsets, 'far_damage', wgp, value, level, firing_mode, '<f')
            print_changes('Far damage', before, after, 'float')

        case '-r':
            value = float(value)
            before, after = assign_param(addresses, offsets, 'fire_rate', wgp, value, level, firing_mode, '<f')
            print_changes('Fire rate', before, after, 'float')

        case '-w':
            value = float(value)
            before, after = assign_param(addresses, offsets, 'water_usage', wgp, value, level, firing_mode, '<f')
            print_changes('Water usage', before, after, 'float')

        case '-a':
            value = float(value)

            # Value must fall within reasonable range (0-1)
            if value > 1.0:
                value = 1.0
            elif value < 0.0:
                value = 0.0

            before, after = assign_param(addresses, offsets, 'accuracy', wgp, value, level, firing_mode, '<f')
            print_changes('Accuracy', before, after, 'percentage')

        case _:
            print('Unknown parameter')


def assign_param(addresses, offsets, param, wgp, value, level, firing_mode, type):
    wgp.seek(addresses[0]['parameters'][level][firing_mode] + offsets[1]['parameter_offsets'][param])
    pos = wgp.tell()
    before_modification = wgp.read(4)

    wgp.seek(addresses[0]['parameters'][level][firing_mode] + offsets[1]['parameter_offsets'][param])
    wgp.write(struct.pack(type, value))

    wgp.seek(pos)
    after_modification = wgp.read(4)

    return (struct.unpack(type, before_modification)[0], struct.unpack(type, after_modification)[0])


def print_changes(param_name, before, after, format_option):
    match format_option:
        case 'float':
            print('{}: {:.1f} -> {:.1f}'.format(param_name, before, after))
        case 'percentage':
            print('{}: {:.1f}% -> {:.1f}%'.format(param_name, before*100, after*100))


# ---------------------------------------------------------

if __name__ == '__main__':
    if len(sys.argv) <= 2:
        print_help()
        raise SystemExit()

    #check_user_option_validity(sys.argv[1:])

    load_config()
    addresses_json, offsets_json = load_address_data()

    with open(PBS_PATH + WATER_GUN_PARAM_PATH + 'WaterGunParam.bin', 'r+b') as wgp:
        for i in range(1, len(sys.argv[1:])):
            if sys.argv[i] in valid_options:
                assign_value(wgp, addresses_json, offsets_json, sys.argv[i], 'level_10', 'primary_fire', sys.argv[i+1])
