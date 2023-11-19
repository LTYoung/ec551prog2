# test runner for fse
import fse as fse
import logic_synthesis_engine as lse
import eq_adt as eq
import fpga_adt as fpga
import configurator as conf

input0 = "(a+b'*c)*(d*e')+(f'*g+h)"

eq0 = eq.eq_adt(input0)
lit, neg, ops = lse.parser(input0)
eq0.update_literals(lit)
eq0.update_neglist(neg)
eq0.update_ops(ops)
print(eq0.eq)
print("min: ", lse.synth_engine(eq0))


analyze_out = fse.analyze_eq([eq0])
print(analyze_out)

conf0 = conf.config([input0], 6, 4)
print(conf0.get_eqs()[0].eq)

fse.partition_to_lut(conf0.get_eqs()[0], 4, conf0)
