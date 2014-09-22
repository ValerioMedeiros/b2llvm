MACHINE
   array
VARIABLES arr, arr2d

INVARIANT 
    arr : ((0..99) --> 0..1000) &
    arr2d : ((0..99) * (0..99) --> 0..1000) 

INITIALISATION 
    arr :: ((0..99) --> 0..1000)||
    arr2d := (0..99) * (0..99) * {0}

OPERATIONS 

set(ix,tt)=
        PRE ix : (0..99) & tt : (0..1000)
        THEN arr := arr <+ {ix |-> tt}
        END;

tt <-- read(ix) =
        PRE ix : (0..99)
        THEN tt := arr(ix)
        END;

swap(ix, jx)=
        PRE ix : (0..99) & jx : (0..99)
        THEN arr := arr <+ {ix |-> arr(jx), jx|-> arr(ix)}
        END;
        
set3(ix1,ix2,tt)=
        PRE ix1 : (0..99) & ix2 : (0..99) & tt : (0..1000)
        THEN arr2d := arr2d <+ {( ix1,ix2) |-> tt}
        END;

tt <-- read3(ix1,ix2) =
        PRE ix1 : (0..99) & ix2 : (0..99)
        THEN tt := arr2d(ix1,ix2)
        END;

swap3(ix1,ix2, ij1,ij2)=
        PRE ix1 : (0..99) & ix2 : (0..99) & ij1 : (0..99) & ij2 : (0..99)
        THEN arr2d := arr2d <+ {(ix1,ix2) |-> arr2d(ij1,ij2), (ij1,ij2)|-> arr2d(ix1,ix2)}
        END


END
