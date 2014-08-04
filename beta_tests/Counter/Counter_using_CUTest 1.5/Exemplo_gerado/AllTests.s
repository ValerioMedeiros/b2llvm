	.section	__TEXT,__text,regular,pure_instructions
	.globl	_check_invariant
	.align	4, 0x90
_check_invariant:                       ## @check_invariant
	.cfi_startproc
## BB#0:
	pushq	%rbp
Ltmp2:
	.cfi_def_cfa_offset 16
Ltmp3:
	.cfi_offset %rbp, -16
	movq	%rsp, %rbp
Ltmp4:
	.cfi_def_cfa_register %rbp
	subq	$16, %rsp
	movq	%rdi, -8(%rbp)
	movq	%rsi, -16(%rbp)
	testb	$1, -12(%rbp)
	je	LBB0_3
## BB#1:
	cmpl	$2147483647, -16(%rbp)  ## imm = 0x7FFFFFFF
	je	LBB0_3
## BB#2:
	movq	-8(%rbp), %rdi
	leaq	L_.str(%rip), %rsi
	leaq	L_.str1(%rip), %r8
	movl	$12, %edx
	xorl	%ecx, %ecx
	callq	_CuFail_Line
LBB0_3:
	cmpl	$0, -16(%rbp)
	jns	LBB0_5
## BB#4:
	movq	-8(%rbp), %rdi
	leaq	L_.str(%rip), %rsi
	leaq	L_.str2(%rip), %r8
	movl	$16, %edx
	xorl	%ecx, %ecx
	callq	_CuFail_Line
LBB0_5:
	movb	$1, %al
	testb	%al, %al
	jne	LBB0_7
## BB#6:
	movq	-8(%rbp), %rdi
	leaq	L_.str(%rip), %rsi
	leaq	L_.str3(%rip), %r8
	movl	$20, %edx
	xorl	%ecx, %ecx
	callq	_CuFail_Line
LBB0_7:
	addq	$16, %rsp
	popq	%rbp
	ret
	.cfi_endproc

	.globl	_counter_inc_test_case_1
	.align	4, 0x90
_counter_inc_test_case_1:               ## @counter_inc_test_case_1
	.cfi_startproc
## BB#0:
	pushq	%rbp
Ltmp8:
	.cfi_def_cfa_offset 16
Ltmp9:
	.cfi_offset %rbp, -16
	movq	%rsp, %rbp
Ltmp10:
	.cfi_def_cfa_register %rbp
	pushq	%r15
	pushq	%r14
	pushq	%rbx
	subq	$24, %rsp
Ltmp11:
	.cfi_offset %rbx, -40
Ltmp12:
	.cfi_offset %r14, -32
Ltmp13:
	.cfi_offset %r15, -24
	movq	%rdi, -32(%rbp)
	movb	$0, -33(%rbp)
	movq	_counter@GOTPCREL(%rip), %rbx
	movb	$0, 4(%rbx)
	movl	$0, -40(%rbp)
	movl	$0, (%rbx)
	movq	%rbx, %rdi
	callq	_counter$inc
	movq	-32(%rbp), %rdi
	movb	4(%rbx), %al
	notb	%al
	movzbl	%al, %r8d
	andl	$1, %r8d
	leaq	L_.str(%rip), %r14
	leaq	L_.str4(%rip), %r15
	movl	$44, %edx
	movq	%r14, %rsi
	movq	%r15, %rcx
	callq	_CuAssert_Line
	movq	-32(%rbp), %rdi
	cmpl	$1, (%rbx)
	sete	%al
	movzbl	%al, %r8d
	movl	$47, %edx
	movq	%r14, %rsi
	movq	%r15, %rcx
	callq	_CuAssert_Line
	movq	-32(%rbp), %rdi
	movq	(%rbx), %rsi
	callq	_check_invariant
	addq	$24, %rsp
	popq	%rbx
	popq	%r14
	popq	%r15
	popq	%rbp
	ret
	.cfi_endproc

	.globl	_counter_inc_test_case_2
	.align	4, 0x90
_counter_inc_test_case_2:               ## @counter_inc_test_case_2
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
	pushq	%r15
	pushq	%r14
	pushq	%rbx
	subq	$24, %rsp
Ltmp20:
	.cfi_offset %rbx, -40
Ltmp21:
	.cfi_offset %r14, -32
Ltmp22:
	.cfi_offset %r15, -24
	movq	%rdi, -32(%rbp)
	movb	$1, -33(%rbp)
	movq	_counter@GOTPCREL(%rip), %rbx
	movb	$1, 4(%rbx)
	movl	$2147483647, -40(%rbp)  ## imm = 0x7FFFFFFF
	movl	$2147483647, (%rbx)     ## imm = 0x7FFFFFFF
	movq	%rbx, %rdi
	callq	_counter$inc
	movq	-32(%rbp), %rdi
	movzbl	4(%rbx), %r8d
	andl	$1, %r8d
	leaq	L_.str(%rip), %r14
	leaq	L_.str4(%rip), %r15
	movl	$70, %edx
	movq	%r14, %rsi
	movq	%r15, %rcx
	callq	_CuAssert_Line
	movq	-32(%rbp), %rdi
	cmpl	$2147483647, (%rbx)     ## imm = 0x7FFFFFFF
	sete	%al
	movzbl	%al, %r8d
	movl	$73, %edx
	movq	%r14, %rsi
	movq	%r15, %rcx
	callq	_CuAssert_Line
	movq	-32(%rbp), %rdi
	movq	(%rbx), %rsi
	callq	_check_invariant
	addq	$24, %rsp
	popq	%rbx
	popq	%r14
	popq	%r15
	popq	%rbp
	ret
	.cfi_endproc

	.globl	_counter_inc_test_suite
	.align	4, 0x90
_counter_inc_test_suite:                ## @counter_inc_test_suite
	.cfi_startproc
## BB#0:
	pushq	%rbp
Ltmp26:
	.cfi_def_cfa_offset 16
Ltmp27:
	.cfi_offset %rbp, -16
	movq	%rsp, %rbp
Ltmp28:
	.cfi_def_cfa_register %rbp
	pushq	%rbx
	pushq	%rax
Ltmp29:
	.cfi_offset %rbx, -24
	callq	_CuSuiteNew
	movq	%rax, %rbx
	movq	%rbx, -16(%rbp)
	leaq	L_.str5(%rip), %rdi
	leaq	_counter_inc_test_case_1(%rip), %rsi
	callq	_CuTestNew
	movq	%rbx, %rdi
	movq	%rax, %rsi
	callq	_CuSuiteAdd
	movq	-16(%rbp), %rbx
	leaq	L_.str6(%rip), %rdi
	leaq	_counter_inc_test_case_2(%rip), %rsi
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
Ltmp33:
	.cfi_def_cfa_offset 16
Ltmp34:
	.cfi_offset %rbp, -16
	movq	%rsp, %rbp
Ltmp35:
	.cfi_def_cfa_register %rbp
	pushq	%rbx
	subq	$24, %rsp
Ltmp36:
	.cfi_offset %rbx, -24
	callq	_CuStringNew
	movq	%rax, -16(%rbp)
	callq	_CuSuiteNew
	movq	%rax, %rbx
	movq	%rbx, -24(%rbp)
	callq	_counter_inc_test_suite
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
	leaq	L_.str7(%rip), %rdi
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
Ltmp39:
	.cfi_def_cfa_offset 16
Ltmp40:
	.cfi_offset %rbp, -16
	movq	%rsp, %rbp
Ltmp41:
	.cfi_def_cfa_register %rbp
	callq	_RunAllTests
	xorl	%eax, %eax
	popq	%rbp
	ret
	.cfi_endproc

	.section	__TEXT,__cstring,cstring_literals
L_.str:                                 ## @.str
	.asciz	"AllTests.c"

L_.str1:                                ## @.str1
	.asciz	"The invariant '((error = TRUE) => (value = MAXINT))' was unsatisfied"

L_.str2:                                ## @.str2
	.asciz	"The invariant '0 <= value' was unsatisfied"

L_.str3:                                ## @.str3
	.asciz	"The invariant 'value <= MAXINT' was unsatisfied"

	.comm	_counter,8,2            ## @counter
L_.str4:                                ## @.str4
	.asciz	"assert failed"

L_.str5:                                ## @.str5
	.asciz	"counter_inc_test_case_1"

L_.str6:                                ## @.str6
	.asciz	"counter_inc_test_case_2"

L_.str7:                                ## @.str7
	.asciz	"%s\n"


.subsections_via_symbols
