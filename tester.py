# test logic_syntehsis_engine.py
import configurator as config
import logic_synthesis_engine as lse
import eq_adt as adt

def lse_tester():
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
# end lse_tester

def config_tester():
    bigF = "F=a*b*c*d*e*f*g + a*b*c*d*e'*f*g + a*b*c*d*e*f'*g + a'*b*c*d*e*f*g' + b*c*d*e*f + c*f'"
    bigG = "G = F+a*b"
    otherG = "G = a+b"
    bigH = "H = a*b + a"
    IwithH = "I = H + b"
    conf = config.config([bigF], 6, 4)
    print(conf[1].get_reqs())
    conf2 = config.config([bigF, bigG], 6, 4)
    print(conf2[1].get_reqs())

    conf3 = config.config([bigF, bigG, otherG], 8, 4)
    print(conf3[1].get_reqs())

    conf4 = config.config([bigH], 4, 4)
    print(conf4[1].get_reqs())

    conf5 = config.config([bigH, IwithH], 4, 4)
    print(conf5[1].get_reqs())

    conf6 = config.config([bigF, bigG, bigH], 8, 4)
    print(conf6[1].get_reqs())
# end config_tester


def fse_tester():
    print("tests being made")
# end fse_tester