# IMPLEMENTATION
#     switch_i
# REFINES
#     switch
# CONCRETE_VARIABLES
#     v1 ,
#     v2
# INVARIANT
#     v1 : INT & v2 : INT &
#     v1 : 0..4 & v2 : 0..1 &
#     ((v1 = 0 & v2 = 0) or
#         (v1 = 1 & v2 = 0) or
#         (v1 = 1 & v2 = 1) or
#         (v1 = 2 & v2 = 1) or
#         (v1 = 4 & v2 = 1))
# INITIALISATION
#     v1 := 0;
#     v2 := 0
    
# OPERATIONS
#     step =
#     VAR sum IN
#         sum := v1 + v2;
#         CASE sum OF
#             EITHER 0 THEN
#                 v1 := v1 + 1
#             OR 1 THEN
#                 v2 := v1 + 1
#             OR 2, 3 THEN
#                 v1 := v1 * 2
#             ELSE
#                 BEGIN
#                     v1 := 0;
#                     v2 := 0
#                 END
#             END
#         END
#     END
# END

import bimp

v1 = bimp.make_imp_var("v1", bimp.INT)
v2 = bimp.make_imp_var("v2", bimp.INT)

two = bimp.make_intlit(2)
three = bimp.make_intlit(3)

inst1 = bimp.make_beq(v1, bimp.ZERO)
inst2 = bimp.make_beq(v2, bimp.ZERO)

sum = bimp.make_loc_var("sum", bimp.INT)
term1 = bimp.make_sum(v1, v2)
inst3 = bimp.make_beq(sum, term1)

term2 = bimp.make_sum(v1, bimp.ONE)
inst4 = bimp.make_beq(v1, term2)
br1 = bimp.make_case_br([bimp.ZERO], inst4)

term3 = bimp.make_sum(v2, bimp.ONE)
inst5 = bimp.make_beq(v2, term3)
br2 = bimp.make_case_br([bimp.ONE], inst5)

term4 = bimp.make_prod(v1, two)
inst6 = bimp.make_beq(v1, term4)
br3 = bimp.make_case_br([two,three], inst6)

inst7 = bimp.make_blk([inst1, inst2])
br4 = bimp.make_case_br([], inst7)

inst8 = bimp.make_case(sum, [br1, br2, br3, br4])

inst9 = bimp.make_var_decl([sum], [inst3, inst8])
step = bimp.make_oper("step", [], [], inst9)

imports = []
consts = []
vars = [v1, v2]
init = [inst1, inst2]
ops = [step]
root = bimp.make_implementation("switch_i", imports, consts, vars, init, ops)
