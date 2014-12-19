###############################################
# Program to test register loading
###############################################

start: 
	LDR r2, #10
	STR r2, [#1]
	ADD r2, r2, #5
	ADD r2, r2, #6
	STR r2, [#1]
	STR #20, [#2]
	LDR r5, [#1], #1