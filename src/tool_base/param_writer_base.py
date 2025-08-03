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


# ---------------------------------------------------------


class ParamWriter:

    # Parameters
    # - script name and synopsis
    writer_name: str
    synopsis: str

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

    # - other stuff
    writer_description: str

    # Constructor
    def __init__(self, parsed_config: dict, writer_name: str, synopsis: str):
        self.writer_name = writer_name
        self.synopsis = synopsis
        self.config = parsed_config
        self.special_options = [
            "help",
            "load-backup",
            "load-file",
            "save-file",
            "load-asset",
            "save-asset",
        ]

        try:
            self.load_addresses()
            self.load_offsets()
            self.load_options()
            self.collect_valid_options()
            self.compose_option_description()

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

    def compose_option_description(self):
        # Collection option briefs
        desc: list
        help_desc: list
        formatter = lambda op, brief: f"{op:<15} : {brief}"

        desc = [
            formatter(o, self.offs[0][self.options[0][o]]["brief"])
            for o in self.valid_options
            if o.find("--") == -1
        ]

        # NOTE: consider a less hard coded alternative
        help_desc = [
            formatter("help", "Prints a brief help message"),
            formatter(
                "load-backup", "Overwrites current parameter file with its backup"
            ),
            formatter(
                "save-file",
                "Save current parameters to a new file (parameter file directory)",
            ),
            formatter(
                "load-file",
                "Load current parameters from a file (parameter file directory)",
            ),
            formatter(
                "save-asset", "Save current parameters to a new file (assets directory)"
            ),
            formatter(
                "load-asset", "Load current parameters from a file (assets directory)"
            ),
        ]

        # Update writer description
        self.writer_description = ""
        self.writer_description += (
            f"{self.writer_name}\n\nSYNOPSIS\n{self.synopsis}\n\n"
        )

        self.writer_description += "OPTIONS\n"
        for i in desc:
            self.writer_description += i + "\n"

        self.writer_description += "\nSPECIAL OPTIONS\n"
        for i in help_desc:
            self.writer_description += i + "\n"

    def display_help_message(self):
        print(self.writer_description)

    def get_full_bin_path(self):
        return (
            self.config["pbs_dir"]
            + self.config["param_dir"]
            + self.config["param_filename"]
        )

    def get_full_backup_path(self):
        backup: str

        if self.config["store_backup_in_pbs"]:
            backup = (
                self.config["pbs_dir"]
                + self.config["backup_dir"]
                + self.config["param_backup_filename"]
            )
        else:
            backup = self.config["backup_dir"] + self.config["param_backup_filename"]

        return backup

    def read_backup(self):
        backup = self.get_full_backup_path()
        bin = self.get_full_bin_path()

        try:
            shutil.copy(backup, bin)
        except Exception as e:
            print(f"Backup operation failed ({e})")

    def manage_file(self, filename, operation="", flag=""):
        bin = self.get_full_bin_path()

        if flag == "asset":
            file_path = get_project_root() + self.config["assets_dir"] + filename
        else:
            file_path = self.config["pbs_dir"] + self.config["param_dir"] + filename

        try:
            if operation == "load":
                shutil.copy(file_path, bin)
            elif operation == "save":
                shutil.copy(bin, file_path)

        except Exception as e:
            print(f"Parameter file write failed ({e})")

    def write_float_param(self, param_file, full_addr, value):
        value = float(value)
        param_file.seek(full_addr)
        param_file.write(struct.pack("<f", value))

    def write_int_param(self, param_file, full_addr, value):
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
            self.write_float_param(param_file, full_address, value)

        elif value_type == "int":
            struct_type = "<i"
            self.write_int_param(param_file, full_address, value)

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

    def parse_special_option(self, args, op_index):
        if args[op_index] == "help":
            self.display_help_message()
        elif args[op_index] == "load-backup":
            self.read_backup()
        elif args[op_index] == "load-file":
            self.manage_file(args[op_index + 1], operation="load")
        elif args[op_index] == "save-file":
            self.manage_file(args[op_index + 1], operation="save")
        elif args[op_index] == "load-asset":
            self.manage_file(args[op_index + 1], operation="load", flag="asset")
        elif args[op_index] == "save-asset":
            self.manage_file(args[op_index + 1], operation="save", flag="asset")

    def perform_standard_preliminaries(self, args):
        # Special option parsing
        if len(args) > 1 and args[1] in self.special_options:

            if (
                args[1] == "save-file"
                or args[1] == "load-file"
                or args[1] == "save-asset"
                or args[1] == "load-asset"
            ) and len(args) <= 2:
                self.display_help_message()
                return -1
            else:
                self.parse_special_option(args, 1)
                return 0

        # Normal parsing
        if (
            len(args) < self.config["min_args"]
            or (len(args) - self.config["min_args"]) % 2 != 0
        ):
            self.display_help_message()
            return -1

        return 0
