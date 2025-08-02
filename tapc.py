###########################
##                       ##
##        tapc.py        ##
##                       ##
###########################

import sys
import shutil
import struct
import json
from typing import cast

PBS_PATH = ""
WATER_TANK_PARAM_PATH = ""
BACKUP_NAME = ""
DATA_PATH = ""
ASSETS_PATH = ""

HELP = ""
HELP_C = ""

# ---------------------------------------------------------

def load_config():
    global PBS_PATH
    global WATER_TANK_PARAM_PATH
    global DATA_PATH
    global BACKUP_NAME
    global ASSETS_PATH

    with open("config.json") as config:
        config_json = json.load(config)

        PBS_PATH = config_json[0]["pbs_path"]
        WATER_TANK_PARAM_PATH = config_json[0]["water_tank_param_path"]
        BACKUP_NAME = config_json[0]["water_tank_param_backup_name"]
        DATA_PATH = config_json[0]["data_path"]
        ASSETS_PATH = config_json[0]["assets_path"]

def load_water_tank_data():
    water_tank_data = []

    with open(DATA_PATH + "WaterTankParam_addresses.json") as addrs:
        water_tank_data.append(json.load(addrs))

    with open(DATA_PATH + "WaterTankParam_offsets.json") as offs:
        water_tank_data.append(json.load(offs))

    return (water_tank_data[0], water_tank_data[1])

def collect_valid_options(offsets):
    valid_options = {}

    for i in offsets:
        for j in i:
            valid_options[i[j]["option"]] = j

    return valid_options

def change_water_tank_parameters(wtp, addresses, offsets, weapon, option, value, valid_options):
    if weapon not in addresses[0]:
        return 1

    if option not in list(valid_options.keys()):
        return 1

    target = offsets[0][valid_options[option]]

    match target['type']:
        case '<f':
            value = float(value)
        case '<i':
            value = int(value)

    wtp.seek(addresses[0][weapon] + target['offset'])
    wtp.write(struct.pack(target['type'], value))

    return 0

# ---------------------------------------------------------

if __name__ == '__main__':
    load_config()
    addresses, offsets = load_water_tank_data()
    valid_options = collect_valid_options(offsets)

    if len(sys.argv) < 4 and len(sys.argv) % 2 == 0:
        print('tapc.py weapon [option value]...')
        raise SystemExit()

    with open(PBS_PATH + WATER_TANK_PARAM_PATH + "WaterTankParam.bin", "r+b") as wtp:

        for i in range(2, len(sys.argv)-1, 2):
            print(change_water_tank_parameters(wtp, addresses, offsets, sys.argv[1], sys.argv[i], sys.argv[i+1], valid_options))
