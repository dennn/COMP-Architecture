#################################
####### F_p inversion ##########
# Input: Prime p and a \in [1,p-1]
# Output: a^{-1} mod p
#################################

##############################
# @author: will williams
# University of Bristol
# gwillwill@gmail.com
##############################

# a = 24, a^{-1}=631
# a = 14, a^{-1}=57

main:   ADDI R1, R0, 1
        ADDI R2, R0, 797        # p
        ADDI R3, R0, 24         # a
        ADDI R30, R0, 1         # temp

#STEP ONE
        MOV R4, R3              # u
        MOV R5, R2              # v
#STEP TWO
        ADDI R11, R0, 1         # x_1 = 1
        ADDI R12, R0, 0         # x_2 = 0

#STEP THREE

#STEP THREE POINT ONE
start:  DIV R13, R5, R4         # q = lower(v/u)
        MUL R14, R13, R4        # qu
        ADDI R30, R30, 1        # temp++
        SUB R15, R5, R14        # r = v-qu
        ADDI R30, R30, 1        # temp++
        MUL R16, R13, R11       # q(x_1)
        SUB R17, R12, R16       # x = x_2 - q(x_1)
        ADDI R30, R30, 1        # temp++
#STEP THREE POINT TWO
        MOV R5, R4              # v = u
        MOV R4, R15             # u = r
        MOV R12, R11            # x_2 = x_1
        MOV R11, R17            # x_1 = x

#STEP FOUR (navie modular reduction)
        BNE R1, R4, start
        BLTH R11, R0, reduceup
        BLTH R2, R11, reducedown

end:    BREAK 0

reduceup:       ADD R11, R11, R2
                BLTH R11, R0, reduceup
                B end

reducedown:     SUB R11, R11, R2
                BLTH R2, R11, reducedown
                B end

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
