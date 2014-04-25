	.section	__TEXT,__text,regular,pure_instructions
	.globl	_CuStrAlloc
	.align	4, 0x90
_CuStrAlloc:                            ## @CuStrAlloc
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
	movl	%edi, -4(%rbp)
	movslq	-4(%rbp), %rdi
	callq	_malloc
	movq	%rax, -16(%rbp)
	addq	$16, %rsp
	popq	%rbp
	ret
	.cfi_endproc

	.globl	_CuStrCopy
	.align	4, 0x90
_CuStrCopy:                             ## @CuStrCopy
	.cfi_startproc
## BB#0:
	pushq	%rbp
Ltmp7:
	.cfi_def_cfa_offset 16
Ltmp8:
	.cfi_offset %rbp, -16
	movq	%rsp, %rbp
Ltmp9:
	.cfi_def_cfa_register %rbp
	subq	$32, %rsp
	movq	%rdi, -8(%rbp)
	callq	_strlen
	movl	%eax, -12(%rbp)
	leal	1(%rax), %edi
	callq	_CuStrAlloc
	movq	%rax, -24(%rbp)
	movq	-8(%rbp), %rsi
	movq	%rax, %rdi
	callq	_strcpy
	movq	-24(%rbp), %rax
	addq	$32, %rsp
	popq	%rbp
	ret
	.cfi_endproc

	.globl	_CuStringInit
	.align	4, 0x90
_CuStringInit:                          ## @CuStringInit
	.cfi_startproc
## BB#0:
	pushq	%rbp
Ltmp12:
	.cfi_def_cfa_offset 16
Ltmp13:
	.cfi_offset %rbp, -16
	movq	%rsp, %rbp
Ltmp14:
	.cfi_def_cfa_register %rbp
	subq	$16, %rsp
	movq	%rdi, -8(%rbp)
	movl	$0, (%rdi)
	movq	-8(%rbp), %rax
	movl	$256, 4(%rax)           ## imm = 0x100
	movq	-8(%rbp), %rax
	movslq	4(%rax), %rdi
	callq	_malloc
	movq	-8(%rbp), %rcx
	movq	%rax, 8(%rcx)
	movq	-8(%rbp), %rax
	movq	8(%rax), %rax
	movb	$0, (%rax)
	addq	$16, %rsp
	popq	%rbp
	ret
	.cfi_endproc

	.globl	_CuStringNew
	.align	4, 0x90
_CuStringNew:                           ## @CuStringNew
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
	subq	$16, %rsp
	movl	$16, %edi
	callq	_malloc
	movq	%rax, -8(%rbp)
	movl	$0, (%rax)
	movq	-8(%rbp), %rax
	movl	$256, 4(%rax)           ## imm = 0x100
	movq	-8(%rbp), %rax
	movslq	4(%rax), %rdi
	callq	_malloc
	movq	-8(%rbp), %rcx
	movq	%rax, 8(%rcx)
	movq	-8(%rbp), %rax
	movq	8(%rax), %rax
	movb	$0, (%rax)
	movq	-8(%rbp), %rax
	addq	$16, %rsp
	popq	%rbp
	ret
	.cfi_endproc

	.globl	_CuStringDelete
	.align	4, 0x90
_CuStringDelete:                        ## @CuStringDelete
	.cfi_startproc
## BB#0:
	pushq	%rbp
Ltmp22:
	.cfi_def_cfa_offset 16
Ltmp23:
	.cfi_offset %rbp, -16
	movq	%rsp, %rbp
Ltmp24:
	.cfi_def_cfa_register %rbp
	subq	$16, %rsp
	movq	%rdi, -8(%rbp)
	testq	%rdi, %rdi
	je	LBB4_2
## BB#1:
	movq	-8(%rbp), %rax
	movq	8(%rax), %rdi
	callq	_free
	movq	-8(%rbp), %rdi
	callq	_free
LBB4_2:
	addq	$16, %rsp
	popq	%rbp
	ret
	.cfi_endproc

	.globl	_CuStringResize
	.align	4, 0x90
_CuStringResize:                        ## @CuStringResize
	.cfi_startproc
## BB#0:
	pushq	%rbp
Ltmp27:
	.cfi_def_cfa_offset 16
Ltmp28:
	.cfi_offset %rbp, -16
	movq	%rsp, %rbp
Ltmp29:
	.cfi_def_cfa_register %rbp
	subq	$16, %rsp
	movq	%rdi, -8(%rbp)
	movl	%esi, -12(%rbp)
	movq	-8(%rbp), %rax
	movq	8(%rax), %rdi
	movslq	-12(%rbp), %rsi
	callq	_realloc
	movq	-8(%rbp), %rcx
	movq	%rax, 8(%rcx)
	movl	-12(%rbp), %eax
	movq	-8(%rbp), %rcx
	movl	%eax, 4(%rcx)
	addq	$16, %rsp
	popq	%rbp
	ret
	.cfi_endproc

	.globl	_CuStringAppend
	.align	4, 0x90
_CuStringAppend:                        ## @CuStringAppend
	.cfi_startproc
## BB#0:
	pushq	%rbp
Ltmp32:
	.cfi_def_cfa_offset 16
Ltmp33:
	.cfi_offset %rbp, -16
	movq	%rsp, %rbp
Ltmp34:
	.cfi_def_cfa_register %rbp
	subq	$32, %rsp
	movq	%rdi, -8(%rbp)
	movq	%rsi, -16(%rbp)
	testq	%rsi, %rsi
	jne	LBB6_2
## BB#1:
	leaq	L_.str(%rip), %rax
	movq	%rax, -16(%rbp)
LBB6_2:
	movq	-16(%rbp), %rdi
	callq	_strlen
	movl	%eax, -20(%rbp)
	movq	-8(%rbp), %rcx
	movl	(%rcx), %edx
	leal	1(%rdx,%rax), %eax
	cmpl	4(%rcx), %eax
	jl	LBB6_4
## BB#3:
	movq	-8(%rbp), %rdi
	movl	(%rdi), %eax
	movl	-20(%rbp), %ecx
	leal	257(%rax,%rcx), %esi
	callq	_CuStringResize
LBB6_4:
	movl	-20(%rbp), %eax
	movq	-8(%rbp), %rcx
	addl	%eax, (%rcx)
	movq	-8(%rbp), %rax
	movq	8(%rax), %rdi
	movq	-16(%rbp), %rsi
	movq	$-1, %rdx
	callq	___strcat_chk
	addq	$32, %rsp
	popq	%rbp
	ret
	.cfi_endproc

	.globl	_CuStringAppendChar
	.align	4, 0x90
_CuStringAppendChar:                    ## @CuStringAppendChar
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
	subq	$16, %rsp
	movq	%rdi, -8(%rbp)
	movb	%sil, -9(%rbp)
	movb	%sil, -11(%rbp)
	movb	$0, -10(%rbp)
	movq	-8(%rbp), %rdi
	leaq	-11(%rbp), %rsi
	callq	_CuStringAppend
	addq	$16, %rsp
	popq	%rbp
	ret
	.cfi_endproc

	.globl	_CuStringAppendFormat
	.align	4, 0x90
_CuStringAppendFormat:                  ## @CuStringAppendFormat
	.cfi_startproc
## BB#0:
	pushq	%rbp
Ltmp43:
	.cfi_def_cfa_offset 16
Ltmp44:
	.cfi_offset %rbp, -16
	movq	%rsp, %rbp
Ltmp45:
	.cfi_def_cfa_register %rbp
	pushq	%r14
	pushq	%rbx
	subq	$8416, %rsp             ## imm = 0x20E0
Ltmp46:
	.cfi_offset %rbx, -32
Ltmp47:
	.cfi_offset %r14, -24
	testb	%al, %al
	je	LBB8_2
## BB#1:
	vmovaps	%xmm0, -8384(%rbp)
	vmovaps	%xmm1, -8368(%rbp)
	vmovaps	%xmm2, -8352(%rbp)
	vmovaps	%xmm3, -8336(%rbp)
	vmovaps	%xmm4, -8320(%rbp)
	vmovaps	%xmm5, -8304(%rbp)
	vmovaps	%xmm6, -8288(%rbp)
	vmovaps	%xmm7, -8272(%rbp)
LBB8_2:
	movq	%r9, -8392(%rbp)
	movq	%r8, -8400(%rbp)
	movq	%rcx, -8408(%rbp)
	movq	%rdx, -8416(%rbp)
	movq	___stack_chk_guard@GOTPCREL(%rip), %r14
	movq	(%r14), %rax
	movq	%rax, -24(%rbp)
	movq	%rdi, -8248(%rbp)
	movq	%rsi, -8256(%rbp)
	leaq	-8432(%rbp), %rax
	movq	%rax, -32(%rbp)
	leaq	16(%rbp), %rax
	movq	%rax, -40(%rbp)
	movl	$48, -44(%rbp)
	movl	$16, -48(%rbp)
	movq	-8256(%rbp), %rcx
	leaq	-8240(%rbp), %rbx
	leaq	-48(%rbp), %r8
	xorl	%esi, %esi
	movl	$8192, %edx             ## imm = 0x2000
	movq	%rbx, %rdi
	callq	___vsprintf_chk
	movq	-8248(%rbp), %rdi
	movq	%rbx, %rsi
	callq	_CuStringAppend
	movq	(%r14), %rax
	cmpq	-24(%rbp), %rax
	jne	LBB8_4
## BB#3:
	addq	$8416, %rsp             ## imm = 0x20E0
	popq	%rbx
	popq	%r14
	popq	%rbp
	ret
LBB8_4:
	callq	___stack_chk_fail
	.cfi_endproc

	.globl	_CuStringInsert
	.align	4, 0x90
_CuStringInsert:                        ## @CuStringInsert
	.cfi_startproc
## BB#0:
	pushq	%rbp
Ltmp50:
	.cfi_def_cfa_offset 16
Ltmp51:
	.cfi_offset %rbp, -16
	movq	%rsp, %rbp
Ltmp52:
	.cfi_def_cfa_register %rbp
	subq	$32, %rsp
	movq	%rdi, -8(%rbp)
	movq	%rsi, -16(%rbp)
	movl	%edx, -20(%rbp)
	movq	-16(%rbp), %rdi
	callq	_strlen
	movl	%eax, -24(%rbp)
	movl	-20(%rbp), %eax
	movq	-8(%rbp), %rcx
	cmpl	(%rcx), %eax
	jle	LBB9_2
## BB#1:
	movq	-8(%rbp), %rax
	movl	(%rax), %eax
	movl	%eax, -20(%rbp)
LBB9_2:
	movq	-8(%rbp), %rax
	movl	(%rax), %ecx
	movl	-24(%rbp), %edx
	leal	1(%rcx,%rdx), %ecx
	cmpl	4(%rax), %ecx
	jl	LBB9_4
## BB#3:
	movq	-8(%rbp), %rdi
	movl	(%rdi), %eax
	movl	-24(%rbp), %ecx
	leal	257(%rax,%rcx), %esi
	callq	_CuStringResize
LBB9_4:
	movq	-8(%rbp), %rax
	movslq	-20(%rbp), %rsi
	movl	(%rax), %ecx
	subl	%esi, %ecx
	addq	8(%rax), %rsi
	movslq	-24(%rbp), %rdi
	addq	%rsi, %rdi
	incl	%ecx
	movslq	%ecx, %rdx
	callq	_memmove
	movl	-24(%rbp), %eax
	movq	-8(%rbp), %rcx
	addl	%eax, (%rcx)
	movq	-8(%rbp), %rax
	movslq	-20(%rbp), %rdi
	addq	8(%rax), %rdi
	movq	-16(%rbp), %rsi
	movslq	-24(%rbp), %rdx
	callq	_memcpy
	addq	$32, %rsp
	popq	%rbp
	ret
	.cfi_endproc

	.globl	_CuTestInit
	.align	4, 0x90
_CuTestInit:                            ## @CuTestInit
	.cfi_startproc
## BB#0:
	pushq	%rbp
Ltmp55:
	.cfi_def_cfa_offset 16
Ltmp56:
	.cfi_offset %rbp, -16
	movq	%rsp, %rbp
Ltmp57:
	.cfi_def_cfa_register %rbp
	subq	$32, %rsp
	movq	%rdi, -8(%rbp)
	movq	%rsi, -16(%rbp)
	movq	%rdx, -24(%rbp)
	movq	-16(%rbp), %rdi
	callq	_CuStrCopy
	movq	-8(%rbp), %rcx
	movq	%rax, (%rcx)
	movq	-8(%rbp), %rax
	movl	$0, 16(%rax)
	movq	-8(%rbp), %rax
	movl	$0, 20(%rax)
	movq	-8(%rbp), %rax
	movq	$0, 24(%rax)
	movq	-24(%rbp), %rax
	movq	-8(%rbp), %rcx
	movq	%rax, 8(%rcx)
	movq	-8(%rbp), %rax
	movq	$0, 32(%rax)
	addq	$32, %rsp
	popq	%rbp
	ret
	.cfi_endproc

	.globl	_CuTestNew
	.align	4, 0x90
_CuTestNew:                             ## @CuTestNew
	.cfi_startproc
## BB#0:
	pushq	%rbp
Ltmp60:
	.cfi_def_cfa_offset 16
Ltmp61:
	.cfi_offset %rbp, -16
	movq	%rsp, %rbp
Ltmp62:
	.cfi_def_cfa_register %rbp
	subq	$32, %rsp
	movq	%rdi, -8(%rbp)
	movq	%rsi, -16(%rbp)
	movl	$40, %edi
	callq	_malloc
	movq	%rax, -24(%rbp)
	movq	-8(%rbp), %rsi
	movq	-16(%rbp), %rdx
	movq	%rax, %rdi
	callq	_CuTestInit
	movq	-24(%rbp), %rax
	addq	$32, %rsp
	popq	%rbp
	ret
	.cfi_endproc

	.globl	_CuTestDelete
	.align	4, 0x90
_CuTestDelete:                          ## @CuTestDelete
	.cfi_startproc
## BB#0:
	pushq	%rbp
Ltmp65:
	.cfi_def_cfa_offset 16
Ltmp66:
	.cfi_offset %rbp, -16
	movq	%rsp, %rbp
Ltmp67:
	.cfi_def_cfa_register %rbp
	subq	$16, %rsp
	movq	%rdi, -8(%rbp)
	testq	%rdi, %rdi
	je	LBB12_2
## BB#1:
	movq	-8(%rbp), %rax
	movq	(%rax), %rdi
	callq	_free
	movq	-8(%rbp), %rdi
	callq	_free
LBB12_2:
	addq	$16, %rsp
	popq	%rbp
	ret
	.cfi_endproc

	.globl	_CuTestRun
	.align	4, 0x90
_CuTestRun:                             ## @CuTestRun
	.cfi_startproc
## BB#0:
	pushq	%rbp
Ltmp71:
	.cfi_def_cfa_offset 16
Ltmp72:
	.cfi_offset %rbp, -16
	movq	%rsp, %rbp
Ltmp73:
	.cfi_def_cfa_register %rbp
	pushq	%rbx
	subq	$184, %rsp
Ltmp74:
	.cfi_offset %rbx, -24
	movq	___stack_chk_guard@GOTPCREL(%rip), %rbx
	movq	(%rbx), %rax
	movq	%rax, -16(%rbp)
	movq	%rdi, -184(%rbp)
	leaq	-176(%rbp), %rax
	movq	%rax, 32(%rdi)
	movq	%rax, %rdi
	callq	_setjmp
	testl	%eax, %eax
	jne	LBB13_2
## BB#1:
	movq	-184(%rbp), %rax
	movl	$1, 20(%rax)
	movq	-184(%rbp), %rdi
	callq	*8(%rdi)
LBB13_2:
	movq	-184(%rbp), %rax
	movq	$0, 32(%rax)
	movq	(%rbx), %rax
	cmpq	-16(%rbp), %rax
	jne	LBB13_4
## BB#3:
	addq	$184, %rsp
	popq	%rbx
	popq	%rbp
	ret
LBB13_4:
	callq	___stack_chk_fail
	.cfi_endproc

	.globl	_CuFail_Line
	.align	4, 0x90
_CuFail_Line:                           ## @CuFail_Line
	.cfi_startproc
## BB#0:
	pushq	%rbp
Ltmp78:
	.cfi_def_cfa_offset 16
Ltmp79:
	.cfi_offset %rbp, -16
	movq	%rsp, %rbp
Ltmp80:
	.cfi_def_cfa_register %rbp
	pushq	%rbx
	subq	$56, %rsp
Ltmp81:
	.cfi_offset %rbx, -24
	movq	%rdi, -16(%rbp)
	movq	%rsi, -24(%rbp)
	movl	%edx, -28(%rbp)
	movq	%rcx, -40(%rbp)
	movq	%r8, -48(%rbp)
	leaq	-64(%rbp), %rdi
	callq	_CuStringInit
	cmpq	$0, -40(%rbp)
	je	LBB14_2
## BB#1:
	movq	-40(%rbp), %rsi
	leaq	-64(%rbp), %rbx
	movq	%rbx, %rdi
	callq	_CuStringAppend
	leaq	L_.str1(%rip), %rsi
	movq	%rbx, %rdi
	callq	_CuStringAppend
LBB14_2:
	movq	-48(%rbp), %rsi
	leaq	-64(%rbp), %rbx
	movq	%rbx, %rdi
	callq	_CuStringAppend
	movq	-16(%rbp), %rdi
	movq	-24(%rbp), %rsi
	movl	-28(%rbp), %edx
	movq	%rbx, %rcx
	callq	_CuFailInternal
	addq	$56, %rsp
	popq	%rbx
	popq	%rbp
	ret
	.cfi_endproc

	.align	4, 0x90
_CuFailInternal:                        ## @CuFailInternal
	.cfi_startproc
## BB#0:
	pushq	%rbp
Ltmp85:
	.cfi_def_cfa_offset 16
Ltmp86:
	.cfi_offset %rbp, -16
	movq	%rsp, %rbp
Ltmp87:
	.cfi_def_cfa_register %rbp
	pushq	%r14
	pushq	%rbx
	subq	$8240, %rsp             ## imm = 0x2030
Ltmp88:
	.cfi_offset %rbx, -32
Ltmp89:
	.cfi_offset %r14, -24
	movq	___stack_chk_guard@GOTPCREL(%rip), %r14
	movq	(%r14), %rax
	movq	%rax, -24(%rbp)
	movq	%rdi, -8232(%rbp)
	movq	%rsi, -8240(%rbp)
	movl	%edx, -8244(%rbp)
	movq	%rcx, -8256(%rbp)
	movq	-8240(%rbp), %r8
	movl	-8244(%rbp), %r9d
	leaq	L_.str23(%rip), %rcx
	leaq	-8224(%rbp), %rbx
	movl	$0, %esi
	movl	$8192, %edx             ## imm = 0x2000
	xorl	%eax, %eax
	movq	%rbx, %rdi
	callq	___sprintf_chk
	movq	-8256(%rbp), %rdi
	xorl	%edx, %edx
	movq	%rbx, %rsi
	callq	_CuStringInsert
	movq	-8232(%rbp), %rax
	movl	$1, 16(%rax)
	movq	-8256(%rbp), %rax
	movq	8(%rax), %rax
	movq	-8232(%rbp), %rcx
	movq	%rax, 24(%rcx)
	movq	-8232(%rbp), %rax
	cmpq	$0, 32(%rax)
	jne	LBB15_3
## BB#1:
	movq	(%r14), %rax
	cmpq	-24(%rbp), %rax
	jne	LBB15_4
## BB#2:
	addq	$8240, %rsp             ## imm = 0x2030
	popq	%rbx
	popq	%r14
	popq	%rbp
	ret
LBB15_4:
	callq	___stack_chk_fail
LBB15_3:
	movq	-8232(%rbp), %rax
	movq	32(%rax), %rax
	xorl	%esi, %esi
	movq	%rax, %rdi
	callq	_longjmp
	.cfi_endproc

	.globl	_CuAssert_Line
	.align	4, 0x90
_CuAssert_Line:                         ## @CuAssert_Line
	.cfi_startproc
## BB#0:
	pushq	%rbp
Ltmp92:
	.cfi_def_cfa_offset 16
Ltmp93:
	.cfi_offset %rbp, -16
	movq	%rsp, %rbp
Ltmp94:
	.cfi_def_cfa_register %rbp
	subq	$48, %rsp
	movq	%rdi, -8(%rbp)
	movq	%rsi, -16(%rbp)
	movl	%edx, -20(%rbp)
	movq	%rcx, -32(%rbp)
	movl	%r8d, -36(%rbp)
	testl	%r8d, %r8d
	jne	LBB16_2
## BB#1:
	movq	-8(%rbp), %rdi
	movq	-16(%rbp), %rsi
	movl	-20(%rbp), %edx
	movq	-32(%rbp), %r8
	xorl	%ecx, %ecx
	callq	_CuFail_Line
LBB16_2:
	addq	$48, %rsp
	popq	%rbp
	ret
	.cfi_endproc

	.globl	_CuAssertStrEquals_LineMsg
	.align	4, 0x90
_CuAssertStrEquals_LineMsg:             ## @CuAssertStrEquals_LineMsg
	.cfi_startproc
## BB#0:
	pushq	%rbp
Ltmp98:
	.cfi_def_cfa_offset 16
Ltmp99:
	.cfi_offset %rbp, -16
	movq	%rsp, %rbp
Ltmp100:
	.cfi_def_cfa_register %rbp
	pushq	%rbx
	subq	$72, %rsp
Ltmp101:
	.cfi_offset %rbx, -24
	movq	%rdi, -16(%rbp)
	movq	%rsi, -24(%rbp)
	movl	%edx, -28(%rbp)
	movq	%rcx, -40(%rbp)
	movq	%r8, -48(%rbp)
	movq	%r9, -56(%rbp)
	cmpq	$0, -48(%rbp)
	jne	LBB17_2
## BB#1:
	cmpq	$0, -56(%rbp)
	je	LBB17_8
LBB17_2:
	cmpq	$0, -48(%rbp)
	je	LBB17_5
## BB#3:
	cmpq	$0, -56(%rbp)
	je	LBB17_5
## BB#4:
	movq	-48(%rbp), %rdi
	movq	-56(%rbp), %rsi
	callq	_strcmp
	testl	%eax, %eax
	je	LBB17_8
LBB17_5:
	leaq	-72(%rbp), %rdi
	callq	_CuStringInit
	cmpq	$0, -40(%rbp)
	je	LBB17_7
## BB#6:
	movq	-40(%rbp), %rsi
	leaq	-72(%rbp), %rbx
	movq	%rbx, %rdi
	callq	_CuStringAppend
	leaq	L_.str1(%rip), %rsi
	movq	%rbx, %rdi
	callq	_CuStringAppend
LBB17_7:
	leaq	L_.str2(%rip), %rsi
	leaq	-72(%rbp), %rbx
	movq	%rbx, %rdi
	callq	_CuStringAppend
	movq	-48(%rbp), %rsi
	movq	%rbx, %rdi
	callq	_CuStringAppend
	leaq	L_.str3(%rip), %rsi
	movq	%rbx, %rdi
	callq	_CuStringAppend
	movq	-56(%rbp), %rsi
	movq	%rbx, %rdi
	callq	_CuStringAppend
	leaq	L_.str4(%rip), %rsi
	movq	%rbx, %rdi
	callq	_CuStringAppend
	movq	-16(%rbp), %rdi
	movq	-24(%rbp), %rsi
	movl	-28(%rbp), %edx
	movq	%rbx, %rcx
	callq	_CuFailInternal
LBB17_8:
	addq	$72, %rsp
	popq	%rbx
	popq	%rbp
	ret
	.cfi_endproc

	.globl	_CuAssertIntEquals_LineMsg
	.align	4, 0x90
_CuAssertIntEquals_LineMsg:             ## @CuAssertIntEquals_LineMsg
	.cfi_startproc
## BB#0:
	pushq	%rbp
Ltmp105:
	.cfi_def_cfa_offset 16
Ltmp106:
	.cfi_offset %rbp, -16
	movq	%rsp, %rbp
Ltmp107:
	.cfi_def_cfa_register %rbp
	pushq	%r14
	pushq	%rbx
	subq	$320, %rsp              ## imm = 0x140
Ltmp108:
	.cfi_offset %rbx, -32
Ltmp109:
	.cfi_offset %r14, -24
	movq	___stack_chk_guard@GOTPCREL(%rip), %rbx
	movq	(%rbx), %rax
	movq	%rax, -24(%rbp)
	movq	%rdi, -296(%rbp)
	movq	%rsi, -304(%rbp)
	movl	%edx, -308(%rbp)
	movq	%rcx, -320(%rbp)
	movl	%r8d, -324(%rbp)
	movl	%r9d, -328(%rbp)
	cmpl	%r9d, -324(%rbp)
	je	LBB18_2
## BB#1:
	movl	-324(%rbp), %r8d
	movl	-328(%rbp), %r9d
	leaq	L_.str5(%rip), %rcx
	leaq	-288(%rbp), %r14
	movl	$0, %esi
	movl	$256, %edx              ## imm = 0x100
	xorl	%eax, %eax
	movq	%r14, %rdi
	callq	___sprintf_chk
	movq	-296(%rbp), %rdi
	movq	-304(%rbp), %rsi
	movl	-308(%rbp), %edx
	movq	-320(%rbp), %rcx
	movq	%r14, %r8
	callq	_CuFail_Line
LBB18_2:
	movq	(%rbx), %rax
	cmpq	-24(%rbp), %rax
	jne	LBB18_4
## BB#3:
	addq	$320, %rsp              ## imm = 0x140
	popq	%rbx
	popq	%r14
	popq	%rbp
	ret
LBB18_4:
	callq	___stack_chk_fail
	.cfi_endproc

	.section	__TEXT,__const
	.align	4
LCPI19_0:
	.quad	9223372036854775807     ## double nan
	.quad	9223372036854775807     ## double nan
	.section	__TEXT,__text,regular,pure_instructions
	.globl	_CuAssertDblEquals_LineMsg
	.align	4, 0x90
_CuAssertDblEquals_LineMsg:             ## @CuAssertDblEquals_LineMsg
	.cfi_startproc
## BB#0:
	pushq	%rbp
Ltmp113:
	.cfi_def_cfa_offset 16
Ltmp114:
	.cfi_offset %rbp, -16
	movq	%rsp, %rbp
Ltmp115:
	.cfi_def_cfa_register %rbp
	pushq	%r14
	pushq	%rbx
	subq	$336, %rsp              ## imm = 0x150
Ltmp116:
	.cfi_offset %rbx, -32
Ltmp117:
	.cfi_offset %r14, -24
	movq	___stack_chk_guard@GOTPCREL(%rip), %rbx
	movq	(%rbx), %rax
	movq	%rax, -24(%rbp)
	movq	%rdi, -296(%rbp)
	movq	%rsi, -304(%rbp)
	movl	%edx, -308(%rbp)
	movq	%rcx, -320(%rbp)
	vmovsd	%xmm0, -328(%rbp)
	vmovsd	%xmm1, -336(%rbp)
	vmovsd	%xmm2, -344(%rbp)
	vmovsd	-328(%rbp), %xmm0
	vsubsd	-336(%rbp), %xmm0, %xmm0
	vandpd	LCPI19_0(%rip), %xmm0, %xmm0
	vucomisd	%xmm0, %xmm2
	jae	LBB19_2
## BB#1:
	vmovsd	-328(%rbp), %xmm0
	vmovsd	-336(%rbp), %xmm1
	leaq	L_.str6(%rip), %rcx
	leaq	-288(%rbp), %r14
	xorl	%esi, %esi
	movl	$256, %edx              ## imm = 0x100
	movb	$2, %al
	movq	%r14, %rdi
	callq	___sprintf_chk
	movq	-296(%rbp), %rdi
	movq	-304(%rbp), %rsi
	movl	-308(%rbp), %edx
	movq	-320(%rbp), %rcx
	movq	%r14, %r8
	callq	_CuFail_Line
LBB19_2:
	movq	(%rbx), %rax
	cmpq	-24(%rbp), %rax
	jne	LBB19_4
## BB#3:
	addq	$336, %rsp              ## imm = 0x150
	popq	%rbx
	popq	%r14
	popq	%rbp
	ret
LBB19_4:
	callq	___stack_chk_fail
	.cfi_endproc

	.globl	_CuAssertPtrEquals_LineMsg
	.align	4, 0x90
_CuAssertPtrEquals_LineMsg:             ## @CuAssertPtrEquals_LineMsg
	.cfi_startproc
## BB#0:
	pushq	%rbp
Ltmp121:
	.cfi_def_cfa_offset 16
Ltmp122:
	.cfi_offset %rbp, -16
	movq	%rsp, %rbp
Ltmp123:
	.cfi_def_cfa_register %rbp
	pushq	%r14
	pushq	%rbx
	subq	$320, %rsp              ## imm = 0x140
Ltmp124:
	.cfi_offset %rbx, -32
Ltmp125:
	.cfi_offset %r14, -24
	movq	___stack_chk_guard@GOTPCREL(%rip), %rbx
	movq	(%rbx), %rax
	movq	%rax, -24(%rbp)
	movq	%rdi, -296(%rbp)
	movq	%rsi, -304(%rbp)
	movl	%edx, -308(%rbp)
	movq	%rcx, -320(%rbp)
	movq	%r8, -328(%rbp)
	movq	%r9, -336(%rbp)
	cmpq	%r9, -328(%rbp)
	je	LBB20_2
## BB#1:
	movq	-328(%rbp), %r8
	movq	-336(%rbp), %r9
	leaq	L_.str7(%rip), %rcx
	leaq	-288(%rbp), %r14
	movl	$0, %esi
	movl	$256, %edx              ## imm = 0x100
	xorl	%eax, %eax
	movq	%r14, %rdi
	callq	___sprintf_chk
	movq	-296(%rbp), %rdi
	movq	-304(%rbp), %rsi
	movl	-308(%rbp), %edx
	movq	-320(%rbp), %rcx
	movq	%r14, %r8
	callq	_CuFail_Line
LBB20_2:
	movq	(%rbx), %rax
	cmpq	-24(%rbp), %rax
	jne	LBB20_4
## BB#3:
	addq	$320, %rsp              ## imm = 0x140
	popq	%rbx
	popq	%r14
	popq	%rbp
	ret
LBB20_4:
	callq	___stack_chk_fail
	.cfi_endproc

	.globl	_CuSuiteInit
	.align	4, 0x90
_CuSuiteInit:                           ## @CuSuiteInit
	.cfi_startproc
## BB#0:
	pushq	%rbp
Ltmp128:
	.cfi_def_cfa_offset 16
Ltmp129:
	.cfi_offset %rbp, -16
	movq	%rsp, %rbp
Ltmp130:
	.cfi_def_cfa_register %rbp
	subq	$16, %rsp
	movq	%rdi, -8(%rbp)
	movl	$0, (%rdi)
	movq	-8(%rbp), %rax
	movl	$0, 8200(%rax)
	movq	-8(%rbp), %rdi
	addq	$8, %rdi
	movl	$8192, %esi             ## imm = 0x2000
	callq	___bzero
	addq	$16, %rsp
	popq	%rbp
	ret
	.cfi_endproc

	.globl	_CuSuiteNew
	.align	4, 0x90
_CuSuiteNew:                            ## @CuSuiteNew
	.cfi_startproc
## BB#0:
	pushq	%rbp
Ltmp133:
	.cfi_def_cfa_offset 16
Ltmp134:
	.cfi_offset %rbp, -16
	movq	%rsp, %rbp
Ltmp135:
	.cfi_def_cfa_register %rbp
	subq	$16, %rsp
	movl	$8208, %edi             ## imm = 0x2010
	callq	_malloc
	movq	%rax, -8(%rbp)
	movq	%rax, %rdi
	callq	_CuSuiteInit
	movq	-8(%rbp), %rax
	addq	$16, %rsp
	popq	%rbp
	ret
	.cfi_endproc

	.globl	_CuSuiteDelete
	.align	4, 0x90
_CuSuiteDelete:                         ## @CuSuiteDelete
	.cfi_startproc
## BB#0:
	pushq	%rbp
Ltmp138:
	.cfi_def_cfa_offset 16
Ltmp139:
	.cfi_offset %rbp, -16
	movq	%rsp, %rbp
Ltmp140:
	.cfi_def_cfa_register %rbp
	subq	$16, %rsp
	movq	%rdi, -8(%rbp)
	movl	$0, -12(%rbp)
	jmp	LBB23_1
	.align	4, 0x90
LBB23_4:                                ##   in Loop: Header=BB23_1 Depth=1
	incl	-12(%rbp)
LBB23_1:                                ## =>This Inner Loop Header: Depth=1
	cmpl	$1023, -12(%rbp)        ## imm = 0x3FF
	ja	LBB23_5
## BB#2:                                ##   in Loop: Header=BB23_1 Depth=1
	movl	-12(%rbp), %eax
	movq	-8(%rbp), %rcx
	cmpq	$0, 8(%rcx,%rax,8)
	je	LBB23_4
## BB#3:                                ##   in Loop: Header=BB23_1 Depth=1
	movl	-12(%rbp), %eax
	movq	-8(%rbp), %rcx
	movq	8(%rcx,%rax,8), %rdi
	callq	_CuTestDelete
	jmp	LBB23_4
LBB23_5:
	movq	-8(%rbp), %rdi
	callq	_free
	addq	$16, %rsp
	popq	%rbp
	ret
	.cfi_endproc

	.globl	_CuSuiteAdd
	.align	4, 0x90
_CuSuiteAdd:                            ## @CuSuiteAdd
	.cfi_startproc
## BB#0:
	pushq	%rbp
Ltmp143:
	.cfi_def_cfa_offset 16
Ltmp144:
	.cfi_offset %rbp, -16
	movq	%rsp, %rbp
Ltmp145:
	.cfi_def_cfa_register %rbp
	subq	$16, %rsp
	movq	%rdi, -8(%rbp)
	movq	%rsi, -16(%rbp)
	movq	-8(%rbp), %rax
	cmpl	$1024, (%rax)           ## imm = 0x400
	jge	LBB24_2
## BB#1:
	movq	-16(%rbp), %rax
	movq	-8(%rbp), %rcx
	movslq	(%rcx), %rdx
	movq	%rax, 8(%rcx,%rdx,8)
	movq	-8(%rbp), %rax
	incl	(%rax)
	addq	$16, %rsp
	popq	%rbp
	ret
LBB24_2:
	leaq	L___func__.CuSuiteAdd(%rip), %rax
	leaq	L_.str8(%rip), %rcx
	leaq	L_.str9(%rip), %r8
	movl	$268, %edx              ## imm = 0x10C
	movq	%rax, %rdi
	movq	%rcx, %rsi
	movq	%r8, %rcx
	callq	___assert_rtn
	.cfi_endproc

	.globl	_CuSuiteAddSuite
	.align	4, 0x90
_CuSuiteAddSuite:                       ## @CuSuiteAddSuite
	.cfi_startproc
## BB#0:
	pushq	%rbp
Ltmp148:
	.cfi_def_cfa_offset 16
Ltmp149:
	.cfi_offset %rbp, -16
	movq	%rsp, %rbp
Ltmp150:
	.cfi_def_cfa_register %rbp
	subq	$32, %rsp
	movq	%rdi, -8(%rbp)
	movq	%rsi, -16(%rbp)
	movl	$0, -20(%rbp)
	jmp	LBB25_1
	.align	4, 0x90
LBB25_2:                                ##   in Loop: Header=BB25_1 Depth=1
	movslq	-20(%rbp), %rax
	movq	-16(%rbp), %rcx
	movq	8(%rcx,%rax,8), %rsi
	movq	%rsi, -32(%rbp)
	movq	-8(%rbp), %rdi
	callq	_CuSuiteAdd
	incl	-20(%rbp)
LBB25_1:                                ## =>This Inner Loop Header: Depth=1
	movl	-20(%rbp), %eax
	movq	-16(%rbp), %rcx
	cmpl	(%rcx), %eax
	jl	LBB25_2
## BB#3:
	addq	$32, %rsp
	popq	%rbp
	ret
	.cfi_endproc

	.globl	_CuSuiteRun
	.align	4, 0x90
_CuSuiteRun:                            ## @CuSuiteRun
	.cfi_startproc
## BB#0:
	pushq	%rbp
Ltmp153:
	.cfi_def_cfa_offset 16
Ltmp154:
	.cfi_offset %rbp, -16
	movq	%rsp, %rbp
Ltmp155:
	.cfi_def_cfa_register %rbp
	subq	$32, %rsp
	movq	%rdi, -8(%rbp)
	movl	$0, -12(%rbp)
	jmp	LBB26_1
	.align	4, 0x90
LBB26_4:                                ##   in Loop: Header=BB26_1 Depth=1
	incl	-12(%rbp)
LBB26_1:                                ## =>This Inner Loop Header: Depth=1
	movl	-12(%rbp), %eax
	movq	-8(%rbp), %rcx
	cmpl	(%rcx), %eax
	jge	LBB26_5
## BB#2:                                ##   in Loop: Header=BB26_1 Depth=1
	movslq	-12(%rbp), %rax
	movq	-8(%rbp), %rcx
	movq	8(%rcx,%rax,8), %rdi
	movq	%rdi, -24(%rbp)
	callq	_CuTestRun
	movq	-24(%rbp), %rax
	cmpl	$0, 16(%rax)
	je	LBB26_4
## BB#3:                                ##   in Loop: Header=BB26_1 Depth=1
	movq	-8(%rbp), %rax
	incl	8200(%rax)
	jmp	LBB26_4
LBB26_5:
	addq	$32, %rsp
	popq	%rbp
	ret
	.cfi_endproc

	.globl	_CuSuiteSummary
	.align	4, 0x90
_CuSuiteSummary:                        ## @CuSuiteSummary
	.cfi_startproc
## BB#0:
	pushq	%rbp
Ltmp159:
	.cfi_def_cfa_offset 16
Ltmp160:
	.cfi_offset %rbp, -16
	movq	%rsp, %rbp
Ltmp161:
	.cfi_def_cfa_register %rbp
	pushq	%r14
	pushq	%rbx
	subq	$32, %rsp
Ltmp162:
	.cfi_offset %rbx, -32
Ltmp163:
	.cfi_offset %r14, -24
	movq	%rdi, -24(%rbp)
	movq	%rsi, -32(%rbp)
	movl	$0, -36(%rbp)
	leaq	L_.str10(%rip), %rbx
	leaq	L_.str11(%rip), %r14
	jmp	LBB27_1
	.align	4, 0x90
LBB27_4:                                ##   in Loop: Header=BB27_1 Depth=1
	callq	_CuStringAppend
	incl	-36(%rbp)
LBB27_1:                                ## =>This Inner Loop Header: Depth=1
	movl	-36(%rbp), %eax
	movq	-24(%rbp), %rcx
	cmpl	(%rcx), %eax
	jge	LBB27_5
## BB#2:                                ##   in Loop: Header=BB27_1 Depth=1
	movslq	-36(%rbp), %rax
	movq	-24(%rbp), %rcx
	movq	8(%rcx,%rax,8), %rax
	movq	%rax, -48(%rbp)
	movq	-32(%rbp), %rdi
	cmpl	$0, 16(%rax)
	movq	%rbx, %rsi
	jne	LBB27_4
## BB#3:                                ## %select.mid
                                        ##   in Loop: Header=BB27_1 Depth=1
	movq	%r14, %rsi
	jmp	LBB27_4
LBB27_5:
	movq	-32(%rbp), %rdi
	leaq	L_.str12(%rip), %rsi
	callq	_CuStringAppend
	addq	$32, %rsp
	popq	%rbx
	popq	%r14
	popq	%rbp
	ret
	.cfi_endproc

	.globl	_CuSuiteDetails
	.align	4, 0x90
_CuSuiteDetails:                        ## @CuSuiteDetails
	.cfi_startproc
## BB#0:
	pushq	%rbp
Ltmp167:
	.cfi_def_cfa_offset 16
Ltmp168:
	.cfi_offset %rbp, -16
	movq	%rsp, %rbp
Ltmp169:
	.cfi_def_cfa_register %rbp
	pushq	%rbx
	subq	$56, %rsp
Ltmp170:
	.cfi_offset %rbx, -24
	movq	%rdi, -16(%rbp)
	movq	%rsi, -24(%rbp)
	movl	$0, -32(%rbp)
	movq	-16(%rbp), %rax
	cmpl	$0, 8200(%rax)
	je	LBB28_1
## BB#5:
	movq	-16(%rbp), %rax
	cmpl	$1, 8200(%rax)
	jne	LBB28_7
## BB#6:
	movq	-24(%rbp), %rdi
	leaq	L_.str16(%rip), %rsi
	callq	_CuStringAppend
	jmp	LBB28_8
LBB28_1:
	movq	-16(%rbp), %rax
	movl	(%rax), %ecx
	subl	8200(%rax), %ecx
	movl	%ecx, -36(%rbp)
	cmpl	$1, %ecx
	jne	LBB28_3
## BB#2:
	leaq	L_.str13(%rip), %rcx
	jmp	LBB28_4
LBB28_7:
	movq	-24(%rbp), %rdi
	movq	-16(%rbp), %rax
	movl	8200(%rax), %edx
	leaq	L_.str17(%rip), %rsi
	xorl	%eax, %eax
	callq	_CuStringAppendFormat
LBB28_8:
	movl	$0, -28(%rbp)
	leaq	L_.str18(%rip), %rbx
	jmp	LBB28_9
	.align	4, 0x90
LBB28_12:                               ##   in Loop: Header=BB28_9 Depth=1
	incl	-28(%rbp)
LBB28_9:                                ## =>This Inner Loop Header: Depth=1
	movl	-28(%rbp), %eax
	movq	-16(%rbp), %rcx
	cmpl	(%rcx), %eax
	jge	LBB28_13
## BB#10:                               ##   in Loop: Header=BB28_9 Depth=1
	movslq	-28(%rbp), %rax
	movq	-16(%rbp), %rcx
	movq	8(%rcx,%rax,8), %rax
	movq	%rax, -56(%rbp)
	cmpl	$0, 16(%rax)
	je	LBB28_12
## BB#11:                               ##   in Loop: Header=BB28_9 Depth=1
	movl	-32(%rbp), %edx
	incl	%edx
	movl	%edx, -32(%rbp)
	movq	-24(%rbp), %rdi
	movq	-56(%rbp), %rax
	movq	(%rax), %rcx
	movq	24(%rax), %r8
	xorl	%eax, %eax
	movq	%rbx, %rsi
	callq	_CuStringAppendFormat
	jmp	LBB28_12
LBB28_13:
	movq	-24(%rbp), %rdi
	leaq	L_.str19(%rip), %rsi
	callq	_CuStringAppend
	movq	-24(%rbp), %rdi
	movq	-16(%rbp), %rax
	movl	(%rax), %edx
	leaq	L_.str20(%rip), %rsi
	xorl	%eax, %eax
	callq	_CuStringAppendFormat
	movq	-24(%rbp), %rdi
	movq	-16(%rbp), %rax
	movl	(%rax), %edx
	subl	8200(%rax), %edx
	leaq	L_.str21(%rip), %rsi
	xorl	%eax, %eax
	callq	_CuStringAppendFormat
	movq	-24(%rbp), %rdi
	movq	-16(%rbp), %rax
	movl	8200(%rax), %edx
	leaq	L_.str22(%rip), %rsi
	xorl	%eax, %eax
	callq	_CuStringAppendFormat
	jmp	LBB28_14
LBB28_3:                                ## %select.mid
	leaq	L_.str14(%rip), %rcx
LBB28_4:                                ## %select.end
	movq	%rcx, -48(%rbp)
	movq	-24(%rbp), %rdi
	movl	-36(%rbp), %edx
	leaq	L_.str15(%rip), %rsi
	xorl	%eax, %eax
	callq	_CuStringAppendFormat
LBB28_14:
	addq	$56, %rsp
	popq	%rbx
	popq	%rbp
	ret
	.cfi_endproc

	.section	__TEXT,__cstring,cstring_literals
L_.str:                                 ## @.str
	.asciz	"NULL"

L_.str1:                                ## @.str1
	.asciz	": "

L_.str2:                                ## @.str2
	.asciz	"expected <"

L_.str3:                                ## @.str3
	.asciz	"> but was <"

L_.str4:                                ## @.str4
	.asciz	">"

L_.str5:                                ## @.str5
	.asciz	"expected <%d> but was <%d>"

L_.str6:                                ## @.str6
	.asciz	"expected <%f> but was <%f>"

L_.str7:                                ## @.str7
	.asciz	"expected pointer <0x%p> but was <0x%p>"

L___func__.CuSuiteAdd:                  ## @__func__.CuSuiteAdd
	.asciz	"CuSuiteAdd"

L_.str8:                                ## @.str8
	.asciz	"CuTest.c"

L_.str9:                                ## @.str9
	.asciz	"testSuite->count < MAX_TEST_CASES"

L_.str10:                               ## @.str10
	.asciz	"F"

L_.str11:                               ## @.str11
	.asciz	"."

L_.str12:                               ## @.str12
	.asciz	"\n\n"

L_.str13:                               ## @.str13
	.asciz	"test"

L_.str14:                               ## @.str14
	.asciz	"tests"

L_.str15:                               ## @.str15
	.asciz	"OK (%d %s)\n"

L_.str16:                               ## @.str16
	.asciz	"There was 1 failure:\n"

L_.str17:                               ## @.str17
	.asciz	"There were %d failures:\n"

L_.str18:                               ## @.str18
	.asciz	"%d) %s: %s\n"

L_.str19:                               ## @.str19
	.asciz	"\n!!!FAILURES!!!\n"

L_.str20:                               ## @.str20
	.asciz	"Runs: %d "

L_.str21:                               ## @.str21
	.asciz	"Passes: %d "

L_.str22:                               ## @.str22
	.asciz	"Fails: %d\n"

L_.str23:                               ## @.str23
	.asciz	"%s:%d: "


.subsections_via_symbols
