# IMPLEMENTATION
#    mult_i
# REFINES
#    mult
# CONCRETE_CONSTANTS
#    THR
# VALUES
#    THR = 2
# CONCRETE_VARIABLES
#    op1 ,
#    op2
# INVARIANT
#     op1: INT & op2: INT
# INITIALISATION
#    op1 := 0;
#    op2 := 0
# OPERATIONS
#    inc1 = op1 := succ(op1);
#    dec1 = op1 := pred(op1);
#    inc2 = op2 := succ(op2);
#    dec2 = op2 := pred(op2);
#    IF op1 > THR and op2 > THR THEN
#      res := TRUE
#    ELSE
#      res := FALSE
#    END;
#    res <-- some =
#    IF op1 > THR or op2 > THR THEN
#      res := TRUE
#    ELSE
#      res := FALSE
#    END;
#    res <-- none =
#    IF not(op1 > THR) and not (op2 > THR) THEN
#      res := TRUE
#    ELSE
#      res := FALSE
#    END
# END

from bimp import *

THR = make_const("THR", INT, make_intlit(2))

op1 = make_imp_var("op1", INT)
op2 = make_imp_var("op2", INT)
val = make_imp_var("val", BOOL)

inst1 = make_beq(op1, zero)
inst2 = make_beq(op2, zero)

term1 = make_succ(op1)
inst3 = make_beq(op1, term1)

inc1 = make_oper("inc1", [], [], inst3)

term2 = make_pred(op1)
inst4 = make_beq(op1, term2)

dec1 = make_oper("dec1", [], [], inst4)

term3 = make_succ(op2)
inst5 = make_beq(op2, term3)

inc2 = make_oper("inc2", [], [], inst5)

term4 = make_pred(op2)
inst6 = make_beq(op2, term4)

dec2 = make_oper("dec2", [], [], inst6)

cond1 = make_gt(op1, THR)
cond2 = make_gt(op2, THR)
form1 = make_and(cond1, cond2)
form2 = make_or(cond1, cond2)
form3 = make_and(make_not(cond1), make_not(cond2))
inst7 = make_beq(val, true)
inst8 = make_beq(val, false)
ifbr1 = make_if_br(form1, inst7)
ifbr2 = make_if_br(None, inst8)
if1 = make_if([ifbr1, ifbr2])
both = make_oper("both", [], [], if1)
ifbr3 = make_if_br(form2, inst7)
if2 = make_if([ifbr3, ifbr2])
some = make_oper("some", [], [], if2)
ifbr4 = make_if_br(form3, inst7)
if3 = make_if([ifbr4, ifbr2])
none = make_oper("none", [], [], if3)
vars = [op1, op2, val]
consts = [THR]
init = [inst1, inst2]
ops = [inc1, dec1, inc2, dec2, both, some, none]
root = make_implementation("cond_i", vars, consts, init, ops)
