########################################
##                                    ##
##        param_writer_base.py        ##
##        (tool_base)                 ##
##                                    ##
########################################

import shutil
import struct
import json

from .basic import get_project_root

# ---------------------------------------------------------


def parse_config(config_path, filter):
    # Ensure filter is valid
    valid_filters = ["gun", "tank"]

    if filter not in valid_filters:
        return None

    with open(config_path) as config_file:
        raw_config = json.load(config_file)

        # Prepare to filter config
        parsed_config = {"filter": filter}

        # - load standard directories
        parsed_config["pbs_dir"] = raw_config[0]["pbs_dir"]
        parsed_config["param_dir"] = raw_config[0]["param_dir"]
        parsed_config["backup_dir"] = raw_config[0]["backup_dir"]
        parsed_config["data_dir"] = raw_config[0]["data_dir"]
        parsed_config["assets_dir"] = raw_config[0]["assets_dir"]

        # - load parameters of interest
        parsed_config["param_filename"] = raw_config[1][f"param_{filter}_filename"]
        parsed_config["param_backup_filename"] = raw_config[1][
            f"param_{filter}_backup_filename"
        ]
        parsed_config["data_addrs_filename"] = raw_config[1][
            f"data_{filter}_addresses_filename"
        ]
        parsed_config["data_offs_filename"] = raw_config[1][
            f"data_{filter}_offsets_filename"
        ]
        parsed_config["data_options_filename"] = raw_config[1][
            f"data_{filter}_options_filename"
        ]

        parsed_config["min_args"] = raw_config[2][f"{filter}_min_args"]
        parsed_config["store_backup_in_pbs"] = raw_config[2]["store_backup_in_pbs"]

        return parsed_config


class ParamWriter:

    # Parameters
    # - parsed config dictionary
    config: dict

    # - extracted JSON data
    addrs: dict
    offs: dict
    options: dict

    # - parsed JSON data for options relevant to script
    valid_options: list

    # - initialisation flag updated at constructor
    init_successful: bool

    # Constructor
    def __init__(self, parsed_config: dict):
        self.config = parsed_config
        self.universal_options = ["--help", "--load_backup"]

        try:
            self.load_addresses()
            self.load_offsets()
            self.load_options()
            self.compose_help_string()
            self.collect_valid_options()

            self.init_successful = 0

        except Exception as e:
            print(f"Initialisation failure ({e})")
            self.init_successful = -1

    def init_is_successful(self):
        return self.init_successful == 0

    def load_addresses(self):
        with open(
            get_project_root()
            + self.config["data_dir"]
            + self.config["data_addrs_filename"]
        ) as adds:
            self.addrs = json.load(adds)

    def load_offsets(self):
        with open(
            get_project_root()
            + self.config["data_dir"]
            + self.config["data_offs_filename"]
        ) as offs:
            self.offs = json.load(offs)

    def load_options(self):
        with open(
            get_project_root()
            + self.config["data_dir"]
            + self.config["data_options_filename"]
        ) as ops:
            self.options = json.load(ops)

    def collect_valid_options(self):
        self.valid_options = list(self.options[0].keys())

    def parse_arguments(self, args):
        """(To be implemented by the inheriting class)"""
        pass

    def compose_help_string(self):
        pass

    def display_help_message(self):
        pass

    def load_backup(self):
        backup: str

        if self.config["store_backup_in_pbs"]:
            backup = (
                self.config["pbs_dir"]
                + self.config["backup_dir"]
                + self.config["param_backup_filename"]
            )
        else:
            backup = self.config["backup_dir"] + self.config["param_backup_filename"]

        bin = (
            self.config["pbs_dir"]
            + self.config["param_dir"]
            + self.config["param_filename"]
        )
        shutil.copy(backup, bin)

    def write_float(self, param_file, full_addr, value):
        value = float(value)
        param_file.seek(full_addr)
        param_file.write(struct.pack("<f", value))

    def write_int(self, param_file, full_addr, value):
        value = int(value)
        param_file.seek(full_addr)
        param_file.write(struct.pack("<i", value))

    def write_changes(
        self, param_file, param_name, full_address, value, value_type, value_size
    ):
        struct_type: str

        # Record value before change
        param_file.seek(full_address)
        before = param_file.read(value_size)

        if value_type == "float":
            struct_type = "<f"
            self.write_float(param_file, full_address, value)

        elif value_type == "int":
            struct_type = "<i"
            self.write_int(param_file, full_address, value)

        # Record value after change
        param_file.seek(full_address)
        after = param_file.read(value_size)

        # Output changes to the terminal
        self.document_changes(
            param_name,
            struct.unpack(struct_type, before)[0],
            struct.unpack(struct_type, after)[0],
            value_type,
        )

    def document_changes(self, param_name, before, after, value_type):
        if value_type == "float":
            print(f"{param_name}: {before:.2f} -> {after:.2f}")
        elif value_type == "int":
            print(f"{param_name}: {before} -> {after}")
