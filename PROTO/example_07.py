# MACHINE counter
# ...
# END
#
# IMPLEMENTATION counter_i
# REFINES counter
# CONCRETE_VARIABLES value, error
# INVARIANT
#     value: INT & error : BOOL & (error = overflow)
# INITIALISATION
#     value := 0;                 inst0
#     error := FALSE              inst1
# OPERATIONS
#     zero =
#     BEGIN                       inst6
#         value := 0;             inst0
#         error := FALSE          inst1
#     END;
#     inc =
#     IF value < MAXINT           inst4
#     THEN                        ifbr0
#         value := value + 1      inst2
#     ELSE                        ifbr1
#         error := TRUE           inst3
#     END;
#     res <-- get = 
#         res := value            inst5
# END

import bimp

value = bimp.make_imp_var("value", bimp.INT)
error = bimp.make_imp_var("error", bimp.BOOL)
res = bimp.make_arg_var("res", bimp.INT)

inst0 = bimp.make_beq(value, bimp.ZERO)
inst1 = bimp.make_beq(error, bimp.FALSE)

inst2 = bimp.make_beq(value, bimp.make_sum(value, bimp.ONE))
inst3 = bimp.make_beq(error, bimp.TRUE)

res1 = bimp.make_arg_var("res", bimp.INT)
ifbr0 = bimp.make_if_br(bimp.make_lt(value, bimp.MAXINT), inst2)
ifbr1 = bimp.make_if_br(None, inst3)
inst4 = bimp.make_if([ifbr0, ifbr1])
inst5 = bimp.make_beq(res1, value)
inst6 = bimp.make_blk([inst0, inst1])

zero = bimp.make_oper("zero", [], [], inst6)
inc = bimp.make_oper("inc", [], [], inst4)
get = bimp.make_oper("get", [], [res1], inst5)

imports = []
consts = []
vars = [value, error]
init = [inst0, inst1]
ops = [zero, inc, get]

counter_i = bimp.make_implementation("counter_i", imports, consts, vars, init, ops)
counter = bimp.make_machine("counter", counter_i)

# IMPLEMENTATION wd_i
# REFINES wd
# VALUES timeout=50
# IMPORTS counter
# INITIALISATION
#    VAR count IN                        inst11
#        count := 0;                     inst7
#        WHILE count < timeout DO        inst10
#            inc;                        inst8
#            count := count+1            inst9
#        END
#    END
# OPERATIONS
#    start =
#       zero;                            inst12
#    tick =
#    VAR elapsed, diff IN                inst17
#        elapsed <-- get;                inst13
#        diff := timeout - elapsed;      inst14
#        IF diff > 0                     inst16
#        THEN                        ifbr2
#            inc                         inst15
#        END
#    END;
#    res <-- expired =
#    VAR elapsed, diff IN                inst23
#        elapsed <-- get;                inst18
#        diff := timeout - elapsed;      inst19
#        IF diff < 0                     inst22
#        THEN                        ifbr3
#            res := TRUE                 inst20
#        ELSE                        ifbr4
#            res := FALSE                inst21
#        END
#    END
# END
imp_counter = bimp.make_import(counter, None)
timeout = bimp.make_const("timeout", bimp.INT, bimp.make_intlit(50))

count = bimp.make_loc_var("count", bimp.INT)

inst7 = bimp.make_beq(count, bimp.ZERO)
inst8 = bimp.make_call(inc, [], [], imp_counter)
inst9 = bimp.make_beq(count, bimp.make_sum(count, bimp.ONE))
inst10 = bimp.make_while(bimp.make_lt(count, timeout), [inst8, inst9])
inst11 = bimp.make_var_decl([count], [inst7, inst10])

inst12 = bimp.make_call(zero, [], [], imp_counter)
start = bimp.make_oper("start", [], [], inst12)

elapsed1 = bimp.make_loc_var("elapsed", bimp.INT)
diff1 = bimp.make_loc_var("diff", bimp.INT)
inst13 = bimp.make_call(get, [], [elapsed1], imp_counter)
inst14 = bimp.make_beq(diff1, bimp.make_diff(timeout, elapsed1))
inst15 = inst8
ifbr2 = bimp.make_if_br(bimp.make_gt(diff1, bimp.ZERO), inst15)
inst16 = bimp.make_if([ifbr2])
inst17 = bimp.make_var_decl([elapsed1, diff1], [inst13, inst14, inst16])
tick = bimp.make_oper("tick", [], [], inst17)

elapsed2 = bimp.make_loc_var("elapsed", bimp.INT)
diff2 = bimp.make_loc_var("diff", bimp.INT)
res = bimp.make_arg_var("res", bimp.BOOL)
inst18 = bimp.make_call(get, [], [elapsed2], imp_counter)
inst19 = bimp.make_beq(diff2, bimp.make_diff(timeout, elapsed2))
inst20 = bimp.make_beq(res, bimp.TRUE)
inst21 = bimp.make_beq(res, bimp.FALSE)
ifbr3 = bimp.make_if_br(bimp.make_lt(diff2, bimp.ZERO), inst20)
ifbr4 = bimp.make_if_br(None, inst21)
inst22 = bimp.make_if([ifbr3, ifbr4])
inst23 = bimp.make_var_decl([elapsed2, diff2], [inst18, inst19, inst22])
expired = bimp.make_oper("expired", [], [res], inst23)

init2 = [inst11]
ops2 = [start, tick, expired]
wd_i = bimp.make_implementation("wd_i", [imp_counter], [timeout], [], init2, ops2)
