# IMPLEMENTATION counter_i
# CONCRETE_VARIABLES value, error
# INITIALISATION
#   BEGIN
#     value := 0;
#     error := FALSE
#   END
# OPERATIONS
# zero =
#   BEGIN
#     value := 0;
#     error := FALSE
#   END
# inc =
#   IF value < MAXINT
#   THEN
#     value := value + 1
#   ELSE
#     error := TRUE
#   END;
# dec =
#   IF 0 < value
#   THEN
#     value := value - 1
#   ELSE
#     error := TRUE
#   END;
# res <-- valid =
#   BEGIN
#     IF error = TRUE
#     THEN
#       res := FALSE
#     ELSE
#       res := TRUE
#     END
#   END;
# res <-- get =
#   res := value;
# set(avalue) =
#   value := avalue
# END

import bimp

value = bimp.make_imp_var("value", bimp.INT)
error = bimp.make_imp_var("error", bimp.BOOL)
res1 = bimp.make_arg_var("res", bimp.BOOL)
res2 = bimp.make_arg_var("res", bimp.INT)
avalue = bimp.make_arg_var("avalue", bimp.INT)

inst1 = bimp.make_beq(value, bimp.ZERO)
inst2 = bimp.make_beq(error, bimp.FALSE)
inst3 = bimp.make_blk([inst1, inst2])
zero = bimp.make_oper("zero", [], [], inst3)

inst4 = bimp.make_beq(value, bimp.make_sum(value, bimp.ONE))
inst5 = bimp.make_beq(error, bimp.TRUE)
branch1 = bimp.make_if_br(bimp.make_lt(value, bimp.MAXINT), inst4)
branch2 = bimp.make_if_br(None, inst5)
inst6 = bimp.make_if([branch1, branch2])
inc = bimp.make_oper("inc", [], [], inst6)

inst7 = bimp.make_beq(value, bimp.make_diff(value, bimp.ONE))
branch3 = bimp.make_if_br(bimp.make_lt(bimp.ZERO, value), inst7)
branch4 = bimp.make_if_br(None, inst5)
inst8 = bimp.make_if([branch3, branch4])
dec = bimp.make_oper("dec", [], [], inst8)

inst9 = bimp.make_beq(res1, bimp.TRUE)
inst10 = bimp.make_beq(res1, bimp.FALSE)
branch6 = bimp.make_if_br(bimp.make_eq(error, bimp.TRUE), inst9)
branch7 = bimp.make_if_br(bimp.make_eq(error, bimp.FALSE), inst10)
inst11 = bimp.make_if([branch6, branch7])
inst12 = bimp.make_blk(inst11)
valid = bimp.make_oper("valid", [], [res1], inst12)

inst13 = bimp.make_beq(res2, value)
get = bimp.make_oper("get", [], [res2], inst13)

inst14 = bimp.make_beq(value, avalue)
set = bimp.make_oper("set", [avalue], [], inst14)

imports = []
consts = []
vars = [value, error]
init = [inst3]
ops = [zero, inc, dec, get, set]
root = bimp.make_implementation("counter_i",
                                imports, consts, vars, init, ops)
