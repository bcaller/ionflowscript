# Copyright Ben Caller 2016

import argparse

from ionflowscript.functions import load_functions
from ionflowscript.filenames import SCRIPT_PREFIX, PROCEDURE_PREFIX
from ionflowscript.proc import print_script, print_proc


def main():
    print("IonFlowScript by Ben Caller")
    parser = argparse.ArgumentParser(description="Read an Ion Torrent flow script or procedure",
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("dir", help="Directory containing script, function and procedure files")
    parser.add_argument("script", help="Name of script or procedure to process "
                                       "(with or without the .txt, e.g. Procedure_Init1)")
    args = parser.parse_args()
    func_dict, cmd_opt_dict = load_functions(args.dir)
    if args.script.startswith(SCRIPT_PREFIX):
        print_script(args.dir, args.script, func_dict, cmd_opt_dict)
    elif args.script.startswith(PROCEDURE_PREFIX):
        print_proc(args.dir, args.script, func_dict, cmd_opt_dict)

if __name__ == '__main__':
    main()