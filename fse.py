########################################
# FPGA Synthesis Engine
########################################
# Yongning Young Ma
# yma00@bu.edu
# Boston University
# EC551, Fall 2023
########################################
# Citations
# https://stackoverflow.com/questions/5574702/how-do-i-print-to-stderr-in-python  <- eprint
########################################

import json
import fpga_adt as fpga
import eq_adt as eq
import numpy as np
import sys


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


# analyze input equations and determine the order they are routed
# most complex equations are routed first
def analyze_eq(eq_adt: list):
    # get the number of literals and ops in each equation
    # higher generally means more complex
    complexity = []
    for each in eq_adt:
        complexity.append(len(each.literals) + len(each.ops))

    # sort the equations by complexity
    # the most complex equations are routed first

    # sort the equations by complexity
    output = [
        x
        for _, x in sorted(
            zip(complexity, eq_adt), key=lambda pair: pair[0], reverse=True
        )
    ]
    return output


# partitions the truth table of each eq_adt into
# either 4 or 6 input luts
# input: eq_adt, lut_type, fpga_adt
# output: partitioned_luts, num_luts
def partition_to_lut(eq_adt: eq, lut_type: int, fpga_adt: fpga):
    # lut_type = 4 or 6
    # 4 input lut: 4 input, 1 output
    # 6 input lut: 6 input, 1 output

    # get the truth table of the eq_adt

    oliteral = []  # ordered literals
    for i in eq_adt.literals:
        if i not in oliteral:
            oliteral.append(i)

    # if the lut type has enough inputs for the truth table
    # then do not partition
    if lut_type == 4 and oliteral <= 4:
        return eq_adt, 1
    elif lut_type == 6 and oliteral <= 6:
        return eq_adt, 1

    table = eq_adt.table

    # partition the truth table
    if lut_type == 4:
        num_luts = np.ceil(len(oliteral) / 4)  # full luts + partial lut
        # if more luts are needed than available
        if num_luts > len(fpga_adt.get_luts()):
            eprint("Error: not enough LUTs available in current layout")
            return None, num_luts - len(fpga_adt.get_luts())

        # partition the truth table

    elif lut_type == 6:
        num_luts = np.ceil(len(oliteral) / 6)
        # if more luts are needed than available
        if num_luts > len(fpga_adt.get_luts()):
            eprint("Error: not enough LUTs available in current layout")
            return None, num_luts - len(fpga_adt.get_luts())
        # partition the truth table

    else:
        eprint(
            "Error: LUT type not supported, supported types are 4 inputs and 6 inputs"
        )
        return None, None


# LUT routing with no connection constraints
# and can be mapped to any LUT from any inputs
# algorithm:
# partition the truth table of each eq_adt into
# either 4 or 6 input luts and route them
# input list of eqs are sorted based on complexity
def routing_free(eq_adt: list, fpga_adt: fpga):
    sorted = analyze_eq(eq_adt)

    # partition eq into luts
    for each in sorted:
        partition_to_lut(each, 4, fpga_adt)

    pass


# LUT routing with connection constraints
def routing_constrained(eq_adt: list):
    sorted = analyze_eq(eq_adt)
    pass


#
def fse(fpga_adt: fpga):
    pass
