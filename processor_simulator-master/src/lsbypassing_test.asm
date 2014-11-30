######################################
##### LD/STR BYPASSING TEST ##########
# Check register renaming
######################################
######################################

# NOTE: ALU must have multicycle for
# multiplication turned on

######################################
# @author: will williams
# University of Bristol
# gwillwill@gmail.com
######################################

ADDI R2, R0, 2
ADDI R3, R0, 3
ADDI R4, R0, 4
ADDI R5, R0, 5
ADDI R6, R0, 6
ADDI R20, R0, 7

MUL R1, R2, R3          # Opportunity for load to overtake other load: SHOULD ALLOW [DONE]
LD  R7, b, R1
LD  R7, b, R3

ADD R7, R7, R7          # Filler
ADD R8, R7, R7
ADD R18, R17, R17
ADD R19, R17, R17


MUL R1, R2, R2          # Opportunity for str to overtake ld: SHOULD BLOCK [DONE]
LD  R7, b, R1
STR  R7, b, R3

BREAK 0

b:      .word 1
        .word 7
        .word 3
        .word 2
        .word 5
        .word 17
        .word 18
