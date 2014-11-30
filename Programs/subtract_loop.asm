start:
	LDR r2, #10

loop:
	SUB r2, #1
	BNE r2, #0, loop

end:
	HALT


