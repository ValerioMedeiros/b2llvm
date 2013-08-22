value = { "kind": "Vari",
          "id":"value",
          "type": "INT",
          "scope": "Impl" }

error = { "kind": "Vari",
          "id":"error",
          "type": "BOOL",
          "scope": "Impl" }

expr1 = { "kind": "IntegerLit",
          "value": "0"}

inst1 = { "kind": "Beq",
          "lhs": value,
          "rhs": expr1}

expr2 = { "kind": "BooleanLit",
          "value": "FALSE"}

inst2 = { "kind": "Beq",
          "lhs": error,
          "rhs": expr2}

zero = {}
inc = {}
dec = {}
valid = {}
get = {}
set = {}

counter_i = { "kind": "Impl",
              "id": "counter_i",
              "concrete_variables": [ value, error ],
              "initialisation": [ inst1, inst2 ],
              "operations": [ zero, inc, dec, valid, get, set ] }

value["root"] = counter_i
error["root"] = counter_i
