################################################
# configurator.py
# Andrew Woska
# agwoska@bu.edu
################################################
# Configures the data for the FPGA synthesis engine
################################################
# TODO:
# - convert bitstream to json to fpga_adt
# - minimize expression
# - convert data to fpga_adt
# - define partially connected LUTs file
################################################
# methods:
# config()
################################################

import logic_synthesis_engine as lse
import eq_adt as adt
import fpga_adt as fpga
import json

def config(expr: list, nLut: int, tLut: int, cLut='', isBitstream=False):
    # expr: expression(s) to be synthesized
    # nLuts: number of LUTs - number > 0
    # tLut: number of inputs per LUT - 4 or 6
    # cLut: connectivity of LUTs - fully or partially connected
    # isBitstream: boolean to determine if bitstream
    # returns: dictionary of configuration data
    if isBitstream:
        # convert bitstream to json to fpga_adt
        return
    
    # get partially connected LUT file if specified
    lut_data = []
    if cLut != '':
        with open(cLut) as f:
            lut_data = json.load(f)
        # end with
    
    # minimize expression
    eq = []
    for e in expr:
        ex = adt.eq_adt(e)
        lit, neg, ops = lse.parser(e)
        ex.update_literals(lit)
        ex.update_neglist(neg)
        ex.update_ops(ops)
        eq.append(ex)
        
        parts = e.split('+')
        # check if expression fits in LUT based on number of expressions
        if len(parts) > nLut:
            # TODO
            pass
        # check if expression fits in LUT based on number of literals in expressions
        for p in parts:
            if len(p) > tLut:
                # TODO
                pass
        # double check if expression fits in LUT based on number of expressions
        if len(eq) > nLut:
            # TODO
            pass
    # check for more problems?
    # TODO: convert data to fpga_adt
    # send data to FPGA synthesis engine
    return fpga.fpga_adt({})
# end config