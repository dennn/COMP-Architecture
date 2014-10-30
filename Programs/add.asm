start:
	LDR r2, #10

loop:
	SUB r2, #1
	CMP r0, r2, #0
	BNE r0, loop

end:
	HALT


