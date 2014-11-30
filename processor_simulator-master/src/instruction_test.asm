##############################
##### INSTRUCTION TEST #######
# Iterate through all instruction
# types to ensure that the
# simulator works correctly
##############################
##############################

##############################
# @author: will williams
# University of Bristol
# gwillwill@gmail.com
##############################

ADDI R2, R0, 88 #R2 = 88
ADDI R1, R0, 1  #R1 = 1
ADD R1, R1, R1  #R1 = 2


MOV R1, R2      #R1 = 88

NEG R1, R1      #R1 = -88

SUB R1, R1, R2  #R1= -176
SUBI R2, R2, 2  #R2= 86

##########################
##########################

ADDI R4, R0, 2
SL R4, R4, 2
SL R4, R4, 2
SR R4, R4, 2

MUL R4, R4, R4

ADDI R8, R0, 15
ADDI R9, R0, 8738
AND R7, R8, R9 #R10 = 2
NOT R7, R7
NEG R7, R7


BREAK
