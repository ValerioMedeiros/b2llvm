/* COMPIMP_REC
 * Author: 
 * Creation date: 2/3/15
 
MACHINE COMPSEES ( ID ) END
*/

 
MACHINE
    COMPSEES ( ID )

CONCRETE_VARIABLES
 	local_var_rec 
INVARIANT local_var_rec : struct( aa : INT)
INITIALISATION 
local_var_rec:= rec( aa : 1) 

END
