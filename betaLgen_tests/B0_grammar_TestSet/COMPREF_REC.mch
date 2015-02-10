/* COMPIMP_INT
 * Author: 
 * Creation date: 1/21/15
 */
MACHINE
    COMPREF_REC (ID)

CONCRETE_VARIABLES var_rec 
INVARIANT var_rec : struct( aa : INT) 


INITIALISATION var_rec:= rec( aa : 1)
END