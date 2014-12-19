###############################################
# Program to compute the factorial of a number
###############################################

main: 
	# Counter
	ADD R1, R0, #1 
	# Result
	ADD R2, R0, #1
	# N
	ADD R3, R0, #4

loop:
	BGT end, R1, R3
	MUL R2, R2, R1
	ADD R1, R1, #1
	B loop

end:
	HALT