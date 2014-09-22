
MACHINE
    ArraySwap
VARIABLES
   mvector
INVARIANT
   mvector : 0..1 --> 2..3
INITIALISATION
   mvector := { 0|-> 2, 1|->3} 
   
OPERATIONS

   swap =
   BEGIN
   mvector := { 0|->mvector(1),
               1|->mvector(0)}
   END
   
   
END
