	.section	__TEXT,__text,regular,pure_instructions
	.globl	_bubble$init$
	.align	4, 0x90
_bubble$init$:                          ## @"bubble$init$"
	.cfi_startproc
## BB#0:                                ## %exit
	movl	$0, (%rdi)
	movl	$5, 20(%rdi)
	movl	4(%rdi), %eax
	movl	%eax, 28(%rdi)
	movl	$0, 400(%rdi)
	ret
	.cfi_endproc

	.globl	_bubble$op_sort
	.align	4, 0x90
_bubble$op_sort:                        ## @"bubble$op_sort"
	.cfi_startproc
## BB#0:                                ## %entry
	movl	$1, -8(%rsp)
	movl	$100, -4(%rsp)
	movl	$0, -12(%rsp)
	jmp	LBB1_1
	.align	4, 0x90
LBB1_2:                                 ## %label2
                                        ##   in Loop: Header=BB1_1 Depth=1
	movl	$0, -8(%rsp)
	movl	$0, -12(%rsp)
	decl	-4(%rsp)
	jmp	LBB1_3
	.align	4, 0x90
LBB1_6:                                 ## %label6
                                        ##   in Loop: Header=BB1_3 Depth=2
	incl	-12(%rsp)
LBB1_3:                                 ## %label4
                                        ##   Parent Loop BB1_1 Depth=1
                                        ## =>  This Inner Loop Header: Depth=2
	movl	-12(%rsp), %eax
	cmpl	-4(%rsp), %eax
	jg	LBB1_1
## BB#4:                                ## %label5
                                        ##   in Loop: Header=BB1_3 Depth=2
	movslq	-12(%rsp), %rax
	movl	(%rdi,%rax,4), %eax
	movl	%eax, -20(%rsp)
	movl	-12(%rsp), %eax
	incl	%eax
	cltq
	movl	(%rdi,%rax,4), %eax
	movl	%eax, -24(%rsp)
	cmpl	%eax, -20(%rsp)
	jle	LBB1_6
## BB#5:                                ## %label7
                                        ##   in Loop: Header=BB1_3 Depth=2
	movl	-12(%rsp), %eax
	incl	%eax
	cltq
	movl	(%rdi,%rax,4), %eax
	movl	%eax, -16(%rsp)
	movslq	-12(%rsp), %rax
	movl	(%rdi,%rax,4), %ecx
	leal	1(%rax), %eax
	cltq
	movl	%ecx, (%rdi,%rax,4)
	movl	-16(%rsp), %eax
	movslq	-12(%rsp), %rcx
	movl	%eax, (%rdi,%rcx,4)
	movl	$1, -8(%rsp)
	jmp	LBB1_6
	.align	4, 0x90
LBB1_1:                                 ## %label1
                                        ## =>This Loop Header: Depth=1
                                        ##     Child Loop BB1_3 Depth 2
	cmpl	$1, -8(%rsp)
	je	LBB1_2
## BB#7:                                ## %exit
	ret
	.cfi_endproc


.subsections_via_symbols
