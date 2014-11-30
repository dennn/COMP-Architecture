##############################
##### RENAMING TEST ##########
# Check register renaming
##############################
##############################

##############################
# @author: will williams
# University of Bristol
# gwillwill@gmail.com
##############################

ADDI R2, R0, 2
ADDI R3, R0, 3
ADDI R4, R0, 4
ADDI R5, R0, 5
ADDI R6, R0, 6
ADDI R20, R0, 7

MUL R1, R2, R3
ADD R2, R4, R5
SUB R7, R2, R6
SUB R8, R2, R6

