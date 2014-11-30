##############################
######## VECTOR ADD ##########
##############################

##############################
# @author: will williams
# University of Bristol
# gwillwill@gmail.com
##############################

##############################

# in C:

#   for( int i = 0; i < 10; i++ )
#   {
#       A[ i ] = B[ i ] + C[ i ];
#   }

##############################


main:   ADDI R3, R0, 9          # i_max =10

        ADDI R5, R0, 0          # i = 0
      
for:    BLTH R3,R0,end
        
        LD  R7, b, R5           # r7 = B[i]
        LD  R8, c, R5           # r8 = C[i]
	
        ADD R9, R8, R7          
        STR R9, a, R5           # A[i] = r7 + r8

        ADDI R5, R5, 1          # i++
        SUB R3, R3, 1

        B for

end:    BREAK 0

b:      .word 1
        .word 2
        .word 3
        .word 4
        .word 5
        .word 6
        .word 7
        .word 8
        .word 9
        .word 10

c:      .word 100
        .word 200
        .word 300
        .word 400
        .word 500
        .word 600
        .word 700
        .word 800
        .word 900
        .word 100

a:
