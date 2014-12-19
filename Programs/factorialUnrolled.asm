###############################################
# Program to compute the factorial of a number
# in an unrolled fashion. This will take advantage
# of multiple execution units
###############################################

main: 
	# Counter
	ADD R1, R0, #1 
	# Result
	ADD R2, R0, #1
	# Unrolled loop for n = 4
	MUL R2, R2, R1
	ADD R1, R1, #1
	MUL R2, R2, R1
	ADD R1, R1, #1
	MUL R2, R2, R1
	ADD R1, R1, #1
	MUL R2, R2, R1
	ADD R1, R1, #1

end:
	HALT