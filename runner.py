################################################
# runner.py
# Andrew Woska
# agwoska@bu.edu
################################################
# Runs the data for the FPGA synthesis engine
################################################
# commands:
# -t: test mode
# -b: bitstream mode
# -f: file mode
# -h: help
################################################
# inputs:
# -nLut: number of LUTs
# -tLut: number of inputs per LUT
# -cLut: connectivity of LUTs (optional)
################################################
# methods:
# main()
################################################

import os
import sys
import configurator as config
import logic_synthesis_engine as lse
import fse
import eq_adt as logic
import fpga_adt as fpga
import tester
import json


def print_help():
    print("Usage: python3 runner.py <mode> <input>")
    print("Modes:")
    print("\t-t: test mode")
    print("\t-b: bitstream mode")
    print("\t-f: file mode")
    print("Inputs for -f:")
    print("\tfile: input equations file")
    print("\tnLut: int > 0")
    print("\ttLut: int 4 or 6")
    print("\tcLut: input file (optional)")


# end print_help


def tests(test):
    if test == "lse":
        tester.lse_tester()
    elif test == "conf":
        tester.config_tester()
    elif test == "fse":
        tester.fse_tester()
    else:
        print("Error: invalid test")
        exit(7)


# end tests


def bitstream(bs_file):
    # check if bs_file exists
    if not os.path.isfile(bs_file):
        return 2
    config = fpga.fpga_adt.load_bitstream(bs_file)
    runner(config)
    return 0


# end bitstream


def get_fpga(eq_file, conn_file, nLut, tLut):
    # check if eq_file exists
    if not os.path.isfile(eq_file):
        return 2
    # check if conn_file exists
    if conn_file != "" and not os.path.isfile(conn_file):
        return 3
    # check if tLut is valid
    if tLut != 4 and tLut != 6:
        return 5
    # check if nLut is valid
    if nLut < 1:
        return 6
    # open eq_file
    with open(eq_file) as f:
        eqs = f.readlines()
    f.close()
    # remove whitespace
    eqs = [x.strip() for x in eqs]

    # TODO: check if eq_file is valid (assuming it is for now)

    # create data
    ret, data = config.config(eqs, nLut, tLut, conn_file)

    # TODO: all detection and generation caused by config

    # check if data is valid
    # TODO: use correct return codes
    if ret != 0:
        # print("panic")
        return 9

    eqts = data.eqs

    for each in eqts:
        (
            lut_inputs,
            lut_outputs,
            lut_data,
            num_luts,
            output_lut_name,
            output_var_name,
        ) = fse.partition_to_lut(each, data.get_lut_type(), data)

    if data.constrained:
        routed = fse.routing_constrained(eqts, data)
    elif not data.constrained:
        routed = fse.routing_free(eqts, data)
    else:
        return 9

    runner(data)
    return 0


# end get_fpga


def get_user_input():
    # get user input
    print("Your input:")
    user_input = input()
    return user_input


# end get_user_input


def runner(data: fpga.fpga_adt):
    while True:
        input = get_user_input()

        if input == "exit":
            break
        elif input == "f":
            fse.show_lut_assignments(data, True)
        elif input[0] == "f" and input[1] == " ":
            a = input.split(" ")
            a.pop(0)
            fse.show_lut_assignments(data, False, a)
        elif input == "c":
            fse.show_connections(data)
        elif input == "i":
            fse.show_i_extern(data)
        elif input == "o":
            fse.show_o_extern(data)
        elif input == "b":
            fse.write_bitstream(data)
        elif input == "r":
            fse.show_utilization(data)
        else:
            print("Error: invalid input")


# end get_outs


def main():
    if len(sys.argv) < 2 or len(sys.argv) > 8:
        print_help()
        exit(1)
    if sys.argv[1] == "-t":
        if len(sys.argv) != 3:
            print_help()
            exit(4)
        tests(sys.argv[2])
        exit(0)
    if sys.argv[1] == "-b":
        if len(sys.argv) != 3:
            print_help()
            exit(5)
        bitstream(sys.argv[2])
        exit(0)
    if sys.argv[1] == "-h":
        print_help()
        exit(0)
    # check if -f is specified anywhere
    if sys.argv[1] == "-f":
        # if cLut is specified, then it is the 6th argument
        args = sys.argv
        if len(sys.argv) == 6:
            cLut = sys.argv[5]
            conn_file = cLut
        else:
            cLut = ""
            conn_file = ""
        # get inputs
        eq_file = sys.argv[2]
        nLut = int(sys.argv[3])
        tLut = int(sys.argv[4])
        # get file
        # run fpga synthesis engine
        foo = get_fpga(eq_file, conn_file, nLut, tLut)
        # check return code
        match foo:
            case 0:  # success
                exit(0)
            case 1:  # not enough LUTs
                print("Error:", foo)
            case 2:  # eq file not found
                print("Error:", foo)
            case 3:  # conn file not found
                print("Error:", foo)
            case 4:  # invalid cLut
                print("Error:", foo)
            case 5:  # invalid tLut
                print("Error:", foo)
            case 6:  # invalid nLut
                print("Error:", foo)
            case 7:  # invalid eq file
                print("Error:", foo)
            case 9:  # undefined error
                print("Error:", foo)
        exit(10 + foo)
    else:
        print_help()
        exit(1)


# end main

if __name__ == "__main__":
    main()
