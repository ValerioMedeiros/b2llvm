	.section	__TEXT,__text,regular,pure_instructions
	.globl	_counter$init$
	.align	4, 0x90
_counter$init$:                         ## @"counter$init$"
	.cfi_startproc
## BB#0:                                ## %exit
	movl	$0, (%rdi)
	movb	$0, 4(%rdi)
	ret
	.cfi_endproc

	.globl	_counter$zero
	.align	4, 0x90
_counter$zero:                          ## @"counter$zero"
	.cfi_startproc
## BB#0:                                ## %exit
	movl	$0, (%rdi)
	movb	$0, 4(%rdi)
	ret
	.cfi_endproc

	.globl	_counter$inc
	.align	4, 0x90
_counter$inc:                           ## @"counter$inc"
	.cfi_startproc
## BB#0:                                ## %entry
	cmpl	$2147483647, (%rdi)     ## imm = 0x7FFFFFFF
	je	LBB2_2
## BB#1:                                ## %label0
	incl	(%rdi)
	ret
LBB2_2:                                 ## %label1
	movb	$1, 4(%rdi)
	ret
	.cfi_endproc

	.globl	_counter$get
	.align	4, 0x90
_counter$get:                           ## @"counter$get"
	.cfi_startproc
## BB#0:                                ## %exit
	movl	(%rdi), %eax
	movl	%eax, (%rsi)
	ret
	.cfi_endproc


.subsections_via_symbols
