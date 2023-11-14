# test logic_syntehsis_engine.min.py
import logic_synthesis_engine as lse
import eq_adt as adt

input2 = "A*B'+C'"
inputFA = "A'*B'*Cin+A'*B*Cin'+A*B'*Cin'+A*B*Cin"
input12 = "D'*B' + B*A' + C*B' + C'*A"
inputHA = "((x0*x1)'*(x0'*x1')')"
input5 = "(x0'*x1')'"
input10 = "a*b*c*d*e*f*g + a*b*c*d*e'*f*g + a*b*c*d*e*f'*g + a'*b*c*d*e*f*g' + b*c*d*e*f + c*f'"

# eq0 = adt.eq_adt(input2)
# lit, neg, ops = lse.parser(input2)
# eq0.update_literals(lit)
# eq0.update_neglist(neg)
# eq0.update_ops(ops)
# print(eq0.eq)
# print("min:", lse.synth_engine(eq0))

# eq0 = adt.eq_adt(inputFA)
# lit, neg, ops = lse.parser(inputFA)
# eq0.update_literals(lit)
# eq0.update_neglist(neg)
# eq0.update_ops(ops)
# print(eq0.eq)
# print("min:", lse.synth_engine(eq0))

# eq0 = adt.eq_adt(input12)
# lit, neg, ops = lse.parser(input12)
# eq0.update_literals(lit)
# eq0.update_neglist(neg)
# eq0.update_ops(ops)
# print(eq0.eq)
# print("min:", lse.synth_engine(eq0))

ip = input10
eq0 = adt.eq_adt(ip)
lit, neg, ops = lse.parser(ip)
eq0.update_literals(lit)
eq0.update_neglist(neg)
eq0.update_ops(ops)
print(eq0.eq)
print("min:", lse.synth_engine(eq0))