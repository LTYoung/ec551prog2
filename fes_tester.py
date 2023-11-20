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

lut_inputs, lut_outputs, lut_data= fse.partition_to_lut(eq0, conf0.get_lut_type(), conf0)

print("Original table:")
print(eq0.table)
print("LUT inputs:")
print(lut_inputs)
print("LUt outputs:")
print(lut_outputs)
print("LUT data:")
print(lut_data)
# print("MUX output assignments: ")
# print(mux_out)