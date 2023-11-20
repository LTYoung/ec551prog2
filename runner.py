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
    if test == 'lse':
        tester.lse_tester()
    elif test == 'conf':
        tester.config_tester()
    elif test == 'fse':
        tester.fse_tester()
    else:
        print("Error: invalid test")
        exit(7)
# end tests


def bitstream(bs_file):
    # check if bs_file exists
    if not os.path.isfile(bs_file):
        return 2
    ret, data = config.config('foo', -1, -1, '', bs_file)
    # TODO: all detection and generation caused by config
    if ret == -1: # WIP so currently always returns -1
        return 9
    return 0
# end bitstream


def get_fpga(eq_file, conn_file, nLut, tLut):
    # check if eq_file exists
    if not os.path.isfile(eq_file):
        return 2
    # check if conn_file exists
    if conn_file != '' and not os.path.isfile(conn_file):
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

    # TODO: check if eq_file is valid

    # TODO: check if conn_file is valid

    # create data
    ret, data = config.config(eqs, nLut, tLut, conn_file)

    # TODO: all detection and generation caused by config

    # check if data is valid
    # TODO: use correct return codes
    if ret != 0:
        print("panic")
        return 9

    # generate report based on output
    # check LUT usage and report

    # fse.show_lut_assignmnets(False)
    # fse.show_connections()
    # fse.show_i_extern()
    # fse.show_o_extern()
    # fse.write_bitstream(data)
    # fse.show_utilization()


    return 0
# end get_fpga



def main():
    if len(sys.argv) < 2 or len(sys.argv) > 8:
        print_help()
        exit(1)
    if sys.argv[1] == '-t':
        if len(sys.argv) != 3:
            print_help()
            exit(4)
        tests(sys.argv[2])
        exit(0)
    if sys.argv[1] == '-b':
        if len(sys.argv) != 3:
            print_help()
            exit(5)
        bitstream(sys.argv[2])
        exit(0)
    if sys.argv[1] == '-h':
        print_help()
        exit(0)
    # check if -f is specified anywhere
    if sys.argv[1] == '-f':
        # if cLut is specified, then it is the 6th argument
        if len(sys.argv) == 8:
            cLut = sys.argv[7]
        else:
            cLut = ''
        # get inputs
        eq_file = sys.argv[2]
        nLut = int(sys.argv[3])
        tLut = int(sys.argv[4])
        # get file
        if len(sys.argv) == 7:
            conn_file = sys.argv[5]
        else:
            conn_file = ''
        # run fpga synthesis engine
        foo = get_fpga(eq_file, conn_file, nLut, tLut)
        # check return code
        match foo:
            case 0: # success
                exit(0)
            case 1: # not enough LUTs
                print("Error:", foo)
            case 2: # eq file not found
                print("Error:", foo)
            case 3: # conn file not found
                print("Error:", foo)
            case 4: # invalid cLut
                print("Error:", foo)
            case 5: # invalid tLut
                print("Error:", foo)
            case 6: # invalid nLut
                print("Error:", foo)
            case 7: # invalid eq file
                print("Error:", foo)
            case 9: # undefined error
                print("Error:", foo)
        exit(10+foo)
    else:
        print_help()
        exit(1)
# end main

if __name__ == "__main__":
    main()
