# test runner for fse
import fse as fse
import logic_synthesis_engine as lse
import eq_adt as eq
import fpga_adt as fpga
import configurator as conf

input0 = "F=a*b*c*d*e*f*g + a*b*c*d*e'*f*g + a*b*c*d*e*f'*g + a'*b*c*d*e*f*g' + b*c*d*e*f + c*f'"

eq0 = eq.eq_adt(input0)
lit, neg, ops = lse.parser(input0)
eq0.update_literals(lit)
eq0.update_neglist(neg)
eq0.update_ops(ops)
print(eq0.eq)
print("min: ", lse.synth_engine(eq0))


analyze_out = fse.analyze_eq([eq0])
print(analyze_out)

conf0 = conf.config([input0], 500, 4)
print(conf0.get_eqs()[0].eq)

table, num_luts, mux= fse.partition_to_lut(eq0, 4, conf0)

print("Original table:")
print(eq0.table)
print("Partitioned table:")
print(table)
print("LUTs needed:")
print(num_luts)
print("MUX assignments:")
print(mux)
# print("MUX output assignments: ")
# print(mux_out)