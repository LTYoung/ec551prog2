################################################
# logic_synthesis_engine.py
# Andrew Woska
# agwoska@bu.edu
################################################
# Contains a minimized version of the boolean equation
# parser and the sythesis engine
################################################
# methods:
# parser(eq) -> (literals, neglist, ops)
# synth_engine(data: adt) -> str
################################################

import eq_adt as adt
import quine_mccluskey as qm


"""
Parameters
eq: str
equation given to synthesis engine
"""
def parser(eq: str, aag = False, pos = False):
    literals = []
    neglist = []
    ops = []
    prev = ""
    lit = ""
    eqo = eq # original equation
    if aag:
        # find last parenthesis
        lp = eqo.rfind(")")
        # if outside parenthesis contains NOT, DeMorgan's and remove parenthesis and is SOP
        if len(eqo)-1 != lp: # end is NOTed
            # remove last index of eq
            eq = eq[:len(eq)-1] + eq[len(eq):]
            # if only 1 right parenthesis, remove it
            if eqo.count(")") != 1:
                # perform DeMorgan's
                idx = [] # indicies to remove
                posa = find_positions("*", eqo)
                for i in range(0, len(eqo)-2):
                    # remove '(' and ')' and ')\'', also if change ANDs to ORs where necessary
                    if eq[i] == '(':
                        idx.append(i)
                    elif eq[i] == ')\'':
                        idx.append(i)
                        # change following AND to OR
                        # get next position of AND after i
                        for j in range(0, len(posa)):
                            if posa[j] > i:
                                eq = replace_str_index(eq, posa[j], '+')
                                break
                    elif eq[i] == ')':
                        # change to NOT
                        eq = replace_str_index(eq, i, '\'')
                        # change following AND to OR
                        for j in range(0, len(posa)):
                            if posa[j] > i:
                                eq = replace_str_index(eq, posa[j], '+')
                                break
                    elif eq[i] == ' ':
                        idx.append(i)
                # remove indicies
                idx.reverse()
                for i in idx:
                    eq = eq[:i] + eq[i+1:]
                1 == 1
            else:
                # remove all parenthesis
                eq = eq[:0] + eq[1:]
                eq = eq[:len(eq)-1] + eq[len(eq):]
                # convert NOTs to NOT NOTs and vice versa
                i = 0
                while i < len(eq):
                    if eq[i] == '*':
                        if eq[i-1] == '\'':
                            eq = replace_str_index(eq, i-1, '')
                            eq = replace_str_index(eq, i-1, '+')
                            # eq[i-1] = '+'
                        else:
                            eq = insert_char_at_index(eq, i-1, '\'')
                            eq = replace_str_index(eq, i, '+')
                            i += 1
                    i += 1
                # check last character
                if eq[len(eq)-1] == '\'':
                    eq = replace_str_index(eq, len(eq)-1, '')
                else:
                    eq = eq.join('\'')
        else: # is possibly POS, process seapretely
            # remove first and last parenthesis
            eq = eq[:0] + eq[1:]
            eq = eq[:len(eq)-1] + eq[len(eq):]
            # if no more parenthesis, is SOP
            if eq.count(')') > 0: # is POS
                pos = True
                # perform DeMorgan's
                rtp = find_positions(')', eq)
                ltp = find_positions('(', eq)
                for i in range(len(rtp)):
                    j = ltp[i]
                    while j < rtp[i]:
                        if eq[j] == '*':
                            eq = replace_str_index(eq, j, '+')
                            if eq[j-1] == '\'':
                                eq = replace_str_index(eq, j-1, '')
                                rtp = find_positions(')', eq)
                            else:
                                eq = insert_char_at_index(eq, j, '\'')
                                j += 1
                                rtp = find_positions(')', eq)
                        j += 1
                    # check last character
                    if eq[rtp[i]-1] == '\'':
                        eq = replace_str_index(eq, rtp[i]-1, '')
                    else:
                        eq = insert_char_at_index(eq, rtp[i], '\'')
                    rtp = find_positions(')', eq)
                    ltp = find_positions('(', eq)
                eq = eq.replace(')\'', ')')
        
    for i in range(0, len(eq)):
        n = eq[i]
        if n == " " or n == '(' or n == ')':  # discard spaces
            continue
        if prev.isalnum():
            if n.isalnum():
                lit += n  # continue literal
            elif n == "'":
                literals.append(lit)  # add to literals
                neglist.append(1)  # inverted
            elif n == "+" or n == "*":
                literals.append(lit)  # add to literals
                ops.append(n)  # next operation
                neglist.append(0)  # non-inverted
            else:
                print("error: illegal character used")
        elif prev == "'":
            if n.isalnum():
                print("error: equation format")
            elif n == "'":
                print("error: double inverted")
            elif n == "+" or n == "*":
                ops.append(n)  # next operation
            else:
                print("error: illegal character used")
        elif prev == "+" or prev == "*":
            if n.isalpha():
                lit = n  # start next literal
            elif n == "'":
                print("error: inversion before literal")
            elif n == "+" or n == "*":
                print("error: two operators in a row")
            else:
                print("error: illegal character used")
        else:
            if n.isalpha():
                lit = n  # start first literal
            else:
                print("error: illegal start")
        prev = n
    if prev.isalnum():  # finish propagation if necessary
        literals.append(lit)
        neglist.append(0)
    
    if aag:
        eq = eqo # restore original equation
    if pos:
        ops.append('POS')

    return literals, neglist, ops
# end parser


"""
Parameters
data: str
    equation given to synthesis engine
opt: str
    command given to synthesis engine
"""
def synth_engine(data: adt):
    # Truth Table Generator
    oliteral = []  # ordered literals
    for i in data.literals:
        if i not in oliteral:
            oliteral.append(i)

    nliteral = len(oliteral)  # number of unique literals
    table = {}
    for i in range(2**nliteral):
        if len(data.ops) == len(data.neglist):
            table[i] = 1
        else:
            table[i] = 0

    term = []  # term
    tern = []  # negative term
    if len(data.ops) != len(data.neglist):
        for l in range(len(data.literals)):
            # add literal to term
            term.append(data.literals[l])
            tern.append(data.neglist[l])
            # check if and/or
            if l < len(data.literals) - 1:
                if data.ops[l] == "+":
                    terr = []
                    # put terms in oliteral order
                    for i in oliteral:
                        if i in term:
                            # add if negative
                            lit = i
                            if tern[term.index(i)] == 1:
                                lit += "'"
                            terr.append(lit)
                        else:
                            terr.append(" ")
                    # generate relevant inputs
                    pos = [
                        i for i, l in enumerate(terr) if l == " "
                    ]  # positions of empty literals
                    dt = len(terr)  # term length

                    if not pos:
                        n = 0
                        # determine input
                        for i in range(dt):
                            if not terr[i].endswith("'"):
                                n += 1 << (dt - i - 1)
                        table[n] = 1
                    else:
                        # determine inputs
                        ip = []
                        for i in range(2 ** len(pos)):
                            tert = terr.copy()  # copy of term
                            for x in pos:
                                if not i & 1 << pos.index(x):
                                    tert[x] = "'"
                            ip.append(tert)
                        for i in ip:
                            n = 0
                            # determine input
                            for j in range(dt):
                                if not i[j].endswith("'"):
                                    n += 1 << (dt - j - 1)
                            table[n] = 1
                    term = []
                    tern = []
            elif l == len(data.literals) - 1:
                terr = []  # term in oliteral order
                # put terms in oliteral order
                for i in oliteral:
                    if i in term:
                        # add if negative
                        lit = i
                        if tern[term.index(i)] == 1:
                            lit += "'"
                        terr.append(lit)
                    else:
                        terr.append(" ")
                # generate relevant inputs
                pos = [
                    i for i, l in enumerate(terr) if l == " "
                ]  # positions of empty literals
                dt = len(terr)  # term length

                if not pos:
                    n = 0
                    # determine input
                    for i in range(dt):
                        if not terr[i].endswith("'"):
                            n += 1 << (dt - i - 1)
                    table[n] = 1
                else:
                    # determine inputs
                    ip = []
                    for i in range(2 ** len(pos)):
                        tert = terr.copy()  # copy of term
                        for x in pos:
                            if not i & 1 << pos.index(x):
                                tert[x] = "'"
                        ip.append(tert)
                    for i in ip:
                        n = 0
                        # determine input
                        for j in range(dt):
                            if not i[j].endswith("'"):
                                n += 1 << (dt - j - 1)
                        table[n] = 1
    else:
            for l in range(len(data.literals)):
                # add literal to term
                term.append(data.literals[l])
                tern.append(data.neglist[l])
                # check if and/or
                if l < len(data.literals) - 1:
                    if data.ops[l] == "*":
                        terr = []
                        # put terms in oliteral order
                        for i in oliteral:
                            if i in term:
                                # add if negative
                                lit = i
                                if tern[term.index(i)] == 1:
                                    lit += "'"
                                terr.append(lit)
                            else:
                                terr.append(" ")
                        # generate relevant inputs
                        pos = [
                            i for i, l in enumerate(terr) if l == " "
                        ]  # positions of empty literals
                        dt = len(terr)  # term length

                        if not pos:
                            n = 0
                            # determine input
                            for i in range(dt):
                                if not terr[i].endswith("'"):
                                    n += 1 << (dt - i - 1)
                            table[n] = 0
                        else:
                            # determine inputs
                            ip = []
                            for i in range(2 ** len(pos)):
                                tert = terr.copy()  # copy of term
                                for x in pos:
                                    if not i & 1 << pos.index(x):
                                        tert[x] = "'"
                                ip.append(tert)
                            for i in ip:
                                n = 0
                                # determine input
                                for j in range(dt):
                                    if not i[j].endswith("'"):
                                        n += 1 << (dt - j - 1)
                                table[n] = 0
                        term = []
                        tern = []
                elif l == len(data.literals) - 1:
                    terr = []  # term in oliteral order
                    # put terms in oliteral order
                    for i in oliteral:
                        if i in term:
                            # add if negative
                            lit = i
                            if tern[term.index(i)] == 1:
                                lit += "'"
                            terr.append(lit)
                        else:
                            terr.append(" ")
                    # generate relevant inputs
                    pos = [
                        i for i, l in enumerate(terr) if l == " "
                    ]  # positions of empty literals
                    dt = len(terr)  # term length

                    if not pos:
                        n = 0
                        # determine input
                        for i in range(dt):
                            if not terr[i].endswith("'"):
                                n += 1 << (dt - i - 1)
                        table[n] = 0
                    else:
                        # determine inputs
                        ip = []
                        for i in range(2 ** len(pos)):
                            tert = terr.copy()  # copy of term
                            for x in pos:
                                if not i & 1 << pos.index(x):
                                    tert[x] = "'"
                            ip.append(tert)
                        for i in ip:
                            n = 0
                            # determine input
                            for j in range(dt):
                                if not i[j].endswith("'"):
                                    n += 1 << (dt - j - 1)
                            table[n] = 0
    # test table out
    data.update_table(table)

    # return minimized expressions
    return qm.quine_mccluskey(data, oliteral)
# end synth_engine

def find_positions(c, s):
    return [i for i, char in enumerate(s) if char == c]

def replace_str_index(text,index=0,replacement=''):
    return '%s%s%s'%(text[:index],replacement,text[index+1:])

def insert_char_at_index(input_string, index, char):
    return input_string[:index] + char + input_string[index:]
