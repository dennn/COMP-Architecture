###############################################
# Program to test superscalar features
# The 3rd ALU operation should finish before 
# the 2nd
###############################################

start: 
	LDR r2, #10
	LDR r3, #5
	MUL r1, r2, r3
	ADD r4, r1, #5
	ADD r6, r2, #1