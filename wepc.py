###########################
##                       ##
##        wepc.py        ##
##                       ##
###########################

# - A script for modding Senran Kagura: Peach Beach Splash
# - Changes contents of the WaterGunParam.bin file
# - Currently intended for command line use

import sys
import shutil
import struct
import json

PBS_PATH = ""
WATER_GUN_PARAM_PATH = ""
BACKUP_NAME = ""
DATA_PATH = ""
ASSETS_PATH = ""

HELP = ""
HELP_C = ""

valid_options = [
    "-a",
    "-A",
    "-b",
    "-B",
    "-c",
    "-d",
    "-D",
    "-f",
    "-F",
    "-p",
    "-P",
    "-r",
    "-s",
    "-S",
    "-w",
]
valid_guns = {
    "assault": (0, "Assault Rifle"),
    "shotgun": (1, "Shotgun"),
    "grenade": (2, "Grenade Launcher"),
    "rocket": (3, "Rocket Launcher"),
    "sniper": (4, "Sniper Rifle"),
    "pistol": (5, "Pistol"),
    "dual": (6, "Dual Pistols"),
    "spray": (7, "Spray Gun"),
    "gatling": (8, "Gatling Gun"),
    "shower": (9, "Shower Gun"),
}

valid_modes = {1: "primary_fire", 2: "secondary_fire"}

other_options = ["--help", "--load-backup", "--write", "--load", "--list"]

# ---------------------------------------------------------


def load_help_files():
    global HELP
    global HELP_C

    with open(ASSETS_PATH + "help.txt") as h:
        HELP = h.read()

    with open(ASSETS_PATH + "help_concise.txt") as hc:
        HELP_C = hc.read()


def load_config():
    global PBS_PATH
    global WATER_GUN_PARAM_PATH
    global DATA_PATH
    global BACKUP_NAME
    global ASSETS_PATH

    with open("config.json") as config:
        config_json = json.load(config)

        PBS_PATH = config_json[0]["pbs_path"]
        WATER_GUN_PARAM_PATH = config_json[0]["water_gun_param_path"]
        BACKUP_NAME = config_json[0]["water_gun_param_backup_name"]
        DATA_PATH = config_json[0]["data_path"]
        ASSETS_PATH = config_json[0]["assets_path"]


def load_address_data():
    """Load the necessary JSON files for searching WaterGunParam.bin"""

    adds_json = None
    offs_json = None

    with open(DATA_PATH + "WaterGunParam_addresses.json") as adds:
        adds_json = json.load(adds)
    with open(DATA_PATH + "WaterGunParam_offsets.json") as offs:
        offs_json = json.load(offs)

    return (adds_json, offs_json)


def assign_value(wgp, addresses, offsets, weapon, level, firing_mode, option, value):
    """Modifies WaterGunParam.bin based with a value based on the option."""

    # Track parameter changes
    before = None
    after = None

    # NOTE: value is a string that is cast based on a matched option
    match option:
        case "-d":
            value = float(value)
            before, after = write_gun_parameter(
                wgp,
                addresses,
                offsets,
                weapon,
                level,
                firing_mode,
                option,
                value,
                "close_damage",
                "<f",
            )
            print_changes("Close damage", before, after, "float")

        case "-D":
            value = float(value)
            before, after = write_gun_parameter(
                wgp,
                addresses,
                offsets,
                weapon,
                level,
                firing_mode,
                option,
                value,
                "far_damage",
                "<f",
            )
            print_changes("Far damage", before, after, "float")

        case "-s":
            value = float(value)
            before, after = write_gun_parameter(
                wgp,
                addresses,
                offsets,
                weapon,
                level,
                firing_mode,
                option,
                value,
                "close_soak",
                "<f",
            )
            print_changes("Close soak", before, after, "float")

        case "-S":
            value = float(value)
            before, after = write_gun_parameter(
                wgp,
                addresses,
                offsets,
                weapon,
                level,
                firing_mode,
                option,
                value,
                "far_soak",
                "<f",
            )
            print_changes("Far soak", before, after, "float")

        case "-r":
            value = float(value)
            before, after = write_gun_parameter(
                wgp,
                addresses,
                offsets,
                weapon,
                level,
                firing_mode,
                option,
                value,
                "fire_rate",
                "<f",
            )
            print_changes("Fire rate", before, after, "float")

        case "-w":
            value = float(value)
            before, after = write_gun_parameter(
                wgp,
                addresses,
                offsets,
                weapon,
                level,
                firing_mode,
                option,
                value,
                "water_usage",
                "<f",
            )
            print_changes("Water usage", before, after, "float")

        case "-a":
            value = float(value)

            # Value must fall within reasonable range (0-1)
            if value > 1.0:
                value = 1.0
            elif value < 0.0:
                value = 0.0

            before, after = write_gun_parameter(
                wgp,
                addresses,
                offsets,
                weapon,
                level,
                firing_mode,
                option,
                value,
                "accuracy",
                "<f",
            )
            print_changes("Accuracy", before, after, "percentage")

        case "-A":
            value = float(value)
            before, after = write_gun_parameter(
                wgp,
                addresses,
                offsets,
                weapon,
                level,
                firing_mode,
                option,
                value,
                "aim_assist_strength",
                "<f",
            )
            print_changes("Aim assist strength", before, after, "float")

        case "-f":
            value = int(value)
            before, after = write_gun_parameter(
                wgp,
                addresses,
                offsets,
                weapon,
                level,
                firing_mode,
                option,
                value,
                "fire_type",
                "<i",
            )
            print_changes("Fire type", before, after, "normal")

        case "-F":
            value = float(value)
            before, after = write_gun_parameter(
                wgp,
                addresses,
                offsets,
                weapon,
                level,
                firing_mode,
                option,
                value,
                "damage_falloff_distance",
                "<f",
            )
            print_changes("Damage falloff distance", before, after, "float")

        case "-b":
            value = int(value)
            before, after = write_gun_parameter(
                wgp,
                addresses,
                offsets,
                weapon,
                level,
                firing_mode,
                option,
                value,
                "burst_size",
                "<i",
            )
            print_changes("Burst size", before, after, "normal")

        case "-B":
            value = float(value)
            before, after = write_gun_parameter(
                wgp,
                addresses,
                offsets,
                weapon,
                level,
                firing_mode,
                option,
                value,
                "burst_delay",
                "<f",
            )
            print_changes("Burst delay", before, after, "float")

        case "-p":
            value = float(value)
            before, after = write_gun_parameter(
                wgp,
                addresses,
                offsets,
                weapon,
                level,
                firing_mode,
                option,
                value,
                "projectile_travel_speed",
                "<f",
            )
            print_changes("Projectile travel speed", before, after, "float")

        case "-P":
            value = float(value)

            if value > sys.float_info.max:
                value = sys.float_info.max

            before, after = write_gun_parameter(
                wgp,
                addresses,
                offsets,
                weapon,
                level,
                firing_mode,
                option,
                value,
                "projectile_travel_distance",
                "<f",
            )
            print_changes("Projectile travel distance", before, after, "float")

        case "-c":
            value = int(value)
            before, after = write_gun_parameter(
                wgp,
                addresses,
                offsets,
                weapon,
                level,
                firing_mode,
                option,
                value,
                "projectile_count",
                "<i",
            )
            print_changes("Projectile count", before, after, "normal")

        case _:
            print("Unknown parameter")


def write_gun_parameter(
    wgp, addresses, offsets, weapon, level, firing_mode, option, value, param, type
):
    parameter_location = 0
    param_level_diff = 0
    pos = 0
    before_modification = 0
    after_modification = 0

    # Preparation
    # - find corrent weapon address with respect to firing mode...
    parameter_location = addresses[valid_guns[weapon][0]]["parameters"][
        valid_modes[firing_mode]
    ]

    # - find correct level...
    param_level_diff = int(offsets[0]["parameter_level_diff"])
    parameter_location += param_level_diff * (level - 1)

    # - find the parameter of interest...
    parameter_location += offsets[2]["parameter_offsets"][param]

    # Write stuff
    # - read current parameter...
    wgp.seek(parameter_location)
    pos = wgp.tell()
    before_modification = wgp.read(4)

    # - write change...
    wgp.seek(parameter_location)
    wgp.write(struct.pack(type, value))

    # - read parameter after change...
    wgp.seek(pos)
    after_modification = wgp.read(4)

    return (
        struct.unpack(type, before_modification)[0],
        struct.unpack(type, after_modification)[0],
    )


def print_changes(param_name, before, after, format_option):
    match format_option:
        case "normal":
            print("{}: {} -> {}".format(param_name, before, after))
        case "float":
            print("{}: {:.1f} -> {:.1f}".format(param_name, before, after))
        case "percentage":
            print(
                "{}: {:.1f}% -> {:.1f}%".format(param_name, before * 100, after * 100)
            )


def exit_with_help():
    print(HELP_C)
    raise SystemExit()


def dupe_bin(name):
    new_bin = PBS_PATH + WATER_GUN_PARAM_PATH + name
    bin = PBS_PATH + WATER_GUN_PARAM_PATH + "WaterGunParam.bin"
    shutil.copy(bin, new_bin)


def load_bin(name):
    new_bin = PBS_PATH + WATER_GUN_PARAM_PATH + name
    bin = PBS_PATH + WATER_GUN_PARAM_PATH + "WaterGunParam.bin"
    shutil.copy(new_bin, bin)


def restore_backup():
    """Replaces WaterGunParam.bin with a backup specified in config.json"""
    backup = PBS_PATH + WATER_GUN_PARAM_PATH + BACKUP_NAME
    bin = PBS_PATH + WATER_GUN_PARAM_PATH + "WaterGunParam.bin"
    shutil.copy(backup, bin)


def parse_other_options(ops):
    match ops[0]:
        case "--help":
            print(HELP)
            return 1
        case "--load-backup":
            restore_backup()
            return 0
        case "--write":
            dupe_bin(ops[1])
            return 0
        case "--load":
            load_bin(ops[1])
            return 0
        case _:
            return 2


# def check_user_option_validity(options):
#    """Verifies that user options can be understood by the script."""
#    pass

# def display_current_values(weapon):
#    """Displays current parameters for a specific weapon."""
#    pass

# def display_header(weapon):
#    """Displays values for a weapon at the header."""
#    pass


# ---------------------------------------------------------

if __name__ == "__main__":

    load_config()
    load_help_files()

    # Check for other options
    if len(sys.argv) > 1 and sys.argv[1] in other_options:
        if parse_other_options(sys.argv[1:]) == 0:
            print("Success")
        raise SystemExit()
    elif len(sys.argv) <= 5:
        exit_with_help()

    addresses_json, offsets_json = load_address_data()

    # Opening the water gun binary
    with open(PBS_PATH + WATER_GUN_PARAM_PATH + "WaterGunParam.bin", "r+b") as wgp:

        # Parsing passed options
        # - essentials
        weapon = sys.argv[1]
        if sys.argv[1] not in list(valid_guns.keys()):
            print('"{}" is not a valid weapon'.format(weapon))
            raise SystemExit()

        level = int(sys.argv[2])
        if level < 1 or level > 10:
            print(
                'Level "{}" is not valid (expected value between 1 to 10)'.format(level)
            )
            raise SystemExit()

        mode = int(sys.argv[3])
        if mode not in list(valid_modes.keys()):
            print('Mode "{}" is not valid (expected value of 1 or 2)'.format(mode))
            raise SystemExit()

        print(
            "Level {} {} ({})".format(
                level, valid_guns[weapon][1], "primary" if mode == 1 else "secondary"
            )
        )

        # - parameter options
        for i in range(4, len(sys.argv[4:]) + 4):
            if sys.argv[i] in valid_options:
                assign_value(
                    wgp,
                    addresses_json,
                    offsets_json,
                    weapon,
                    level,
                    mode,
                    sys.argv[i],
                    sys.argv[i + 1],
                )
