# IMPLEMENTATION counter_i
# REFINES...
# CONCRETE_CONSTANTS MAX
# PROPRTIES MAX : INT & MAX = 3
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
#   IF value < MAX
#   THEN
#     value := succ value
#   ELSE
#     error := TRUE
#   END;
# END
# dec =
#   IF 0 < value
#   THEN
#     value := pred value
#   ELSE
#     error := TRUE
#   END;
# END

import bimp

value = bimp.make_imp_var("value", bimp.INT)
error = bimp.make_imp_var("error", bimp.INT)
three = bimp.make_intlit(3)
max = bimp.make_const("MAX", bimp.INT, three)

comp1 = bimp.make_lt(value, max)
comp2 = bimp.make_lt(bimp.ZERO, value)

inst1 = bimp.make_beq(value, bimp.ZERO)
inst2 = bimp.make_beq(error, bimp.FALSE)
inst3 = bimp.make_blk([inst1, inst2])
inst4 = bimp.make_beq(value, bimp.make_succ(value))
inst5 = bimp.make_beq(error, bimp.TRUE)
branch1 = bimp.make_if_br(comp1, inst4)
branch2 = bimp.make_if_br(None, inst5)
inst6 = bimp.make_if([branch1, branch2])
inst7 = bimp.make_beq(value, bimp.make_pred(value))
branch3 = bimp.make_if_br(comp2, inst7)
branch4 = bimp.make_if_br(None, inst5)
inst8 = bimp.make_if([branch3, branch4])
zero = bimp.make_oper("zero", [], [], inst3)
inc = bimp.make_oper("inc", [], [], inst6)
dec = bimp.make_oper("dec", [], [], inst8)
init = [inst3]
imports = []
consts = [max]
vars = [value, error]
ops = [zero, inc, dec]
root = bimp.make_implementation("counter_i", imports, consts, vars, init, ops)
