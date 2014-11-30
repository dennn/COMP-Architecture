##############################
######## BUBBLE SORT #########
##############################

##############################
# @author: will williams
# University of Bristol
# gwillwill@gmail.com
##############################

main:   ADDI R3, R0, 10         # outer counter
        ADDI R5, R0, 0          # inner counter 1
        ADDI R6, R0, 1          # inner counter 2
        ADDI R20, R0, 10
      
for:    BLTH R3,R0,end
                
        LD  R7, b, R5           
        LD  R8, b, R6            

        BLTH R8, R7, swap

swapr:  ADD R5, R5, 1        
        ADD R6, R6, 1

        BLTH R6, R20, for
        ADDI R5, R0, 0          # inner counter 1
        ADDI R6, R0, 1          # inner counter 2
        SUB R3, R3, 1
        B for

end:    BREAK 0

swap:   STR R7, b, R6
        STR R8, b, R5
        B swapr

b:      .word 1
        .word 7
        .word 3
        .word 2
        .word 5
        .word 4
        .word 10
        .word 8
        .word 6
        .word 9

a:
