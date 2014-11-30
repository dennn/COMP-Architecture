##############################
######## FIBONNACCI ##########
##############################

##############################
# @author: will williams
# University of Bristol
# gwillwill@gmail.com
##############################

main:   ADDI R3, R0, 20         # j =40
        ADDI R4, R0, 2          # a = 8, memory locations
        ADDI R5, R0, 1          # b = 4
        ADDI R6, R0, 0          # c = 0
        
        ADDI R7, R0, 0          # t1 = 0, intermediary results
        ADDI R8, R0, 1          # t2 = 1
        
        STR R7, fib, R6         # fib[c] = t1
        STR R8, fib, R5         # fib[b] = t2

for:    BEQ R3,R4,end
        LD  R7, fib, R5
        LD  R8, fib, R6
	
        ADD R9, R8, R7          # fib[a] = t3
        STR R9, fib, R4

        ADDI R4, R4, 1
        ADDI R5, R5, 1
        ADDI R6, R6, 1

        B for

end:    BREAK 0

fib:
