from strutils import nl, sp, tb

INDENT = 0
ACTIVE = False

def INI(activate):
    global ACTIVE
    ACTIVE = activate

def OUT(out, msg):
    global tb, nl, INDENT, ACTIVE
    if ACTIVE:
        out.extend(bytearray(";;"+INDENT*tb+sp+msg+nl))

def TAB():
    global INDENT, ACTIVE
    if ACTIVE:
        INDENT += 1

def UNTAB():
    global INDENT, ACTIVE
    if ACTIVE:
        INDENT -= 1

