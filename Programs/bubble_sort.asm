###############################################
# Program to sort an array of values using the 
# Bubble Sort Algorithm
###############################################

main: 
# outer counter
	ADD R2, #10
# inner counter 1
	ADD R3, #0
# inner counter 2
	ADD R4, #1
# number of elements
	ADD R5, #10

loop:
	BLT R2, #0, end

	LDR R6, [values], R3
	LDR R7, [values], R4

	BGT R6, R7, swapValues

swapRest:
	ADD R3, R3, #1
	ADD R4, R4, #1

	BLT R4, R5, loop
	ADD R3, R0, #0
	ADD R4, R0, #1
	SUB R2, #1
	B loop

swapValues:
	STR R6, [values], R4
	STR R7, [values], R3
	B swapRest

end:
	HALT

values: 
	.data 12
	.data 6
	.data 16
	.data 4
	.data 3
	.data 2
	.data 20
	.data 23
	.data -1
	.data 14