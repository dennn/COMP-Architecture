start:
	LDR r2, #10

loop:
	SUB r2, r2, #1
	BNE loop, r2, #0

end:
	HALT


