/* mult
 * Author: 
 * Creation date: 8/28/13
 */
MACHINE
    mult
VARIABLES
    op1, op2, res, ok
INVARIANT
    op1: INT & op2: INT & res: INT & ok: BOOL &
    op1: 0..100 & op2: 0..100 &
    ((ok = TRUE) => (res = op1*op2))
INITIALISATION
    op1 := 0 || op2 := 0 || res := 0 || ok := TRUE
OPERATIONS
    inc1 =
    PRE op1 < 100 THEN
        op1 := op1 + 1 || ok := FALSE
    END;
    dec1 = 
    PRE op1 > 0 THEN
        op1 := op1 - 1 || ok := FALSE
    END;
    inc2 =
    PRE op2 < 100 THEN
        op2 := op2 + 1 || ok := FALSE
    END;
    dec2 =
    PRE op2 > 0 THEN
        op2 := op2 - 1 || ok := FALSE
    END;
    calc = res, ok := op1*op2, TRUE
END
