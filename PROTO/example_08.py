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

# IMPLEMENTATION timer_i
# IMPORTS hh.counter, mm.counter, ss.counter

imp_hh = bimp.make_import(counter, "hh")
imp_mm = bimp.make_import(counter, "mm")
imp_ss = bimp.make_import(counter, "ss")
timer_imports = [imp_hh, imp_mm, imp_ss]
# VALUES capacity = (24 * 60 * 60) - 1
timeout = bimp.make_const("capacity", bimp.INT, bimp.make_intlit(24*60*60-1))
timer_consts = [timeout]
# CONCRETE_VARIABLES
#     is_running, overflow
is_running = bimp.make_imp_var("is_running", bimp.BOOL)
overflow = bimp.make_imp_var("overflow", bimp.BOOL)
timer_vars = [is_running, overflow]
# INITIALISATION
#     is_running := FALSE;
#     overflow := FALSE
inst7 = bimp.make_beq(is_running, bimp.FALSE)
inst8 = bimp.make_beq(overflow, bimp.FALSE)
timer_init = [inst7, inst8]
# OPERATIONS
#     tick =
#     IF ( is_running = TRUE ) & ( overflow = FALSE )
cond1 = bimp.make_and(bimp.make_eq(is_running, bimp.TRUE),
                      bimp.make_eq(overflow, bimp.FALSE))
#     THEN
#         VAR hours, minutes, seconds IN
hours = bimp.make_loc_var("hours", bimp.INT)
minutes = bimp.make_loc_var("minutes", bimp.INT)
seconds = bimp.make_loc_var("seconds", bimp.INT)
#             hours <-- hh.get;
#             minutes <-- mm.get;
#             seconds <-- ss.get;
inst9 = bimp.make_call(get, [], [hours], imp_hh)
inst10 = bimp.make_call(get, [], [minutes], imp_mm)
inst11 = bimp.make_call(get, [], [seconds], imp_ss)
#             IF (seconds < 59) THEN
fiftynine = bimp.make_intlit(59)
cond2 = bimp.make_lt(seconds, fiftynine)
#                 ss.inc
inst12 = bimp.make_call(inc, [], [], imp_ss)
if_br0 = bimp.make_if_br(cond2, inst12)
#             ELSE
#                 BEGIN
#                     ss.zero;
inst13 = bimp.make_call(zero, [], [], imp_ss)
#                     IF (minutes < 59) THEN
cond3 = bimp.make_lt(minutes, fiftynine)
#                         mm.inc
inst14 = bimp.make_call(inc, [], [], imp_mm)
if_br1 = bimp.make_if_br(cond3, inst14)
#                     ELSE
#                         BEGIN
#                             mm.zero;
#                             hh.inc
#                         END
inst15 = bimp.make_call(zero, [], [], imp_mm)
inst16 = bimp.make_call(inc, [], [], imp_hh)
inst17 = bimp.make_blk([inst15, inst16])
if_br2 = bimp.make_if_br(None, inst17)
#                     END
inst18 = bimp.make_if([if_br1, if_br2])
#                 END
inst19 = bimp.make_blk([inst13, inst18])
if_br3 = bimp.make_if_br(None, inst19)
#             END
inst20 = bimp.make_if([if_br0, if_br3])
#         END
inst21 = bimp.make_var_decl([hours, minutes, seconds],
                       [inst9, inst10, inst11, inst20])
#     END;
tick = bimp.make_oper("tick", [], [], inst21)
#     reset =
#     BEGIN
#         hh.zero;
#         mm.zero;
#         ss.zero;
#         overflow := FALSE
#     END;
inst22 = bimp.make_call(zero, [], [], imp_hh)
inst23 = bimp.make_call(zero, [], [], imp_mm)
inst24 = bimp.make_call(zero, [], [], imp_ss)
inst25 = bimp.make_blk([inst22, inst23, inst24])
reset = bimp.make_oper("reset", [], [], inst25)
#     stop =
#     IF ( is_running = TRUE)
#     THEN
#         is_running := FALSE
#     END;
cond4 = bimp.make_eq(is_running, bimp.TRUE)
inst26 = bimp.make_beq(is_running, bimp.FALSE)
inst27 = bimp.make_if([bimp.make_if_br(cond4, inst26)])
stop = bimp.make_oper("stop", [], [], inst27)
#     start =
#     IF ( is_running = FALSE )
#     THEN
#         is_running := TRUE
#     END;
cond5 = bimp.make_eq(is_running, bimp.FALSE)
inst28 = bimp.make_beq(is_running, bimp.TRUE)
start = bimp.make_oper("start", [], [], bimp.make_if([bimp.make_if_br(cond5, inst28)]))
#     hours , minutes , seconds <-- elapsed =
el_hours = bimp.make_arg_var("hours", bimp.INT)
el_minutes = bimp.make_arg_var("minutes", bimp.INT)
el_seconds = bimp.make_arg_var("seconds", bimp.INT)
#     BEGIN
#         IF ( overflow = TRUE )
cond6 = bimp.make_eq(overflow, bimp.TRUE)
#         THEN
#             hours := 0 ;
#             minutes := 0 ;
#             seconds := 0
inst29 = bimp.make_beq(el_hours, bimp.ZERO)
inst30 = bimp.make_beq(el_minutes, bimp.ZERO)
inst31 = bimp.make_beq(el_seconds, bimp.ZERO)
if_br4 = bimp.make_if_br(cond6, bimp.make_blk([inst29, inst30, inst31]))
#         ELSE
#             hours <-- hh.get;
#             minutes <-- mm.get;
#             seconds <-- ss.get
inst32 = bimp.make_call(get, [], [el_hours], imp_hh)
inst33 = bimp.make_call(get, [], [el_minutes], imp_mm)
inst34 = bimp.make_call(get, [], [el_seconds], imp_ss)
#         END
if_br5 = bimp.make_if_br(None, bimp.make_blk([inst32, inst33, inst34]))
inst35 = bimp.make_if([if_br4, if_br5])
inst36 = bimp.make_blk([inst35])
#     END;
elapsed = bimp.make_oper("elapsed", [], [el_hours, el_minutes, el_seconds], inst36)
#     answer <-- has_overflown =
#     answer := overflow
answer = bimp.make_arg_var("answer", bimp.BOOL)
inst37 = bimp.make_beq(answer, overflow)
has_overflown = bimp.make_oper("has_overflown", [], [answer], inst37)
# END

timer_ops = [tick, reset, start, stop, elapsed, has_overflown]
wd_i = bimp.make_implementation("wd_i", 
                                timer_imports, 
                                timer_consts, 
                                timer_vars, 
                                timer_init, 
                                timer_ops)
