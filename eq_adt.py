################################################
# eq_adt.py
# Yongning Young Ma
# yma00@bu.edu
################################################
# Contains the class defination of the
# equation adt used by the SE
###############################################
# ADT attributes:
#   eq: string of the input equation, provide at init
#   literals: list of literals in the equation, updated by parser
#   neglist: list of negations in the equation, updated by parser
#   ops: list of operators in the equation, updated by parser
################################################
# methods:
# parser(eq) -> void
# synth_engine() -> void
################################################
# import numpy as np
# import matplotlib.pyplot as plt
import quine_mccluskey as qm


class eq_adt:
    def __init__(self, eq):
        self.eq = eq
        self.literals = []
        self.neglist = []
        self.ops = []
        self.table = {}
        self.isCircuit = False

    # update literals method
    def update_literals(self, lit):
        # unpack lit and update literals
        for i in range(0, len(lit)):
            self.literals.append(lit[i])

    # update neglist method
    def update_neglist(self, neg):
        # unpack neg and update neglist
        for i in range(0, len(neg)):
            self.neglist.append(neg[i])

    # update ops method
    def update_ops(self, op):
        # unpack op and update ops
        for i in range(0, len(op)):
            self.ops.append(op[i])

    # save truth table
    def update_table(self, table):
        self.table = table

    def update_isCircuit(self):
        self.isCircuit = True

    def isCircuit(self):
        return self.isCircuit

    # get_literals()
    def get_literals(self):
        return self.literals

    # get_neglist()
    def get_neglist(self):
        return self.neglist

    # get_ops()
    def get_ops(self):
        return self.ops

    # get_table()
    def get_table(self):
        return self.table

    def draw_tt(self, term):
        print("---------------")
        print("Truth Table for: " + self.eq + ":")
        print("---------------")
        # print truth table in a nice format

        header = " | ".join(term + ["Output"])
        print(header)
        print("-" * len(header))

        for minterm, result in sorted(self.table.items(), key=lambda x: x[0]):
            binary_minterm = format(int(minterm), f"0{len(term)}b")
            bits = [bit for bit in binary_minterm]
            row = " | ".join(bits + [str(result)])
            print(row)

        return ""

    # draw the kmap representation based on solved truth table

    def print_kmap(self):
        unique_literals = sorted(set(self.literals))

        num_vars = len(unique_literals)
        if num_vars > 4:
            print("This method supports up to four variables only.")
            return

        # Define the header and row format based on the number of variables
        headers = {
            2: ["00", "01", "11", "10"],
            3: ["00", "01", "11", "10"],
            4: ["00", "01", "11", "10"],
        }
        rows = {2: ["0", "1"], 3: ["0", "1"], 4: ["00", "01", "11", "10"]}

        # Print header
        header = "   " + " ".join(headers[num_vars])
        print(header)
        print("  " + "-" * len(header))

        # Print rows
        for i, row_label in enumerate(rows[num_vars]):
            row_data = [
                str(self.table.get(int(f"{row_label}{col_label}", 2), "-"))
                for col_label in headers[num_vars]
            ]
            print(f"{row_label} | {' '.join(row_data)}")
