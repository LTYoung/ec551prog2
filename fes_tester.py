# test runner for fse
import fse as fse
import logic_synthesis_engine as lse
import eq_adt as eq
import fpga_adt as fpga
import configurator as conf

input0 = "F = a*b*c*d*e*f*g + a*b*c*d*e'*f*g + a*b*c*d*e*f'*g + a'*b*c*d*e*f*g' + b*c*d*e*f + c*f'"
input1 = "G = F+a*b"
input2 = "H = a+b"
input3 = "I = G*H"

inputComp = [input0, input1, input2]
#inputComp = [input1, input2]

# eq0 = eq.eq_adt(input0)
# lit, neg, ops = lse.parser(input0)
# eq0.update_literals(lit)
# eq0.update_neglist(neg)
# eq0.update_ops(ops)
# print(eq0.eq)
# print("min: ", lse.synth_engine(eq0))


conf0 = conf.config(inputComp, 50, 4)

eqts = conf0.eqs


for each in eqts:
    (
        lut_inputs,
        lut_outputs,
        lut_data,
        num_luts,
        output_lut_name,
        output_var_name,
    ) = fse.partition_to_lut(each, conf0.get_lut_type(), conf0)

    print("Original table:")
    print(each.table)
    print("LUT inputs:")
    print(lut_inputs)
    print("LUt outputs:")
    print(lut_outputs)
    print("LUT data:")
    print(lut_data)
    print("Number of LUTs:")
    print(num_luts)
    print("Output LUT name:")
    print(output_lut_name)
    print("Output variable name:")
    print(output_var_name)


routed_free = fse.routing_free(eqts, conf0)
print("Free done")


conf1 = conf.config(inputComp, 50, 4)


routed_constrained = fse.routing_constrained(eqts, conf1)
print("Constrained done")