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
for:    LD  R7, a, R4
        LD  R8, b, R4
        MUL R9, R8, R7          
        ADD R10, R10, R9
        ADD R4, R4, 1
        BLTH R4, R5, for

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
