'''
This module provides string templates to form lines of LLVM source code.

The templates are properly indented.
'''

TB = "  "
NL = "\n"

ALLOC = TB + "{0} = alloca {1}" + NL
APPLY = TB + "{0} = {1} {2} {3}, {4}" + NL
CALL  = TB + "call void {0}({1})" + NL)
CGOTO = TB + "br i1 {0}, label %{1}, label %{2}" + NL)
COMM  = ";; {0}" + NL
FNDEC = "declare void {0}({1})"
FNDEF = "define void {0}({1}) {"
FNEND = "}" + NL
GLOBL = "{0} = common global {1} zeroinitializer" + NL
GOTO  = TB + "br label %{0}" + NL
ICOMP = TB + "{0} = icmp {1} {2}, {3}" + NL
LABEL = "{0}:" + NL
LOADD = TB + "{0} = load {1}* {2}" + NL
LOADI = TB + "{0} = getelementptr {1} {2}, i32 0, i32 {3}" + NL
OTYPE = "{0} = type opaque"
RET   = TB + "ret void" + NL
STORE = TB + "store {0} {1}, {0}* {2}" + NL
SWEND = TB + "]" + NL
SWEXP = TB + "switch {0} {1}, label %{2} [" + NL
SWVAL = 2*TB + "{0} {1}, label %{3}" + NL
TYPE = "{0} = type {{{1}}}" + NL
