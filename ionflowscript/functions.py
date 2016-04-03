# Copyright Ben Caller 2016

from os.path import join

import re

from ionflowscript.filenames import *


class Function:
    def __init__(self, line):
        parts = line.split('\t')
        self.id = int(parts[0])
        self.valves = [int(v) for v in parts[1].split(',')]
        self.name = parts[2].rstrip('\n')
        self.alt = None

    def __str__(self):
        return self.name + " (" + ', '.join(str(v) for v in self.valves) + ')'


def load_functions(dir):
    function_dict = {-1: Function("-1\t-1\tNEXT NUCLEOTIDE")}
    cmd_opt_dict = {0: "Default"}
    user_func_regex = re.compile(r"^(\d+) \"([^\"]+)\"(?:\s*#\s*)?(.+)?")
    cmd_regex = re.compile(r"^CMD: ADVOPT (\d+) (.+)")
    with open(join(dir, FUNCTIONS + EXT), 'r') as f:
        for line in f:
            if line[0] != '#':
                func = Function(line)
                function_dict[func.id] = func

    with open(join(dir, USER_FUNCTIONS + EXT), 'r') as f:
        for line in f:
            if line[0] != '#':
                line = line.rstrip('\n')
                user_func_match = user_func_regex.match(line)
                if user_func_match is not None:
                    _id = int(user_func_match.group(1))
                    function_dict[_id].alt = user_func_match.group(2)
                    if user_func_match.group(3):
                        function_dict[_id].name += user_func_match.group(3)
                else:
                    cmd_match = cmd_regex.match(line)
                    if cmd_match is not None:
                        cmd_opt_dict[int(cmd_match.group(1))] = cmd_match.group(2)

    return function_dict, cmd_opt_dict
