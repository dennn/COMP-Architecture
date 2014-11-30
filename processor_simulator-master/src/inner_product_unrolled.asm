#################################
######## INNER PRODUCT ##########
#################################

##############################
# @author: will williams
# University of Bristol
# gwillwill@gmail.com
##############################

# NOTE: result in R10 should be 228

main:   ADDI R10, R0, 0         # result
        ADDI R4, R0, 0          # counter
        ADDI R5, R0, 10         # loop max
        
        LD  R7, a, R4           # 1
        LD  R8, b, R4
        MUL R9, R8, R7          
        ADD R10, R10, R9
        ADD R4, R4, 1
        
        LD  R7, a, R4           # 2
        LD  R8, b, R4
        MUL R9, R8, R7          
        ADD R10, R10, R9
        ADD R4, R4, 1

        LD  R7, a, R4           # 3
        LD  R8, b, R4
        MUL R9, R8, R7         #line 15 
        ADD R10, R10, R9
        ADD R4, R4, 1

        LD  R7, a, R4           # 4
        LD  R8, b, R4
        MUL R9, R8, R7          
        ADD R10, R10, R9
        ADD R4, R4, 1

        LD  R7, a, R4           # 5
        LD  R8, b, R4
        MUL R9, R8, R7          
        ADD R10, R10, R9
        ADD R4, R4, 1

        LD  R7, a, R4           # 6
        LD  R8, b, R4
        MUL R9, R8, R7          
        ADD R10, R10, R9
        ADD R4, R4, 1

        LD  R7, a, R4           # 7
        LD  R8, b, R4
        MUL R9, R8, R7          
        ADD R10, R10, R9
        ADD R4, R4, 1

        LD  R7, a, R4           # 8
        LD  R8, b, R4
        MUL R9, R8, R7          
        ADD R10, R10, R9
        ADD R4, R4, 1

        LD  R7, a, R4           # 9
        LD  R8, b, R4
        MUL R9, R8, R7          
        ADD R10, R10, R9
        ADD R4, R4, 1

        LD  R7, a, R4           # 10
        LD  R8, b, R4
        MUL R9, R8, R7          
        ADD R10, R10, R9
        ADD R4, R4, 1

        LD  R7, a, R4           # 11
        LD  R8, b, R4
        MUL R9, R8, R7          
        ADD R10, R10, R9
        ADD R4, R4, 1

end:    BREAK 0

a:      .word 1
        .word 7
        .word 3
        .word 2
        .word 5
        .word 4
        .word 10
        .word 8
        .word 6
        .word 9

b:      .word 16
        .word 27
        .word 5
        .word 1
        .word 5
        .word 8
        .word 2
        .word -1
        .word 3
        .word -9

c:
