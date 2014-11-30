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
	
        XOR R9, R8, R7          
        STR R9, a, R5           # A[i] = r7 + r8

        ADDI R5, R5, 1          # i++
        SUB R3, R3, 1
        NOP
        B for

end:    BREAK 0

b:      .word 66
        .word 31
        .word 23
        .word 11
        .word 3
        .word 58
        .word 93
        .word 26
        .word 17
        .word 41

c:      .word 14
        .word 22
        .word 23
        .word 24
        .word 25
        .word 26
        .word 27
        .word 28
        .word 29
        .word 30

a:
