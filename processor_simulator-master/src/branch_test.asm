##############################
######## BRANCH TEST #########
##############################

##############################
# @author: will williams
# University of Bristol
# gwillwill@gmail.com
##############################

ADDI R2, R0, 5
ADDI R1, R0, 10
ADDI R9, R0, 11
ADDI R3, R0 , 1

main:   ADDI R3, R3, 1         # j =40
        BEQ R2,R3,branch1
        BEQ R1,R3,branch2
        BEQ R9,R3, end
        B main        

branch1:        MUL R7, R3, R3    
                B main

branch2:        MUL R22, R3, R3
                B end

end:    BREAK
