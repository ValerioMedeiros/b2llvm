import math
from strutils import nl, sp, tb

INDENT = 0
ACTIVE = False
INDEX = [0]

def nb_digits(n):
    if n == 0:
        return 1
    else:
        return int(math.floor(math.log(n, 10))+1)

def INI(activate):
    global ACTIVE
    ACTIVE = activate

def OUTU(out, msg):
    global tb, nl, INDENT, ACTIVE
    if ACTIVE:
        out.extend(bytearray(";;"+sp+" ".join([nb_digits(i)*sp for i in INDEX])+sp+msg+nl))
        # out.extend(bytearray(";;"+INDENT*tb+sp+msg+nl))

def OUT(out, msg):
    global tb, nl, INDENT, ACTIVE
    if ACTIVE:
        last = INDEX.pop()
        INDEX.append(last+1)
        out.extend(bytearray(";;"+sp+".".join([str(i) for i in INDEX])+sp+msg+nl))
        # out.extend(bytearray(";;"+INDENT*tb+sp+msg+nl))

def TAB():
    global INDENT, ACTIVE
    if ACTIVE:
        INDEX.append(0)
        # INDENT += 1

def UNTAB():
    global INDENT, ACTIVE
    if ACTIVE:
        # INDENT -= 1
        INDEX.pop()

