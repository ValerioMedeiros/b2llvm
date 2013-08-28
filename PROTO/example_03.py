# IMPLEMENTATION
#    swap_i
# REFINES
#    swap
# CONCRETE_VARIABLES
#    v1 ,  v2
# INVARIANT
#     v1 : INT & v2 : INT
# INITIALISATION
#    v1 := 0; v2 := 1
# OPERATIONS
#    step =
#    VAR tmp IN
#        BEGIN
#            tmp := v1;
#            v1 := v2;
#            v2 := tmp
#        END
#    END;
#    set ( av1 , av2 ) =
#    BEGIN
#        v1 := av1;
#        v2 := av2
#    END
#    ;
#    r1 , r2 <-- get =
#    BEGIN
#        r1 := v1;
#        r2 := v2
#    END
# END

v1 = { "kind": "Vari",
       "id":"v1",
       "type": "INT",
       "scope": "Impl" }

v2 = { "kind": "Vari",
       "id":"v2",
       "type": "INT",
       "scope": "Impl" }

ilit0 = { "kind": "IntegerLit",
          "value": "0"}

ilit1 = { "kind": "IntegerLit",
          "value": "1"}

r1 = { "kind": "Vari",
       "id": "r1",
       "type": "INT",
       "scope": "Oper" }

r2 = { "kind": "Vari",
       "id": "r2",
       "type": "INT",
       "scope": "Oper" }

av1 = { "kind": "Vari",
        "id":"av1",
        "type": "INT",
        "scope": "Oper" }

av2 = { "kind": "Vari",
        "id":"av2",
        "type": "INT",
        "scope": "Oper" }

tmp = { "kind": "Vari",
        "id":"tmp",
        "type": "INT",
        "scope": "Local" }


inst1 = { "kind": "Beq",
          "lhs": v1,
          "rhs": ilit0}

inst2 = { "kind": "Beq",
          "lhs": v2,
          "rhs": ilit1}

inst3 = { "kind": "Beq",
          "lhs": tmp,
          "rhs": v1}

inst4 = { "kind": "Beq",
          "lhs": v1,
          "rhs": v2}

inst5 = { "kind": "Beq",
          "lhs": v2,
          "rhs": tmp}

inst6 = { "kind": "VarD",
          "vars": [tmp],
          "body": [inst3, inst4, inst5] }

inst7 = { "kind": "Beq",
          "lhs": v1,
          "rhs": av1 }

inst8 = { "kind": "Beq",
          "lhs": v2,
          "rhs": av2 }

inst9 = { "kind": "Blk",
          "body": [inst7, inst8] }

inst10 = { "kind": "Beq",
           "lhs": r1,
           "rhs": v1 }

inst11 = { "kind": "Beq",
           "lhs": r2,
           "rhs": v2 }

inst12 = { "kind": "Blk",
          "body": [inst10, inst11] }

step = { "kind": "Oper",
         "id": "step",
         "inp": [],
         "out": [],
         "body": inst6 }

set = { "kind": "Oper",
        "id": "set",
        "inp": [av1, av2],
        "out": [],
        "body":  inst9 }

get = { "kind": "Oper",
        "id": "get",
        "inp": [],
        "out": [r1, r2],
        "body": inst12 }

root = { "kind": "Impl",
         "id": "swap_i",
         "concrete_variables": [ v1, v2 ],
         "initialisation": [ inst1, inst2 ],
         "operations": [ set, get, step ] }

for n in [v1, v2, step, set, get]:
    n["root"] = root
