# Copyright Ben Caller 2016

import re

from ionflowscript.filenames import SCRIPT_PREFIX, EXT
import os


def advanced_hex(str):
    return len("{0:b}".format(int(str, 16))) - 1


def print_script(directory, name, func_dict, cmd_opt_dict, error_messages=None, tabs=0):
    t_counter = 0.0
    loop_start_time = 0.0
    output = lambda x: print('\t' * tabs + x)
    with open(os.path.join(directory, name + EXT), 'r') as f:
        for line in f:
            line = line.rstrip('\n')
            if len(line) == 0:
                pass
            elif line[0] == '#':
                comment = line.rstrip('\t')
                if len(comment) > 2:
                    output(comment)
            elif len(line) > 2:
                if line.startswith("LOOP"):
                    # assuming no nesting
                    if line.startswith("LOOPSTART"):
                        loop_start_time = t_counter
                        output(line.rstrip('\t'))
                        tabs += 1
                    else:
                        parts = line.split('\t')
                        times = int(parts[2]) - int(float(parts[1]))
                        delta_t = t_counter - loop_start_time
                        t_counter = loop_start_time + delta_t * times
                        tabs -= 1
                        output('LOOPEND x' + str(times))
                elif line.startswith("CMD:"):
                    output(line)
                elif line.startswith("ADV END"):
                    tabs -= 1
                    output(line)
                elif line.startswith("ADV START"):
                    adv_opt = re.match(r"ADV START Mask:0x([A-F0-9]+) Val:0x([A-F0-9]+)", line)
                    if adv_opt is not None:
                        opt_value = advanced_hex(adv_opt.group(2))
                        if opt_value in cmd_opt_dict:
                            opt_value = cmd_opt_dict[opt_value]
                        output("{}: opt {} is {}".format(line.rstrip('\t'),
                                                         advanced_hex(adv_opt.group(1)), opt_value))
                    else:
                        output(line)
                    tabs += 1
                else:
                    parts = line.split('\t', maxsplit=3)
                    func_id = int(parts[2])
                    end = parts[3].rstrip('\t') if len(parts) == 4 else ''
                    if func_id == -1 and len(parts) == 4 and end.endswith('-'):
                        func_id = find_user_function(func_dict, end + 'C').id
                        end += 'NUCLEOTIDE (e.g. C)'
                    dur = float(parts[1])
                    duration_str = 'for {}'.format(dur) if dur != -1 else 'forever'
                    if parts[0][0] == '+':
                        start = float(parts[0]) + t_counter
                        if func_id == 0 and dur == 0.0:
                            output("{:.3f}+: ? {}".format(start, end))
                        else:
                            output("{:.3f}+: {} {} {}".format(start, func_dict[func_id], duration_str, end))
                    elif parts[0] == '*':
                        output("{:.3f}*: {} {} {}".format(t_counter, func_dict[func_id], duration_str, end))
                        if float(parts[1]) != -1:
                            t_counter += float(parts[1])
                    else:
                        output("{}: {} {} {}".format(parts[0], func_dict[func_id], duration_str, end))

                    if error_messages and len(error_messages) and len(parts) == 4 and 'P =' in parts[3]:
                        output("\tELSE " + error_messages.pop(0))
        output('{:.3f}: END'.format(t_counter))


def print_proc(directory, name, func_dict, cmd_opt_dict):
    with open(os.path.join(directory, name + EXT), 'r') as f:
        for line in f:
            line = line.rstrip('\n')
            if line[0] == '#':
                comment = line.rstrip('\t')
                if len(comment) > 2:
                    print(comment)
            elif len(line) > 3:
                parts = line.split('\t')
                if len(parts[0]) > 3:
                    print(parts[0])  # Text
                if len(parts) > 2 and parts[2].startswith(SCRIPT_PREFIX):
                    print_script(directory, parts[2], func_dict, cmd_opt_dict,
                                 error_messages=parts[3].split(';') if len(parts) > 3 else None,
                                 tabs=1)  # Run Script
                elif len(parts) > 3 and len(parts[3]) > 3:
                    print(parts[3])
                    if parts[3].startswith("START:"):
                        user_function = parts[3].split(':')[1]  # START:UserFunction
                        print(str(find_user_function(func_dict, user_function)))


def find_user_function(func_dict, user_function_name):
    return next(func for func in func_dict.values() if func.alt == user_function_name)