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

import bimp

THR = bimp.make_const("THR", bimp.INT, bimp.make_intlit(2))

op1 = bimp.make_imp_var("op1", bimp.INT)
op2 = bimp.make_imp_var("op2", bimp.INT)
val = bimp.make_imp_var("val", bimp.BOOL)

inst1 = bimp.make_beq(op1, bimp.ZERO)
inst2 = bimp.make_beq(op2, bimp.ZERO)

term1 = bimp.make_succ(op1)
inst3 = bimp.make_beq(op1, term1)

inc1 = bimp.make_oper("inc1", [], [], inst3)

term2 = bimp.make_pred(op1)
inst4 = bimp.make_beq(op1, term2)

dec1 = bimp.make_oper("dec1", [], [], inst4)

term3 = bimp.make_succ(op2)
inst5 = bimp.make_beq(op2, term3)

inc2 = bimp.make_oper("inc2", [], [], inst5)

term4 = bimp.make_pred(op2)
inst6 = bimp.make_beq(op2, term4)

dec2 = bimp.make_oper("dec2", [], [], inst6)

cond1 = bimp.make_gt(op1, THR)
cond2 = bimp.make_gt(op2, THR)
form1 = bimp.make_and(cond1, cond2)
form2 = bimp.make_or(cond1, cond2)
form3 = bimp.make_and(bimp.make_not(cond1), bimp.make_not(cond2))
inst7 = bimp.make_beq(val, bimp.TRUE)
inst8 = bimp.make_beq(val, bimp.FALSE)
ifbr1 = bimp.make_if_br(form1, inst7)
ifbr2 = bimp.make_if_br(None, inst8)
if1 = bimp.make_if([ifbr1, ifbr2])
both = bimp.make_oper("both", [], [], if1)
ifbr3 = bimp.make_if_br(form2, inst7)
if2 = bimp.make_if([ifbr3, ifbr2])
some = bimp.make_oper("some", [], [], if2)
ifbr4 = bimp.make_if_br(form3, inst7)
if3 = bimp.make_if([ifbr4, ifbr2])
none = bimp.make_oper("none", [], [], if3)
imports = []
consts = [THR]
vars = [op1, op2, val]
init = [inst1, inst2]
ops = [inc1, dec1, inc2, dec2, both, some, none]
root = bimp.make_implementation("cond_i", [], consts, vars, init, ops)
