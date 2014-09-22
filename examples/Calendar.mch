/* Calendar
 * Author: 
 * Creation date: 11/09/14
 */
MACHINE
    Calendar

VARIABLES
    mm
INVARIANT
    mm : INT
INITIALISATION
    mm :=1

OPERATIONS
    month(nn) = 
    PRE
        nn : 1..12
    THEN
        CASE nn OF
            EITHER 1 THEN
                mm := 1
            OR 2 THEN
                mm := 2
            OR 3 THEN
                mm := 3
            OR 4 THEN
                mm := 4
            OR 5 THEN
                mm := 5
            OR 6 THEN
                mm := 6
            OR 7 THEN
                mm := 7
            OR 8 THEN
                mm := 8
            OR 9 THEN
                mm := 9
            OR 10 THEN
                mm := 10
            OR 11 THEN
                mm := 11
            OR 12 THEN
                mm := 12
            END
       END
    END
 
END
