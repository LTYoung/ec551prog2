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
import eq_adt as logic
import fpga_adt as fpga
import json


''' config
configures the data for the FPGA synthesis engine
inputs:
- expr: expression(s) to be synthesized
- nLuts: number of LUTs - number > 0
- tLut: number of inputs per LUT - 4 or 6
- cLut: connectivity of LUTs - fully or partially connected
- isBitstream: boolean to determine if bitstream
'''
def config(expr: list, nLut: int, tLut: int, cLut='', isBitstream=False):
    if tLut != 4 and tLut != 6:
        raise Exception("tLut must be 4 or 6")
    if isBitstream:
        # convert bitstream to json to fpga_adt
        return
    
    data = fpga.fpga_adt()

    # create LUTs
    for i in range(nLut):
        lut = fpga.LUT('LUT' + str(i), tLut)
        data.add_lut(lut)

    # get partially connected LUT file if specified
    # TODO: implement
    connectivity = []
    if cLut != '':
        conn_file = 'connectivity.json'
        pass
        # with open(cLut) as f:
        #     lut_data = json.load(f)
    data.update_connectivity(connectivity)
    
    # minimize expression to fit in LUTs
    eq = []
    inputs = []
    rein   = {} # redundant input assignment
    outputs = []
    for e in expr:
        # TODO: take out output & check for same name I/O
        # eliminate all spaces
        e = e.replace(' ', '')
        ex = e.split('=')
        if ex[0] not in outputs:
            outputs.append(ex[0])
        else:
            if ex[0] in rein:
                rein[ex[0]] += 1
            else:
                rein[ex[0]] = 1
            # replace input in expression with redundant input
            ex[1] = ex[1].replace(ex[0], ex[0] + str(rein[ex[0]]))

        # if existing output is input, replace with equation?

        # minimize expression
        equ = logic.eq_adt(ex[1])
        lit, neg, ops = lse.parser(ex[1])
        equ.update_literals(lit)
        equ.update_neglist(neg)
        equ.update_ops(ops)

        # add literals to LUT data
        # TODO: check for I/O with the same name
        for l in lit:
            if l in outputs:
                # replace input in expression with redundant input
                continue
        
        parts = ex[1].split('+')
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
        eq.append(equ)

    # update ADT
    data.update_inputs(inputs)
    data.update_outputs(outputs)
    data.update_eqs(eq)
    
    # develop specs
    r = 2
    c = nLut // r
    w = tLut * c-1
    # create layout
    layout = []
    l = []
    for i in range(r+1):            # rows of LUTs + 1
        wr = []
        for j in range(w):          # rows of wires
            for k in range(c*2):    # columns of wires * 2
                wr.append('')
            l.append(wr)
            wr = []
        layout.append(l)
        l = []
    # create whole layout
    rlayout = [layout, layout]
    data.update_layout(rlayout)

    # check for more problems?
    # send data to FPGA synthesis engine

    # TODO: wait for FSE implementation
    # fdata is updated fpga_adt
    # ndata reports any problems / LUT usage
    # fdata,ndata = fse.fse()

    return data
# end config

''' calloc_lst
generate a list of zeros of length n
'''
def calloc_lst(n):
    return [0 for i in range(n)]
# end calloc_lst

# config test
bigF = "F=a*b*c*d*e*f*g + a*b*c*d*e'*f*g + a*b*c*d*e*f'*g + a'*b*c*d*e*f*g' + b*c*d*e*f + c*f'"
bigG = "G = F+a*b"
conf = config([bigF], 6, 4)
print(conf.get_eqs()[0].eq)
conf2 = config([bigF, bigG], 6, 4)
print(conf2.get_eqs()[0].eq, conf2.get_eqs()[1].eq)
