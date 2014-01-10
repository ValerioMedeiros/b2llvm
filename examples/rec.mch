/* Author: ??? */
MACHINE Rec
SETS
 ID={aa,bb}
VARIABLES xx, bank, total
INVARIANT
 xx : struct(name : ID, balance : NAT) & bank : struct(name : ID) & total:struct(money:NAT)
INITIALISATION bank := rec(name:bb) || xx:= rec(name:aa, balance:10) || total := rec(money:20)
OPERATIONS

  res<--positive = PRE xx'balance > 0 THEN res:=TRUE END;

  withrdaw(amt) = PRE amt:NAT1 & (xx'balance >= amt) THEN
     xx := rec(name:xx'name, balance:(xx'balance - amt))
  END;
  
  unsafe_dec = BEGIN
       xx'balance := xx'balance - 1
  END
END

