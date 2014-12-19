###############################################
# Program to calculate vector multiplication
###############################################

main: 
	# Number of elements (n-1)
	LDR R1, #4 
	# i
	LDR R2, #0

loop:
	BGT end, R2, R1

	LDR R3, [a], R2
	LDR R4, [b], R2

	MUL R5, R3, R4
	STR R5, [c], R2

	ADD R2, R2, #1

	B loop

end:
	HALT

a: 
	.data 1
	.data 2
	.data 3
	.data 4
	.data 5

b:
	.data 50
	.data 40
	.data 30
	.data 20
	.data 10

c: