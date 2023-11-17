########################################
# FPGA Synthesis Engine
########################################
# Yongning Young Ma
# yma00@bu.edu
# Boston University
# EC551, Fall 2023
########################################

import json
import fpga_adt as fpga
import eq_adt as eq


# analyze input equations and determine the order they are routed
# most complex equations are routed first
def analyze_eq(eq_adt: list):
    # get the number of literals and ops in each equation
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
# output: a list of eq_adt with each eq_adt
# containing a partitioned truth table
def partition_to_lut(eq_adt: eq, lut_type: int):
    # lut_type = 4 or 6
    # 4 input lut: 4 input, 1 output
    # 6 input lut: 6 input, 1 output

    # get the truth table of the eq_adt
    table = eq_adt.table
    oliteral = []  # ordered literals
    for i in eq_adt.literals:
        if i not in oliteral:
            oliteral.append(i)

    # if the lut type has enough inputs for the truth table
    # then do not partition
    if lut_type == 4 and oliteral <= 4:
        return eq_adt
    elif lut_type == 6 and oliteral <= 6:
        return eq_adt
    if lut_type == 4:
        pass
    elif lut_type == 6:
        pass
    else:
        print("Error: lut type not supported")
        return None


# LUT routing with no connection constraints
# and can be mapped to any LUT from any inputs
# algorithm:
# partition the truth table of each eq_adt into
# either 4 or 6 input luts and route them
# input list of eqs are sorted based on complexity
def routing_free(eq_adt: list):
    sorted = analyze_eq(eq_adt)

    pass


# LUT routing with connection constraints
def routing_constrained(eq_adt: list):
    sorted = analyze_eq(eq_adt)
    pass


#
