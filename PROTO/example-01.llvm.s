	.section	__TEXT,__text,regular,pure_instructions
	.globl	_counter_i$init$
	.align	4, 0x90
_counter_i$init$:                       ## @"counter_i$init$"
	.cfi_startproc
## BB#0:                                ## %entry
	movq	_counter_i$self$@GOTPCREL(%rip), %rax
	movl	$0, (%rax)
	movb	$0, 4(%rax)
	ret
	.cfi_endproc

	.globl	_counter_i$zero
	.align	4, 0x90
_counter_i$zero:                        ## @"counter_i$zero"
	.cfi_startproc
## BB#0:                                ## %entry
	movl	$0, (%rdi)
	movb	$0, 4(%rdi)
	ret
	.cfi_endproc

	.comm	_counter_i$self$,8,3    ## @"counter_i$self$"

.subsections_via_symbols
