
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

value = { "kind": "Vari",
          "id":"value",
          "type": "INT",
          "scope": "Impl" }

error = { "kind": "Vari",
          "id":"error",
          "type": "BOOL",
          "scope": "Impl" }

ilit1 = { "kind": "IntegerLit",
          "value": "3"}

max = { "kind": "Cons",
        "id": "MAX",
        "type": "INT",
        "value" : ilit1 }

res = { "kind": "Vari",
        "id": "res",
        "type": "BOOL",
        "scope": "Oper" }

res2 = { "kind": "Vari",
        "id": "res",
        "type": "INT",
        "scope": "Oper" }

avalue = { "kind": "Vari",
           "id":"avalue",
           "type": "INT",
           "scope": "Oper" }

zero = { "kind": "IntegerLit",
          "value": "0"}

false = { "kind": "BooleanLit",
          "value": "FALSE"}

one = { "kind": "IntegerLit",
          "value": "1"}

true = { "kind": "BooleanLit",
          "value": "TRUE"}

term1 = { "kind": "Term",
          "op": "succ",
          "args" : [value] }

term2 = { "kind": "Term",
          "op": "pred",
          "args" : [value] }

comp1 = { "kind": "Comp",
          "op": "<",
          "arg1": value,
          "arg2": max }

comp2 = { "kind": "Comp",
          "op": "<",
          "arg1": zero,
          "arg2": value }

inst1 = { "kind": "Beq",
          "lhs": value,
          "rhs": zero}

inst2 = { "kind": "Beq",
          "lhs": error,
          "rhs": false}

inst3 = { "kind": "Blk",
          "body": [inst1, inst2] }

inst4 = { "kind": "Beq",
          "lhs": value,
          "rhs": term1}

inst5 = { "kind": "Beq",
          "lhs": error,
          "rhs": true}

branch1 = { "kind": "IfBr",
            "cond": comp1,
            "body": inst4 }

branch2 = { "kind": "IfBr",
            "body": inst5 }

inst6 = { "kind": "If",
          "branches": [branch1, branch2]}

inst7 = { "kind": "Beq",
          "lhs": value,
          "rhs": term2}

branch3 = { "kind": "IfBr",
            "cond": comp2,
            "body": inst7 }

branch4 = { "kind": "IfBr",
            "body": inst5 }

zero = { "kind": "Oper",
         "id": "zero",
         "inp": [],
         "out": [],
         "body": inst3 }

inc = { "kind": "Oper",
        "id": "inc",
        "inp": [],
        "out": [],
        "body": inst6 }

inst8 = { "kind": "If",
          "branches": [branch3, branch4]}

dec = { "kind": "Oper",
        "id": "dec",
        "inp": [],
        "out": [],
        "body": inst8 }

root = { "kind": "Impl",
         "id": "counter_i",
         "concrete_constants": [ max ],
         "concrete_variables": [ value, error ],
         "initialisation": [ inst1, inst2 ],
         "operations": [ zero, inc, dec ] }

for n in [value, error, zero, max, inc, dec]:
    n["root"] = root
