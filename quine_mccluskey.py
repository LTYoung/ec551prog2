################################################
# quine_mccluskey.py
# Andrew Woska
# agwoska@bu.edu
################################################
# Contains an implementation of the Quine-McCluskey
# algorithm for the minimization of boolean functions.
################################################
# methods:
# quine_mccluskey(data: adt, literals: list) -> str
# solve(nvars: int, minterms: list) -> tuple
# compute_primes(nvars: int, cubes: list) -> set
# unate_cover(nvars: int, primes: list, ones: list) -> tuple
# calculate_complexity(nvars: int, minterms: list) -> int
# parentheses(glue: str, array: list) -> str
# get_function(vars: list, minterms: list) -> str
# bitcount(i: int) -> int
# is_power_of_two_or_zero(x: int) -> bool
# merge(a: tuple, b: tuple) -> tuple
# onset_minterms(tt: dict, bits: bool) -> list
# minterm_b2d(terms: list) -> list
# reduce(terms: list) -> dict
# getPIs(terms: list) -> list
# pi_b2d(pis: list) -> list
# b2d(b: list) -> int
################################################
# The following code is a modified version of the
# Quine-McCluskey algorithm from:
# https://github.com/prekageo/optistate/
# which is based on code from 
# Robert Dick <dickrp@eecs.umich.edu> and 
# Pat Maupin <pmaupin@gmail.com>.
# The code uses the MIT license.
################################################

import eq_adt as adt

""" quine_mccluskey
provides information for the Quine-McCluskey algorithm
"""
def quine_mccluskey(data: adt, literals: list, sop = True):
    if sop:
        mb = onset_minterms(data.table, True)
        md = terms_b2d(mb)
        vars = literals.copy()
        vars.reverse()
        soln = solve(len(vars), md)
        return get_sop_function(vars, soln[1])
    else:
        mb = onset_maxterms(data.table, True)
        md = terms_b2d(mb)
        vars = literals.copy()
        vars.reverse()
        soln = solve(len(vars), md)
        return get_pos_function(vars, soln[1])
# end quine_mccluskey

""" solve
executes the Quine-McCluskey algorithm
"""
def solve(nvars, minterms):
    # Handle special case for functions that always evaluate to True or False.
    if len(minterms) == 0:
      return 0,'0'
    if len(minterms) == 1<<nvars:
      return 0,'1'
    primes = compute_primes(nvars, minterms)
    return unate_cover(nvars, list(primes), minterms)
# end solve

""" compute_primes
find all prime implicants of the function
"""
def compute_primes(nvars, cubes):
    sigma = []
    for i in range(nvars+1):
        sigma.append(set())
    for i in cubes:
        sigma[bitcount(i)].add((i,0))

    primes = set()
    while sigma:
        nsigma = []
        redundant = set()
        for c1, c2 in zip(sigma[:-1], sigma[1:]):
            nc = set()
            for a in c1:
                for b in c2:
                    m = merge(a, b)
                    if m != None:
                        nc.add(m)
                        redundant |= set([a, b])
            nsigma.append(nc)
        primes |= set(c for cubes in sigma for c in cubes) - redundant
        sigma = nsigma
    return primes
# end compute_primes

""" unate_cover
use the PIs to find EPIs and PIs of the function
"""
def unate_cover(nvars, primes, ones):
    chart = []
    for one in ones:
        column = []
        for i in range(len(primes)):
            if (one & (~primes[i][1])) == primes[i][0]:
                column.append(i)
        chart.append(column)

    covers = []
    if len(chart) > 0:
        covers = [set([i]) for i in chart[0]]
    for i in range(1,len(chart)):
        new_covers = []
        for cover in covers:
            for prime_index in chart[i]:
                x = set(cover)
                x.add(prime_index)
                append = True
                for j in range(len(new_covers)-1,-1,-1):
                    if x <= new_covers[j]:
                        del new_covers[j]
                    elif x > new_covers[j]:
                        append = False
                if append:
                    new_covers.append(x)
        covers = new_covers

    min_complexity = 99999999
    for cover in covers:
        primes_in_cover = [primes[prime_index] for prime_index in cover]
        complexity = calculate_complexity(nvars, primes_in_cover)
        if complexity < min_complexity:
            min_complexity = complexity
            result = primes_in_cover
    return min_complexity,result
# end unate_cover

""" calculate_complexity
calculate complexity of the function
"""
def calculate_complexity(nvars, minterms):
    complexity = len(minterms)
    if complexity == 1:
        complexity = 0
    mask = (1<<nvars)-1
    for minterm in minterms:
        masked = ~minterm[1] & mask
        term_complexity = bitcount(masked)
        if term_complexity == 1:
            term_complexity = 0
        complexity += term_complexity
        complexity += bitcount(~minterm[0] & masked)
    return complexity
# end calculate_complexity

""" parentheses
add parentheses to a string
"""
def parentheses(glue, array):
    if len(array) > 1:
        return ''.join(['(',glue.join(array),')'])
    else:
        return glue.join(array)
# end parentheses

def get_sop_function(vars, minterms):
    if isinstance(minterms, str):
        return minterms
    or_terms = []
    for minterm in minterms:
      and_terms = []
      for j in range(len(vars)-1,-1,-1):
        if minterm[0] & 1<<j:
          and_terms.append(vars[j])
        elif not minterm[1] & 1<<j:
          and_terms.append('%s\'' % vars[j])
      or_terms.append(parentheses('*', and_terms))
    return parentheses(' + ', or_terms)
# end get_function

def get_pos_function(vars, minterms):
    if isinstance(minterms, str):
        return minterms
    or_terms = []
    for minterm in minterms:
      and_terms = []
      for j in range(len(vars)):
        if minterm[0] & 1<<j:
          and_terms.append(vars[j])
        elif not minterm[1] & 1<<j:
          and_terms.append('%s\'' % vars[j])
      or_terms.append(parentheses('+', and_terms))
    return parentheses(' * ', or_terms)

""" bitcount
count the number of bits in an integer
"""
def bitcount(i):
    res = 0
    while i > 0:
        res += i & 1
        i >>= 1
    return res
# end bitcount

""" is_power_of_two_or_zero
determine if an input is zero or a pwoer of two
"""
def is_power_of_two_or_zero(x):
    return (x & (~x + 1)) == x
# end is_power_of_two_or_zero

""" merge
combine two terms if they differ by only one bit
"""
def merge(a, b):
    if a[1] != b[1]:
        return None
    y = a[0] ^ b[0]
    if not is_power_of_two_or_zero(y):
        return None
    return (a[0] & b[0], a[1] | y)
# end merge

""" onset_minterms()
returns all minterms in the truth table
bits for Quine-McCluskey algorithm
"""
def onset_minterms(tt: dict, bits = False):
    minterms = []
    # get minimum number of bits required to represent all minterms
    blen = 1
    while True:
        if 1<<(blen+1) > len(tt):
            break
        blen += 1
    for k,v in tt.items():
        if v == 1:
            if bits:
                blit = []
                for b in range(0, blen):
                    blit.append((k >> b) & 1)
                blit.reverse()
                minterms.append(blit)
            else:
                minterms.append(k)
    return minterms
# end onset_minterms

""" onset_maxterms()
returns all maxterms in the truth table
bits for Quine-McCluskey algorithm
"""
def onset_maxterms(tt: dict, bits = False):
    minterms = []
    # get minimum number of bits required to represent all maxterms
    blen = 1
    while True:
        if 1<<(blen+1) > len(tt):
            break
        blen += 1
    for k,v in tt.items():
        if v == 0:
            if bits:
                blit = []
                for b in range(0, blen):
                    blit.append((k >> b) & 1)
                blit.reverse()
                minterms.append(blit)
            else:
                minterms.append(k)
    return minterms
# end onset_minterms

""" term_b2d(terms)
convert binary minterms to decimal
"""
def terms_b2d(terms: list):
    m = []
    for i in terms:
        m.append(b2d(i))
    return m
# end minterm_b2d

""" reduce(term)
get a reduced set of terms based on minterms
returns dict with keys 'pis' and 'reduced'
"""
def reduce(terms: list):
    reduced = []
    pis     = []
    pir     = []
    # determine how many bits are in each term
    if not terms:
        return {
            "pis": pis,
            "reduced": reduced
        }
    blen = len(terms[0])
    for i in range(0, len(terms)):
        red = False
        for j in range(i+1, len(terms)):
            if terms[i] != terms[j]:    # skip if same term
                # check if terms differ by only one bit
                diff = []
                for b in range(0, blen):
                    if terms[i][b] != terms[j][b]:
                        diff.append(b)
                if len(diff) == 1:
                    t = terms[i].copy()
                    t[diff[0]] = -1
                    reduced.append(t)
                    red = True
                    # add reduced terms to pir
                    # t[diff[0]] = 0
                    if terms[i] not in pir:
                        pir.append(terms[i])
                    # t[diff[0]] = 1
                    if terms[j] not in pir:
                        pir.append(terms[j])
        if not red and terms[i] not in pir:
            pis.append(terms[i])
    return {
        "pis": pis,
        "reduced": reduced
    }
# end reduce

""" getPIs()
get all prime implicants
"""
def getPIs(terms: list):
    # determine how many bits are in each term
    if not terms:
        return []
    blen = len(terms[0])
    # get all prime implicants using binary reduction
    pis = []
    if blen == 0:
        pass
    elif blen == 1:
        pis = terms
    elif blen == 2: # TODO: combine if necessary
        pis = reduce(terms)['pis']
        if not pis:
            pis = terms[:-1]
    else:
        red = reduce(terms)
        if red['pis']:
            for pi in red['pis']:
                pis.append(pi)
        for i in range(2,blen):
            if not red['reduced']:
                break
            red = reduce(red['reduced'])
            if red['pis']:
                for pi in red['pis']:
                    # add pis to pis
                    pis.append(pi)
        if red['reduced']:
            for pi in red['reduced']:
                pis.append(pi)
    return pis
# end getPIs

""" pi_b2d()
convert binary prime implicants to decimal
"""
def pi_b2d(pis: list):
    # determine how many bits are in each term
    if not pis:
        return []
    blen = len(pis[0])
    pid = []
    # convert binary to decimal based on bit length
    if blen == 0:
        pass
    elif blen == 1:
        if pis[0] == -1:
            pid = [0,1]
        else:
            pid = pis[0]
    else:
        for pi in pis:
            d = []
            idx = [i for i, x in enumerate(pi) if x == -1]
            for i in range(0, 1<<len(idx)):
                comb = []
                for j in range(len(pi)):
                    if j in idx:
                        comb.append((i >> idx.index(j)) & 1)
                    else:
                        comb.append(pi[j])
                d.append(comb)
            # convert binary to decimal
            dn = []
            for i in d:
                n = b2d(i)
                dn.append(n)
            pid.append(dn)
    return pid
# end getPIs_d

""" b2d()
binary list to decimal
"""
def b2d(b: list):
    n = 0
    for i in range(0, len(b)):
        n += b[i] << (len(b)-i-1)
    return n
# end b2d

""" getPILen
get the number of prime implicants
"""
def getPILen(data: adt):
    mb = onset_minterms(data.table, True)
    md = terms_b2d(mb)
    # reduce minterms to prime implicants
    pib = getPIs(mb)
    pid = pi_b2d(pib)
    # remove duplicates
    if len(pid) > 1:
        pid.reverse()
        p = len(pid)-2
        for i in range(0, p):
            if pid[p-i] == pid[p-i+1]:
                pid.pop(p-i)
        pid.reverse()
        # get last index
        p = len(pid)-1
        if pid[p] == pid[p-1]:
            pid.pop(p)
    # get number of prime implicants
    l = 0
    if len(pid) == 1:
        if len(pid[0]) == 1:
            l = 1
        for j in range(0, len(pid)):
            for k in range(j+1, len(pid)):
                if pid[0][j] != pid[0][k]:
                    l += 1
    else:
        for i in pid:
            # get number of combinations for each prime implicant
            for j in range(0, len(i)):
                if len(i) == 1:
                    l += 1
                else:
                    for k in range(j+1, len(i)):
                        if i[j] != i[k]:
                            l += 1
    if l == 0:
        pass
    return l
# end getPI

def genPIs(data: adt, literals: list):
    mb = onset_minterms(data.table, True)
    md = terms_b2d(mb)
    vars = literals.copy()
    vars.reverse()
    soln = solve(len(vars), md)
    return getPIs(vars, soln[1], md)
# end genPIs

""" getEPIs
get all essential prime implicants
TODO: does not get all EPIs
"""
def getEPIs(data: adt, literals: list):
    # get all minterms
    mb = onset_minterms(data.table, True)
    md = terms_b2d(mb)
    # reduce minterms to prime implicants
    pib = getPIs(mb)
    pid = pi_b2d(pib)
    # sort pid in ascending order
    pid.sort()
    # remove duplicates
    if len(pid) > 1:
        pid.reverse()
        p = len(pid)-2
        for i in range(0, p):
            if pid[p-i] == pid[p-i+1]:
                pid.pop(p-i)
        pid.reverse()
        # get last index
        p = len(pid)-1
        if pid[p] == pid[p-1]:
            pid.pop(p)
    # construct prime implicant table
    empty_row = []
    for i in range(0, len(pid)+1):
        empty_row.append('-')
    pis = []
    pit = {
        "minterms": md,
        "pis": pis
    }
    for row in range(0, len(md)):
        r = empty_row.copy()
        r[0] = md[row]
        # check if minterm is covered by a PI
        for col in range(0, len(pid)):
            if md[row] in pid[col]:
                r[col+1] = 'x'
        pis.append(r)

    # Method
    # get EPIs
    epi = []
    times = 0
    while times < 2:
        times += 1
        nepi = []
        for row in range(0, len(md)):
            x = []
            for col in range(1, len(pid)+1):
                if pis[row][col] == 'x':
                    x.append(pid[col-1])
            if len(x) == 1:
                if x[0] not in nepi:
                    nepi.append(x[0])
        # remove EPIs
        rows = []
        for pi in nepi:
            # get index of pi in md
            idx = pid.index(pi)
            # remove pi from pis
            rm = True
            while rm:
                rm = False
                for row in range(0, len(pis)):
                    if pis[row][idx+1] == 'x':
                        # index of pi in md
                        r = md.index(pis[row][0])
                        rows.append(r)
                        pis.pop(row)
                        rm = True
                        break
        epi += nepi
        # remove rows from pit
        rows.sort()
        rows.reverse()
        for row in rows:
            md.pop(row)
        # get rid of empty columns
        rows = []
        for col in range(1, len(pid)+1):
            x = 0
            for row in range(0, len(pis)):
                if pis[row][col] == 'x':    # TODO
                    x += 1
            if x == 0:
                rows.append(col-1)
        # remove rows from pit
        rows.reverse()
        for row in rows:
            for r in range(0, len(pis)):
                pis[r].pop(row+1)
        for row in rows:
            pid.pop(row)
        # row dominance
        if pis:
            drows = find_dominated_rows(pis)
            for row in drows:
                # eliminate row
                idx = pis.index(row)
                pis.pop(idx)
                md.pop(idx)
            # column dominance
            dcols = find_dominated_columns(pis)
            dcols.reverse()
            for col in dcols:
                # eliminate column
                for row in range(0, len(pis)):
                    pis[row].pop(col)
                pid.pop(col-1)
    if not epi:
        mb = onset_minterms(data.table, True)
        md = terms_b2d(mb)
        vars = literals.copy()
        vars.reverse()
        soln = solve(len(vars), md)
        epi = list(soln[1])
    return epi
# end getEPIs


def is_dominated(row1, row2):
    for i in range(1, len(row1)):
        if row1[i] == 'x' and row2[i] == '-':
            return False
    return True

def find_dominated_rows(table):
    result = []
    for i in range(len(table)):
        dominated = False
        for j in range(len(table)):
            if i != j and is_dominated(table[i], table[j]):
                dominated = True
                break
        if not dominated:
            result.append(table[i])
    return result

def find_dominated_columns(pis):
    if not pis:
        return []
    num_cols = len(pis[0])
    dominated_columns = set()

    # switch rows and columns
    table = []
    for i in range(len(pis[0])):
        table.append([row[i] for row in pis])
    1==1
    for i in range(1, num_cols):
        for j in range(i+1, num_cols):
            # find columns with 1 in the same rows
            if table[i] == table[j]:
                dominated_columns.add((i, j))
            else:
                # if column has 1 in more than one row
                if table[i].count('x') > 1 and table[j].count('x') == 1:
                    dominated_columns.add((i, j))
                elif table[i].count('x') == 1 and table[j].count('x') > 1:
                    dominated_columns.add((j, i))

    d = set()
    for i, j in dominated_columns:
        d.add(j)
    return list(d)
