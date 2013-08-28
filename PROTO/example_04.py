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

from bimp import *

op1 = make_imp_var("op1", INT)
op2 = make_imp_var("op2", INT)
res = make_imp_var("res", INT)
ok = make_imp_var("ok", BOOL)

inst1 = make_beq(op1, zero)
inst2 = make_beq(op2, zero)
inst3 = make_beq(res, zero)
inst4 = make_beq(ok, true)

term1 = make_succ(op1)
inst5 = make_beq(op1, term1)
inst6 = make_beq(ok, false)
inst7 = make_blk([inst5, inst6])

inc1 = make_oper("inc1", [], [], inst7)

term2 = make_pred(op1)
inst8 = make_beq(op1, term2)
inst9 = make_blk([inst8, inst6])

dec1 = make_oper("dec1", [], [], inst9)

term3 = make_succ(op2)
inst10 = make_beq(op2, term3)
inst11 = make_blk([inst10, inst6])

inc2 = make_oper("inc2", [], [], inst11)

term4 = make_pred(op2)
inst12 = make_beq(op2, term4)
inst13 = make_blk([inst12, inst6])

dec2 = make_oper("dec2", [], [], inst13)

acc = make_loc_var("acc", INT)
idx = make_loc_var("idx", INT)
inst14 = make_beq(acc, zero)
inst15 = make_beq(idx, zero)
inst16 = make_beq(idx, make_succ(idx))
inst17 = make_beq(acc, make_sum(acc, op1))
cond1 = make_lt(idx, op2)
inst18 = make_while(cond1, [inst16, inst17])
inst19 = make_beq(res, acc)
inst20 = make_beq(ok, true)
inst21 = make_var_decl([acc, idx],[inst14, inst15, inst18, inst19, inst20])
calc = make_oper("calc", [], [], inst21)

vars = [op1, op2, res, ok]
init = [inst1, inst2, inst3, inst4]
ops = [inc1, dec1, inc2, dec2, calc]
root = make_implementation("mult_i", vars, [], init, ops)
