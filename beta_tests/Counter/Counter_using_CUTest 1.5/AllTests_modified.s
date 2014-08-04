	.section	__TEXT,__text,regular,pure_instructions
	.globl	_Test_oper_inc_testCase1
	.align	4, 0x90
_Test_oper_inc_testCase1:               ## @Test_oper_inc_testCase1
	.cfi_startproc
## BB#0:
	pushq	%rbp
Ltmp3:
	.cfi_def_cfa_offset 16
Ltmp4:
	.cfi_offset %rbp, -16
	movq	%rsp, %rbp
Ltmp5:
	.cfi_def_cfa_register %rbp
	pushq	%rbx
	subq	$24, %rsp
Ltmp6:
	.cfi_offset %rbx, -24
	movq	%rdi, -16(%rbp)
	movq	_counter@GOTPCREL(%rip), %rbx
	movl	$0, (%rbx)
	movb	$0, 4(%rbx)
	movq	%rbx, %rdi
	callq	_counter$init$
	movq	%rbx, %rdi
	callq	_counter$inc
	movb	$1, %al
	testb	$1, 4(%rbx)
	je	LBB0_2
## BB#1:
	cmpl	$2147483647, (%rbx)     ## imm = 0x7FFFFFFF
	sete	%al
LBB0_2:
	movb	%al, -17(%rbp)
	movq	-16(%rbp), %rdi
	movzbl	%al, %r8d
	leaq	L_.str(%rip), %rsi
	leaq	L_.str1(%rip), %rcx
	movl	$23, %edx
	callq	_CuAssert_Line
	addq	$24, %rsp
	popq	%rbx
	popq	%rbp
	ret
	.cfi_endproc

	.globl	_Test_oper_inc_testCase2
	.align	4, 0x90
_Test_oper_inc_testCase2:               ## @Test_oper_inc_testCase2
	.cfi_startproc
## BB#0:
	pushq	%rbp
Ltmp10:
	.cfi_def_cfa_offset 16
Ltmp11:
	.cfi_offset %rbp, -16
	movq	%rsp, %rbp
Ltmp12:
	.cfi_def_cfa_register %rbp
	pushq	%rbx
	subq	$24, %rsp
Ltmp13:
	.cfi_offset %rbx, -24
	movq	%rdi, -16(%rbp)
	movq	_counter@GOTPCREL(%rip), %rbx
	movl	$3, (%rbx)
	movb	$1, 4(%rbx)
	movq	%rbx, %rdi
	callq	_counter$inc
	movb	$1, %al
	testb	$1, 4(%rbx)
	je	LBB1_2
## BB#1:
	cmpl	$2147483647, (%rbx)     ## imm = 0x7FFFFFFF
	sete	%al
LBB1_2:
	movb	%al, -17(%rbp)
	movq	-16(%rbp), %rdi
	movzbl	%al, %r8d
	leaq	L_.str(%rip), %rsi
	leaq	L_.str1(%rip), %rcx
	movl	$38, %edx
	callq	_CuAssert_Line
	addq	$24, %rsp
	popq	%rbx
	popq	%rbp
	ret
	.cfi_endproc

	.globl	_Test_oper_zero_testCase1
	.align	4, 0x90
_Test_oper_zero_testCase1:              ## @Test_oper_zero_testCase1
	.cfi_startproc
## BB#0:
	pushq	%rbp
Ltmp17:
	.cfi_def_cfa_offset 16
Ltmp18:
	.cfi_offset %rbp, -16
	movq	%rsp, %rbp
Ltmp19:
	.cfi_def_cfa_register %rbp
	pushq	%rbx
	subq	$24, %rsp
Ltmp20:
	.cfi_offset %rbx, -24
	movq	%rdi, -16(%rbp)
	movq	_counter@GOTPCREL(%rip), %rbx
	movl	$3, (%rbx)
	movb	$1, 4(%rbx)
	movq	%rbx, %rdi
	callq	_counter$zero
	movb	$1, %al
	testb	$1, 4(%rbx)
	je	LBB2_2
## BB#1:
	cmpl	$2147483647, (%rbx)     ## imm = 0x7FFFFFFF
	sete	%al
LBB2_2:
	movb	%al, -17(%rbp)
	movq	-16(%rbp), %rdi
	movzbl	%al, %r8d
	leaq	L_.str(%rip), %rsi
	leaq	L_.str1(%rip), %rcx
	movl	$52, %edx
	callq	_CuAssert_Line
	addq	$24, %rsp
	popq	%rbx
	popq	%rbp
	ret
	.cfi_endproc

	.globl	_testsSuite
	.align	4, 0x90
_testsSuite:                            ## @testsSuite
	.cfi_startproc
## BB#0:
	pushq	%rbp
Ltmp24:
	.cfi_def_cfa_offset 16
Ltmp25:
	.cfi_offset %rbp, -16
	movq	%rsp, %rbp
Ltmp26:
	.cfi_def_cfa_register %rbp
	pushq	%rbx
	pushq	%rax
Ltmp27:
	.cfi_offset %rbx, -24
	callq	_CuSuiteNew
	movq	%rax, %rbx
	movq	%rbx, -16(%rbp)
	leaq	L_.str2(%rip), %rdi
	leaq	_Test_oper_inc_testCase1(%rip), %rsi
	callq	_CuTestNew
	movq	%rbx, %rdi
	movq	%rax, %rsi
	callq	_CuSuiteAdd
	movq	-16(%rbp), %rbx
	leaq	L_.str3(%rip), %rdi
	leaq	_Test_oper_inc_testCase2(%rip), %rsi
	callq	_CuTestNew
	movq	%rbx, %rdi
	movq	%rax, %rsi
	callq	_CuSuiteAdd
	movq	-16(%rbp), %rbx
	leaq	L_.str4(%rip), %rdi
	leaq	_Test_oper_zero_testCase1(%rip), %rsi
	callq	_CuTestNew
	movq	%rbx, %rdi
	movq	%rax, %rsi
	callq	_CuSuiteAdd
	movq	-16(%rbp), %rax
	addq	$8, %rsp
	popq	%rbx
	popq	%rbp
	ret
	.cfi_endproc

	.globl	_RunAllTests
	.align	4, 0x90
_RunAllTests:                           ## @RunAllTests
	.cfi_startproc
## BB#0:
	pushq	%rbp
Ltmp31:
	.cfi_def_cfa_offset 16
Ltmp32:
	.cfi_offset %rbp, -16
	movq	%rsp, %rbp
Ltmp33:
	.cfi_def_cfa_register %rbp
	pushq	%rbx
	subq	$24, %rsp
Ltmp34:
	.cfi_offset %rbx, -24
	callq	_CuStringNew
	movq	%rax, -16(%rbp)
	callq	_CuSuiteNew
	movq	%rax, %rbx
	movq	%rbx, -24(%rbp)
	callq	_testsSuite
	movq	%rbx, %rdi
	movq	%rax, %rsi
	callq	_CuSuiteAddSuite
	movq	-24(%rbp), %rdi
	callq	_CuSuiteRun
	movq	-24(%rbp), %rdi
	movq	-16(%rbp), %rsi
	callq	_CuSuiteSummary
	movq	-24(%rbp), %rdi
	movq	-16(%rbp), %rsi
	callq	_CuSuiteDetails
	movq	-16(%rbp), %rax
	movq	8(%rax), %rsi
	leaq	L_.str5(%rip), %rdi
	xorl	%eax, %eax
	callq	_printf
	addq	$24, %rsp
	popq	%rbx
	popq	%rbp
	ret
	.cfi_endproc

	.globl	_main
	.align	4, 0x90
_main:                                  ## @main
	.cfi_startproc
## BB#0:
	pushq	%rbp
Ltmp37:
	.cfi_def_cfa_offset 16
Ltmp38:
	.cfi_offset %rbp, -16
	movq	%rsp, %rbp
Ltmp39:
	.cfi_def_cfa_register %rbp
	callq	_RunAllTests
	xorl	%eax, %eax
	popq	%rbp
	ret
	.cfi_endproc

	.comm	_counter,8,2            ## @counter
	.section	__TEXT,__cstring,cstring_literals
L_.str:                                 ## @.str
	.asciz	"AllTests.c"

L_.str1:                                ## @.str1
	.asciz	"Invariant invalid"

L_.str2:                                ## @.str2
	.asciz	"Test_oper_inc_testCase1"

L_.str3:                                ## @.str3
	.asciz	"Test_oper_inc_testCase2"

L_.str4:                                ## @.str4
	.asciz	"Test_oper_zero_testCase1"

L_.str5:                                ## @.str5
	.asciz	"%s\n"


.subsections_via_symbols
