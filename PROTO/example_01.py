value = { "kind": "Vari",
          "id":"value",
          "type": "INT",
          "scope": "Impl" }

error = { "kind": "Vari",
          "id":"error",
          "type": "BOOL",
          "scope": "Impl" }

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

max_int = { "kind": "IntegerLit",
          "value": "2147483647"}

one = { "kind": "IntegerLit",
          "value": "1"}

true = { "kind": "BooleanLit",
          "value": "TRUE"}

term1 = { "kind": "Term",
          "op": "+",
          "args" : [value, one] }

term2 = { "kind": "Term",
          "op": "-",
          "args" : [value, one] }

comp1 = { "kind": "Comp",
          "op": "<",
          "arg1": value,
          "arg2": max_int }

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

inst8 = { "kind": "If",
          "branches": [branch3, branch4]}

inst9 = { "kind": "Beq",
          "lhs": res,
          "rhs": false }

inst10 = { "kind": "Beq",
           "lhs": res,
           "rhs": true }

comp3 = { "kind": "Comp",
          "op": "=",
          "arg1": error,
          "arg2": true }

branch5 = { "kind": "IfBr",
            "cond": comp3,
            "body": inst9 }

branch6 = { "kind": "IfBr",
            "body": inst10 }

inst11 = { "kind": "If",
           "branches": [branch5, branch6] }

inst12 = { "kind": "Blk",
           "body": [inst11] }

inst13 = { "kind": "Beq",
           "lhs": res2,
           "rhs": value }

inst14 = { "kind": "Beq",
           "lhs": value,
           "rhs": avalue }

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

dec = { "kind": "Oper",
        "id": "dec",
        "inp": [],
        "out": [],
        "body": inst8 }

valid = { "kind": "Oper",
          "id": "valid",
          "inp": [],
          "out": [res],
          "body": inst12 }

get = { "kind": "Oper",
        "id": "get",
        "inp": [],
        "out": [res2],
        "body": inst13 }

set = { "kind": "Oper",
        "id": "set",
        "inp": [avalue],
        "out": [],
        "body": inst14 }

counter_i = { "kind": "Impl",
              "id": "counter_i",
              "concrete_variables": [ value, error ],
              "initialisation": [ inst1, inst2 ],
              "operations": [ zero, inc, dec, valid, get, set ] }

for n in [value, error, zero, res, res2, avalue, inc, dec, valid, get, set]:
    n["root"] = counter_i
