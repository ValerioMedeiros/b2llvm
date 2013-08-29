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

from bimp import *

v1 = make_imp_var("v1", INT)
v2 = make_imp_var("v2", INT)

one = make_intlit(1)
two = make_intlit(2)
three = make_intlit(3)

inst1 = make_beq(v1, zero)
inst2 = make_beq(v2, zero)

sum = make_loc_var("sum", INT)
term1 = make_sum(v1, v2)
inst3 = make_beq(sum, term1)

term2 = make_sum(v1, one)
inst4 = make_beq(v1, term2)
br1 = make_case_br([zero], inst4)

term3 = make_sum(v2, one)
inst5 = make_beq(v2, term3)
br2 = make_case_br([one], inst5)

term4 = make_prod(v1, two)
inst6 = make_beq(v1, term4)
br3 = make_case_br([two,three], inst6)

inst7 = make_blk([inst1, inst2])
br4 = make_case_br([], inst7)

inst8 = make_case(sum, [br1, br2, br3, br4])

inst9 = make_var_decl([sum], [inst3, inst8])
step = make_oper("step", [], [], inst9)

vars = [v1, v2]
consts = []
init = [inst1, inst2]
ops = [step]
root = make_implementation("switch_i", vars, consts, init, ops)
