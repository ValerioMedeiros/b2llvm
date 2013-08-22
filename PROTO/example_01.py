value = { "kind": "Vari",
          "id":"value",
          "type": "INT",
          "scope": "Impl" }

error = { "kind": "Vari",
          "id":"error",
          "type": "BOOL",
          "scope": "Impl" }

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

comp1 = { "kind": "Comp",
          "op": "<",
          "arg1": value,
          "arg2": max_int }

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

dec = {}
valid = {}
get = {}
set = {}

counter_i = { "kind": "Impl",
              "id": "counter_i",
              "concrete_variables": [ value, error ],
              "initialisation": [ inst1, inst2 ],
              "operations": [ zero, inc ] }

for n in [value, error, zero, inc]:
    n["root"] = counter_i
