Factorial:
	move $fp $sp
	sw $ra 0($sp)
	addiu $sp $sp -40
	jal System.out.println
	lw $ra 40($sp)
	addiu $sp $sp 40
	lw $fp 0($sp)
	jr $ra
Fac:
ComputeFac:
	li $a0 0
:
	move $fp $sp
	sw $ra 0($sp)
	addiu $sp $sp -4
	li $a0 0
	sw $a0 0($sp)
	addiu $sp $sp -4
	li $a0 0
	sw $a0 0($sp)
	addiu $sp $sp -4
	lw $ra 4($sp)
	addiu $sp $sp 12
	lw $fp 0($sp)
	jr $ra
