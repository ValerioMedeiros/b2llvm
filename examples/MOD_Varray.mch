/* Varray
 * Author: 
 * Creation date: 20/09/14
 */
MACHINE
    MOD_Varray
CONSTANTS
    cap
PROPERTIES
    cap : NAT1
VARIABLES
    array
INVARIANT
    array : 0..cap --> INT
INITIALISATION
    array :: 0..cap --> INT
OPERATIONS
    set(ii, vv) = 
    PRE
        ii : 0..cap & vv : INT
    THEN
        array(ii) := vv
    END;
    vv <-- get(ii) = 
    PRE
        ii : 0..cap
    THEN
        vv := array(ii)
    END
END
