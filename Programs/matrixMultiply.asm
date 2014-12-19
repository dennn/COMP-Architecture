###############################################
# Program that carries out a matrix multiplication
# [12]     			  [84 24 120]
# [6]   *  [7 2 10] = [42 12 60]
# [3] 				  [21 6 30]	
###############################################
# Matrix counter
LDR R1, #0
# outer
LDR R2, #0

outerloop:
	# inner
	LDR R3, #0
	# Check if we're bigger than the matrix size (n - 1)
	BGT end, R2, #2
	LDR R6, [matrixA], R2
	ADD R2, R2, #1

innerloop:
	# Check if we're bigger than the matrix size (n - 1)
	BGT outerloop, R3, #2
	LDR R7, [matrixB], R3
	MUL R5, R6, R7
	STR R5, [matrixResult], R1
	ADD R1, R1, #1
	ADD R3, R3, #1
	B innerloop

end:
	HALT

matrixA: 
	.data 12
	.data 6
	.data 3

matrixB:
	.data 7
	.data 2
	.data 10

matrixResult: