/* Monopoly
 * Author:  ???
 * Creation date: 12/16/13
 */
MACHINE
    Monopoly

SETS
    Icons = { ScottishTerrier,  Battleship, Automobile, Hat, Thimble,  Boot, Wheelbarrow, Cat }
    
DEFINITIONS
    IdPlayers == 1..7;
    Property == struct (  qt : INT, balance : NAT);
    Player == struct (  name : Icons, property : Property)
VARIABLES 
   currentPlayer, players 
   
INVARIANT
    currentPlayer : IdPlayers &
    players : IdPlayers -->> Player 
 
INITIALISATION 
    currentPlayer := 1 ||
    players := { 1 |-> rec( name : ScottishTerrier, property: rec( qt:0,balance:0)),
                 2 |-> rec( name : Battleship, property: rec( qt:0,balance:0)),
                 3 |-> rec( name : Automobile, property: rec( qt:0,balance:0)),
                 4 |-> rec( name : Hat, property: rec( qt:0,balance:0)),
                 5 |-> rec( name : Thimble, property: rec( qt:0,balance:0)),
                 6 |-> rec( name : Boot, property: rec( qt:0,balance:0)),
                 7 |-> rec( name : Wheelbarrow, property: rec( qt:0,balance:0)), 
                 8 |-> rec( name : Cat, property: rec( qt:0,balance:0))} 

OPERATIONS
    // This example has operations on structure: initialization, getting, setting, direct attribution ( ? ) 
    nextPlayer =
    BEGIN
        currentPlayer := ((currentPlayer+2 ) mod  7) -1
    END;
    
    // TODO: transfer between accounts 
    res <-- positive =
    LET player  BE player = players(currentPlayer) IN
        IF player'property'balance > 0 THEN
                res := TRUE
        ELSE 
                res := FALSE
        END        
    END;

    // Join accounts - 
    safe_withdraw(amt) = 
    PRE amt : NAT1 THEN
        LET player  BE player = players(currentPlayer) IN
                PRE amt : NAT1 & (player'property'balance >= amt) THEN
                  players(currentPlayer) := rec( name : player'name, property: rec( qt:0,balance:0))

                END
        END
    END

    /*  ;
    pay_taxes(amt) = 
    LET player  BE player = players(currentPlayer) IN
        PRE amt:NAT1 & (player'property'balance >= amt) THEN
            player'property'balance := player'property'balance - amt
        END
    END;
    
    receive_taxes(amt) =
    LET player  BE player = players(currentPlayer) IN
        PRE amt:NAT1 & (player'balance + amt < MAXINT) THEN
            player'balance := player'balance + amt
        END
    END;

    
    swap = 
    BEGIN
           tmp := yy
    END
    */  
    
    
END


