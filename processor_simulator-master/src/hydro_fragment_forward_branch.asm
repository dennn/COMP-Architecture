#################################
####### HYDRO-FRAGMENT ##########
#################################

##############################
# @author: will williams
# University of Bristol
# gwillwill@gmail.com
##############################


main:   ADDI R20, R0, 6         # q
        ADDI R21, R0, 2         # r
        ADDI R22, R0, 9         # t

        ADDI R4, R0, 0          # k
        ADDI R5, R0, 1          # l
        ADDI R6, R0, 10         # loop max
        ADDI R7, R0, 6          # n
        

for:    LD  R10, y, R4          # y[k]

        ADDI R11, R4, 10        # k+10
        LD R12, z, R11          # z[k+10]

        ADDI R13, R4, 11        # k+11
        LD R14, z, R13          # z[k+11]

        BLTH R21, R20, mul

mulret: ADD R17, R15, R16       # r*z[k+1] + t*z[k+11]
        
        MUL R18, R10, R17       # y[k] * (r*z[k+1] + t*z[k+11])
        
        ADD R19, R20, R18       # q + y[k] * (r*z[k+10] + t*z[k+11])
        STR R19, x, R4          # store result

        ADD R4, R4, 1           # loop managment
        BLTH R4, R7, for
        ADDI R4, R0, 0
        ADD R5, R5, 1
        BLTH R5, R6, for

end:    BREAK 0

mul:    MUL R15, R21, R12       # r*z[k+1]
        MUL R16, R22, R14       # t*z[k+11]
        B mulret

y:      .word 4
        .word 10
        .word 8
        .word 6
        .word 9
        .word 31

z:      .word 16
        .word 27
        .word 5
        .word 32
        .word 1
        .word 5
        .word 8
        .word 19
        .word 2
        .word 11
        .word 3
        .word 9
        .word 8
        .word 6
        .word 9
        .word 31
        .word 7

x:
