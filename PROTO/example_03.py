# IMPLEMENTATION
#    swap_i
# REFINES
#    swap
# CONCRETE_VARIABLES
#    v1 ,  v2
# INVARIANT
#     v1 : INT & v2 : INT
# INITIALISATION
#    v1 := 0; v2 := 1
# OPERATIONS
#    step =
#    VAR tmp IN
#        BEGIN
#            tmp := v1;
#            v1 := v2;
#            v2 := tmp
#        END
#    END;
#    set ( av1 , av2 ) =
#    BEGIN
#        v1 := av1;
#        v2 := av2
#    END
#    ;
#    r1 , r2 <-- get =
#    BEGIN
#        r1 := v1;
#        r2 := v2
#    END
# END

import bimp

v1 = bimp.make_imp_var("v1", bimp.INT)
v2 = bimp.make_imp_var("v2", bimp.INT)
r1 = bimp.make_arg_var("r1", bimp.INT)
r2 = bimp.make_arg_var("r2", bimp.INT)
av1 = bimp.make_arg_var("av1", bimp.INT)
av2 = bimp.make_arg_var("av2", bimp.INT)
tmp = bimp.make_arg_var("tmp", bimp.INT)
inst1 = bimp.make_beq(v1, bimp.ZERO)
inst2 = bimp.make_beq(v2, bimp.ONE)
inst3 = bimp.make_beq(tmp, v1)
inst4 = bimp.make_beq(v1, v2)
inst5 = bimp.make_beq(v2, tmp)
inst6 = bimp.make_var_decl([tmp], [inst3, inst4, inst5])
inst7 = bimp.make_beq(v1, av1)
inst8 = bimp.make_beq(v2, av2)
inst9 = bimp.make_blk([inst7, inst8])
inst10 = bimp.make_beq(r1, v1)
inst11 = bimp.make_beq(r2, v2)
inst12 = bimp.make_blk([inst10, inst11])
step = bimp.make_oper("step", [], [], inst6)
set = bimp.make_oper("set", [av1, av2], [], inst9)
get = bimp.make_oper("get", [], [r1, r2], inst12)
imports = []
consts = []
vars = [v1, v2]
init = [inst1, inst2]
ops = [set, get, step]
root = bimp.make_implementation("swap_i", imports, consts, vars, init, ops)
