# IMPLEMENTATION
#    mult_i
# REFINES
#    mult
# CONCRETE_VARIABLES
#    op1 , op2 , res , ok
# INVARIANT
#     op1: INT & op2: INT & res: INT & ok: BOOL
# INITIALISATION
#    op1 := 0;
#    op2 := 0;
#    res := 0;
#    ok := TRUE
# OPERATIONS
#    inc1 =
#    BEGIN
#        op1 := succ(op1);
#        ok := FALSE
#    END;
#    dec1 =
#    BEGIN
#        op1 := pred(op1);
#        ok := FALSE
#    END;
#    inc2 =
#    BEGIN
#        op2 := succ(op2);
#        ok := FALSE
#    END;
#    dec2 =
#    BEGIN
#        op2 := pred(op2);
#        ok := FALSE
#    END;
#    calc =
#    VAR acc, idx IN
#        acc := 0;
#        idx := 0;
#        WHILE idx < op2 DO
#            idx := succ(idx);
#            acc := acc + op1
#        INVARIANT
#            idx: 0..op2 &
#            acc = op1 * idx
#        VARIANT
#            op2 - idx
#        END;
#        res := acc;
#        ok := TRUE
#    END
# END

import bimp

op1 = bimp.make_imp_var("op1", bimp.INT)
op2 = bimp.make_imp_var("op2", bimp.INT)
res = bimp.make_imp_var("res", bimp.INT)
ok = bimp.make_imp_var("ok", bimp.BOOL)

inst1 = bimp.make_beq(op1, bimp.ZERO)
inst2 = bimp.make_beq(op2, bimp.ZERO)
inst3 = bimp.make_beq(res, bimp.ZERO)
inst4 = bimp.make_beq(ok, bimp.TRUE)

term1 = bimp.make_succ(op1)
inst5 = bimp.make_beq(op1, term1)
inst6 = bimp.make_beq(ok, bimp.FALSE)
inst7 = bimp.make_blk([inst5, inst6])

inc1 = bimp.make_oper("inc1", [], [], inst7)

term2 = bimp.make_pred(op1)
inst8 = bimp.make_beq(op1, term2)
inst9 = bimp.make_blk([inst8, inst6])

dec1 = bimp.make_oper("dec1", [], [], inst9)

term3 = bimp.make_succ(op2)
inst10 = bimp.make_beq(op2, term3)
inst11 = bimp.make_blk([inst10, inst6])

inc2 = bimp.make_oper("inc2", [], [], inst11)

term4 = bimp.make_pred(op2)
inst12 = bimp.make_beq(op2, term4)
inst13 = bimp.make_blk([inst12, inst6])

dec2 = bimp.make_oper("dec2", [], [], inst13)

acc = bimp.make_loc_var("acc", bimp.INT)
idx = bimp.make_loc_var("idx", bimp.INT)
inst14 = bimp.make_beq(acc, bimp.ZERO)
inst15 = bimp.make_beq(idx, bimp.ZERO)
inst16 = bimp.make_beq(idx, bimp.make_succ(idx))
inst17 = bimp.make_beq(acc, bimp.make_sum(acc, op1))
cond1 = bimp.make_lt(idx, op2)
inst18 = bimp.make_while(cond1, [inst16, inst17])
inst19 = bimp.make_beq(res, acc)
inst20 = bimp.make_beq(ok, bimp.TRUE)
inst21 = bimp.make_var_decl([acc, idx],[inst14, inst15, inst18, inst19, inst20])
calc = bimp.make_oper("calc", [], [], inst21)

imports = []
consts = []
vars = [op1, op2, res, ok]
init = [inst1, inst2, inst3, inst4]
ops = [inc1, dec1, inc2, dec2, calc]
root = bimp.make_implementation("mult_i", imports, consts, vars, init, ops)
