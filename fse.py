########################################
# FPGA Synthesis Engine
########################################
# Yongning Young Ma
# yma00@bu.edu
# Boston University
# EC551, Fall 2023
########################################
# Citations
# Contains code generated by ChatGPT 4.0 and Github Copilot
# https://stackoverflow.com/questions/5574702/how-do-i-print-to-stderr-in-python  <- eprint
########################################

import json
import fpga_adt as fpga
import eq_adt as eq
import numpy as np
import math
import sys
import itertools


class eq_part_adt(eq.eq_adt):
    def __init__(self, eq, literals, neglist, ops, table, isCircuit):
        super().__init__(eq)
        self.literals = literals
        self.neglist = neglist
        self.ops = ops
        self.table = table
        self.isCircuit = isCircuit
        self.lutPrim = []


def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)


# analyze input equations and determine the order they are routed
# most complex equations are routed first
def analyze_eq(eq_adt: list, constraint="free", fpga_adt: fpga = None):
    # get the number of literals and ops in each equation
    # higher generally means more complex

    if constraint == "free":
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
    elif constraint == "constrained":
        # determine the dependency of each equation

        # first append any eq with no dependency
        output = []
        fpga_outputs = fpga_adt.get_outputs()
        for each in eq_adt:
            oliteral = list(set(each.literals))
            oliteral.sort()
            depdendent = False
            for literal in oliteral:
                if literal in fpga_outputs:
                    depdendent = True
                    break
            if not depdendent:
                output.append(each)
                eq_adt.remove(each)  # so we don't have to iterate through it again

        # then append the rest
        # starting from the ones with least dependency (just 1)
        # to the ones with most dependency

        # create an empty layer list that is the same size of eq_adt
        layer = [0] * len(eq_adt)
        i = 0
        for each in eq_adt:
            oliteral = list(set(each.literals))
            oliteral.sort()
            for literal in oliteral:
                if literal in fpga_outputs:
                    layer[i] += 1
            i += 1

        # sort the equations by dependency
        # the least dependent equations are routed first
        output += [
            x
            for _, x in sorted(
                zip(layer, eq_adt), key=lambda pair: pair[0], reverse=False
            )
        ]

        return output


# partitions the truth table of each eq_adt into
# either 4 or 6 input luts
# input: eq_adt, lut_type, fpga_adt
# output: partitioned_luts, num_luts


def partition_to_lut(eq_adt: eq, lut_type: int, fpga_adt: fpga):
    oliteral = list(
        set(eq_adt.literals)
    )  # Assuming this gives a list of all possible input literals
    oliteral.sort()
    num_literals = len(oliteral)

    lut_inputs = []
    lut_outputs = []
    lut_data = []

    if len(oliteral) < lut_type:
        lut_input_combinations = itertools.combinations(oliteral, len(oliteral))
    else:
        lut_input_combinations = itertools.combinations(oliteral, lut_type)
    for combination in lut_input_combinations:
        filtered_table = {
            k: v
            for k, v in eq_adt.table.items()
            if is_combination_relevant(k, combination, num_literals, oliteral)
        }
        if filtered_table:
            lut_index = len(lut_inputs)  # Index for the next LUT
            lut_inputs.append(list(combination))
            lut_outputs.append(f"LUT_{eq_adt.name}_{lut_index}_Output")
            relevant_minterms = get_relevant_minterms(
                combination, num_literals, oliteral, eq_adt.table
            )
            binary_data = "".join(
                str(eq_adt.table.get(minterm, 0)) for minterm in relevant_minterms
            )
            binary_data = adjust_binary_length(binary_data, lut_type)
            lut_data.append(binary_data)

    # if no muxes are needed, return here
    if len(lut_data) == 1:
        num_luts = 1
        output_lut_name = lut_outputs[0].split("_Output")[0]
        output_var_name = eq_adt.name
        return (
            lut_inputs,
            lut_outputs,
            lut_data,
            num_luts,
            output_lut_name,
            output_var_name,
        )

    # Determining MUX LUTs
    num_normal_luts = len(lut_inputs)
    num_select_lines = math.ceil(math.log2(num_normal_luts))
    num_mux_luts = math.ceil(num_normal_luts / lut_type)

    # Generate MUX LUT configurations
    for i in range(num_mux_luts):
        mux_inputs = [
            lut_outputs[j]
            for j in range(i * lut_type, min((i + 1) * lut_type, num_normal_luts))
        ]
        mux_outputs = f"MUX_{eq_adt.name}_{i}_Output"
        mux_binary_data = generate_mux_data(
            num_select_lines, len(mux_inputs)
        )  # Placeholder, implement the logic based on your MUX design
        lut_inputs.append(mux_inputs)
        lut_outputs.append(mux_outputs)
        lut_data.append(mux_binary_data)

    num_luts = len(lut_outputs)
    output_lut_name = lut_outputs[-1].split("_Output")[0]
    output_var_name = eq_adt.name
    return lut_inputs, lut_outputs, lut_data, num_luts, output_lut_name, output_var_name


def is_combination_relevant(minterm, combination, num_literals, oliteral):
    binary_repr = format(minterm, f"0{num_literals}b")
    return all(binary_repr[oliteral.index(lit)] != "0" for lit in combination)


def get_relevant_minterms(combination, num_literals, oliteral, table):
    relevant_minterms = []
    for minterm in range(2**num_literals):
        if (
            is_combination_relevant(minterm, combination, num_literals, oliteral)
            and minterm in table
        ):
            relevant_minterms.append(minterm)
    return relevant_minterms


def generate_mux_data(num_select_lines, num_inputs):
    binary_data = "MUX_CONFIG_BITS_PLACEHOLDER"
    # for select_combination in range(2**num_select_lines):
    #     # Determine which input is selected by this combination
    #     selected_input = select_combination % num_inputs
    #     # For each combination, only one input is selected
    #     input_state = ["0"] * num_inputs
    #     if selected_input < num_inputs:
    #         input_state[selected_input] = "1"  # Set '1' for the selected input
    #     binary_data += "".join(input_state)

    return binary_data


def adjust_binary_length(binary_data, lut_type):
    # Ensure the binary data length matches 2^lut_type
    required_length = 2**lut_type
    return binary_data.ljust(required_length, "0")  # Pad with '0's if necessary


# LUT routing with no connection constraints
# and can be mapped to any LUT from any inputs
# algorithm:
# partition the truth table of each eq_adt into
# either 4 or 6 input luts and route them
# input list of eqs are sorted based on complexity
def routing_free(eq_adt: list, fpga_adt: fpga):
    sorted_eqs = analyze_eq(eq_adt)  # Analyze and sort equations, placeholder function

    lut_ins = []
    lut_outs = []
    for eq in sorted_eqs:
        # Partition each equation into LUTs
        (
            lut_inputs,
            lut_outputs,
            lut_data,
            num_luts,
            output_lut_name,
            output_var_name,
        ) = partition_to_lut(eq, fpga_adt.get_lut_type(), fpga_adt)

        lut_ins.append(lut_inputs)
        lut_outs.append(output_var_name)

        # Place LUTs on the FPGA
        for i in range(num_luts):
            # Find the next available location on the FPGA

            location = find_and_place(fpga_adt, "free", "base", "lut")
            # populate a LUT object
            luts_on_fpga = fpga_adt.get_luts()

            # find the first empty LUT
            # lut is empty when location = []
            for lut in luts_on_fpga:
                if lut.location == []:
                    lut.name = lut_outputs[i].split("_Output")[0]
                    lut.op = eq
                    lut.location = location
                    lut.data = lut_data[i]
                    update_fpga_layout(fpga_adt, lut)
                    break
    # route wires
    # first route inputs and outputs
    # then route the internal connections

    # update fpga_inputs
    # if a literal does not exist as an output in lut_outs, it is an external input
    external_inputs = []
    for eq in eq_adt:
        for literal in eq.literals:
            if literal not in lut_outs:
                external_inputs.append(literal)
    #
    external_inputs = list(set(external_inputs))
    external_inputs.sort()
    fpga_adt.update_inputs(external_inputs)
    for input in external_inputs:
        # place the input on a free I/O fabric location
        location = find_and_place(fpga_adt, "free", "io", "input")
        update_io_layout(fpga_adt, location, input)

    # place outputs
    for output in fpga_adt.outputs:
        location = find_and_place(fpga_adt, "free", "io", "output")
        update_io_layout(fpga_adt, location, output)

    # no need to make connections as
    # free routing does not have any constraints
    # repr is done at query by the runner
    # # make connections
    # # connect all inputs to the LUTs
    # # and update these connections to fpga_adt.wire
    # for lut in fpga_adt.luts:
    #     lut_index = int(lut.name.split("_")[1])
    #     for inputs in lut_ins[lut_index]:
    #         for input in inputs:
    #             input_location = find_io(fpga_adt, input)
    #             pass


# LUT routing with connection constraints
def routing_constrained(eq_adt: list, fpga_adt: fpga):
    sorted_eqs = analyze_eq(
        eq_adt, "constrained", fpga_adt
    )  # Analyze and sort equations, placeholder function
    lut_ins = []
    lut_outs = []

    output_dict = {}
    place_wires(fpga_adt)
    find_lut_list = sorted_eqs.copy()
    for eq in sorted_eqs:
        # Partition each equation into LUTs
        (
            lut_inputs,
            lut_outputs,
            lut_data,
            num_luts,
            output_lut_name,
            output_var_name,
        ) = partition_to_lut(eq, fpga_adt.get_lut_type(), fpga_adt)

        lut_ins.append(lut_inputs)
        lut_outs.append(output_var_name)

        output_dict[output_var_name] = output_lut_name
        # place wires

        # place LUTs

        # find depdendency of each LUT
        # a LUT that is dependent on other LUTs will be ordered after all the LUTs it is dependent on

        for i in range(num_luts):
            location = find_and_place(
                fpga_adt,
                "constrained",
                "base",
                "lut",
                find_lut_list,
                sorted_eqs,
                output_dict,
            )
            luts_on_fpga = fpga_adt.get_luts()

            for lut in luts_on_fpga:
                if lut.location == []:
                    lut.name = lut_outputs[i].split("_Output")[0]
                    lut.op = eq
                    lut.location = location
                    lut.data = lut_data[i]
                    update_fpga_layout(fpga_adt, lut)
                    break
        find_lut_list.pop(0)


def find_and_place(
    fpga_adt: fpga,
    constraint: str,
    target_layer: str,
    target_type: str,
    remaining_eq: list = None,
    eq_adt=None,
    dependency_dict=None,
):
    layout = fpga_adt.get_layout()
    if constraint == "free":
        if target_layer == "base":
            # get the base layer
            layout = layout[0]
            if target_type == "lut":
                # get the LUT layer
                layout = layout[0]
                # fill vertically first
                for j in range(len(layout[0])):
                    for i in range(len(layout)):
                        if layout[i][j] == "":
                            return [i, j]
            elif target_type == "wire":
                # get the wire layer
                layout = layout[1]
                for i in range(len(layout)):
                    for j in range(len(layout[i])):
                        if layout[i][j] == "":
                            return [i, j]
        elif target_layer == "io":
            layout = layout[0][2]  # the other array is discared
            # no constraint so just place whereever
            for j in range(len(layout[0])):
                for i in range(len(layout)):
                    if layout[i][j] == "":
                        return [i, j]

    elif constraint == "constrained":
        # first check the types of input to this LUT
        # if all the inputs are external, it can be placed more towards the left (start of index)
        # if it is dependent on the output of another LUT, it must be placed behind it
        if target_layer == "base":
            # get the base layer
            layout = layout[0]
            if target_type == "lut":
                # get the LUT layer
                layout = layout[0]
                oliteral = list(set(remaining_eq[0].literals))
                oliteral.sort()
                dependent = {}  # {depdent_var: dependent_var_location}
                out_vars = fpga_adt.get_outputs()
                for literal in oliteral:
                    if literal in out_vars:
                        dependent[literal] = find_lut(
                            fpga_adt, literal, dependency_dict
                        )

                # if the LUT is not dependent on any other LUTs, place it
                # as far left as possible

                if len(dependent) == 0:
                    # fill vertically first
                    for j in range(len(layout[0])):
                        for i in range(len(layout)):
                            if layout[i][j] == "":
                                return [i, j]

                # if the LUT is dependent on other LUTs, place it on the first
                # column that is to the rightmost of all the dependent LUTs

                else:
                    # find the rightmost column
                    rightmost = 0
                    for key in dependent:
                        if dependent[key][1] > rightmost:
                            rightmost = dependent[key][1]
                    # fill vertically first
                    for j in range(rightmost + 1, len(layout[0])):
                        for i in range(len(layout)):
                            if layout[i][j] == "":
                                return [i, j]

    return [0, 0]  # Return location as [x, y]


def update_fpga_layout(fpga_adt, lut):
    layout = fpga_adt.get_layout()
    lut_layer = layout[0][0]
    lut_layer[lut.location[0]][lut.location[1]] = lut.name
    layout[0][0] = lut_layer
    # fpga_adt.update_layout(layout)


def update_io_layout(fpga_adt, loc, name):
    layout = fpga_adt.get_layout()
    io_layer = layout[0][2]
    io_layer[loc[0]][loc[1]] = name
    layout[0][2] = io_layer
    # fpga_adt.update_layout(layout)


def find_lut(fpga_adt, lut_name, dependency_dict):
    layout = fpga_adt.get_layout()
    lut_layer = layout[0][0]
    for j in range(len(lut_layer[0])):
        for i in range(len(lut_layer)):
            target = dependency_dict[lut_name]
            if lut_layer[i][j] == target:
                return [i, j]

    return [-1, -1]


def find_io(fpga_adt, name):
    layout = fpga_adt.get_layout()
    io_layer = layout[0][2]
    for i in range(len(io_layer)):
        for j in range(len(io_layer[i])):
            if io_layer[i][j] == name:
                return [i, j]
    return [0, 0]


# place wires on base layer every other column
# (on odd columns)
def place_wires(fpga_adt):
    layout = fpga_adt.get_layout()
    wire_layer = layout[0][0]
    for j in range(len(wire_layer[0])):
        if j % 2 == 0:
            for i in range(len(wire_layer)):
                wire_layer[i][j] = "rud"
        else:
            for i in range(len(wire_layer)):
                if i % 2 == 0:
                    wire_layer[i][j] = "rud"


#
def fse_runner(fpga_adt: fpga):
    pass


def show_lut_assignments(show_all: bool):
    pass


def show_connections():
    pass


def show_i_extern():
    pass


def show_o_extern():
    pass


def load_bitstream(bitstream):
    pass


def write_bitstream(fpga_adt: fpga):
    pass


def show_utilization():
    pass