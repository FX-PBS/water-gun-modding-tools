###########################
##                       ##
##        wepc.py        ##
##                       ##
###########################

import sys

from tool_base import get_project_root
from tool_base import ParamWriter, parse_config

# ---------------------------------------------------------


class GunParamWriter(ParamWriter):

    def parse_arguments(self, args):
        if self.perform_standard_preliminaries(args) != 0:
            return -100

        try:
            with open(
                self.config["pbs_dir"]
                + self.config["param_dir"]
                + self.config["param_filename"],
                "r+b",
            ) as param_file:
                for i in range(len(args)):
                    if args[i] in self.valid_options:
                        param_name = self.offs[0][self.options[0][args[i]]][
                            "param_name"
                        ]
                        full_address = (
                            self.addrs[0][f"{args[1]}_{args[3]}"]
                            + self.offs[0][self.options[0][args[i]]]["offset"]
                            + self.get_level_difference(int(args[2]))
                        )
                        value = args[i + 1]
                        value_type = self.offs[0][self.options[0][args[i]]]["type"]
                        value_size = 4  # NOTE: temporarily hard coded

                        self.write_changes(
                            param_file,
                            param_name,
                            full_address,
                            value,
                            value_type,
                            value_size,
                        )

                return 0

        except Exception as e:
            print(f"Something went wrong during script execution ({e})")
            return -101

    def get_level_difference(self, level):
        if level < 1:
            level = 1

        if level > 10:
            level = 10

        return self.offs[1]["param_level_diff"] * (level - 1)


# ---------------------------------------------------------

if __name__ == "__main__":
    writer = GunParamWriter(
        parse_config(get_project_root() + "config.json", "gun"),
        "Weapon parameter changer",
        "wepc.py weapon level firing_mode [option value]...\nwepc.py special_option [value]",
    )

    writer_exit_code: int

    if writer.init_is_successful():
        writer_exit_code = writer.parse_arguments(sys.argv)
