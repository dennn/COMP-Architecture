import java.io.IOException;


public class Print {

	public static void printState()
	{
		System.out.println("////////////////////////////");
		System.out.println("*** CLOCK CYCLE = " + Simulator.clockCycles + " ***");
		System.out.println("////////////////////////////\n");
		
		System.out.println("--------- FETCH --------\n");
		if(FetchUnit.currentIssue.size() == 0) System.out.println("empty buffer");
		for(int i=0; i< FetchUnit.currentIssue.size(); i++)
		{
			Instruction inst = FetchUnit.currentIssue.get(i);
			if(inst!=null)
			{
			System.out.print("["+i+"] = " + inst.instruction);
			if(inst.specualtive) System.out.print("*");
			System.out.print(" || ");
			}
			else
			{
				System.out.print("["+i+"] = null");
				System.out.print(" || ");
			}
		}
		
		System.out.println("\n\n--------- DECODE --------\n");
		if(Decoder.currentDecodedInstructionSS.size() == 0) System.out.print("empty buffer");
		for(int i=0; i< Decoder.currentDecodedInstructionSS.size(); i++)
		{
			Instruction inst = Decoder.currentDecodedInstructionSS.get(i);
			
			if(inst!=null)
			{
				System.out.print("["+i+"] = " + inst.instruction + " ");
				for(String operand : inst.workingOperands)
				{
					System.out.print(operand + ", ");
				}
				if(inst.specualtive) System.out.print("*");
				System.out.print(" || ");
			}else{
				System.out.print("["+i+"] = null");
				System.out.print(" || ");
			}
		}
		
		System.out.println("\n\n--------- ISSUE --------\n");
		for(int i=0; i<4; i++)
		{
			Instruction inst = Decoder.issue[i];
			
			if(inst!=null)
			{
				System.out.print("["+i+"] = " + inst.instruction + " ");
				for(String operand : inst.workingOperands)
				{
					System.out.print(operand + ", ");
				}
				if(inst.specualtive) System.out.print("*");
				System.out.print(" || ");
			}else{
				System.out.print("["+i+"] = null");
				System.out.print(" || ");
			}
		}
		
		System.out.println("\n\n--------- RESERVATION STATIONS --------\n");
		
		System.out.print("[ALU1] ");
		if(ReservationStationALU1.rseSet.size() == 0) System.out.print("empty station");
		for(ReservationStationEntry rse : ReservationStationALU1.rseSet)
		{	
			if(rse.inst!=null)
			{
				System.out.print("=> " + rse.inst.instruction + " ");
				for(String operand : rse.inst.workingOperands)
				{
					System.out.print(operand + ", ");
				}
				for(boolean v : rse.validBits)
				{
					System.out.print("(" + v + ")");
				}
				if(rse.inst.specualtive) System.out.print("*");
			}
			else
			{
				System.out.print("=> null");
			}
			System.out.print(" || ");
		}
		
		System.out.print("\n\n[ALU2] ");
		if(ReservationStationALU2.rseSet.size() == 0) System.out.print("empty station");
		for(ReservationStationEntry rse : ReservationStationALU2.rseSet)
		{	
			if(rse.inst!=null)
			{
				System.out.print("=> " + rse.inst.instruction + " ");
				for(String operand : rse.inst.workingOperands)
				{
					System.out.print(operand + ", ");
				}
				for(boolean v : rse.validBits)
				{
					System.out.print("(" + v + ")");
				}
				if(rse.inst.specualtive) System.out.print("*");
			}
			else
			{
				System.out.print("=> null");
			}
			System.out.print(" || ");
		}
		
		System.out.print("\n\n[LS] ");
		if(ReservationStationLS.rseSet.size() == 0) System.out.print("empty station");
		for(ReservationStationEntry rse : ReservationStationLS.rseSet)
		{	
			if(rse.inst!=null)
			{
				System.out.print("=> " + rse.inst.instruction + " ");
				for(String operand : rse.inst.workingOperands)
				{
					System.out.print(operand + ", ");
				}
				for(boolean v : rse.validBits)
				{
					System.out.print("(" + v + ")");
				}
				if(rse.inst.specualtive) System.out.print("*");
			}
			else
			{
				System.out.print("=> null");
			}
			System.out.print(" || ");
		}
		
		System.out.print("\n\n[BRANCH] ");
		if(ReservationStationBranch.rseSet.size() == 0) System.out.println("empty station");
		for(ReservationStationEntry rse : ReservationStationBranch.rseSet)
		{	
			if(rse.inst!=null)
			{
				System.out.print("=> " + rse.inst.instruction + " ");
				for(String operand : rse.inst.workingOperands)
				{
					System.out.print(operand + ", ");
				}
				for(boolean v : rse.validBits)
				{
					System.out.print("(" + v + ")");
				}
				if(rse.inst.specualtive) System.out.print("*");
			}
			else
			{
				System.out.print("=> null");
			}
			System.out.print(" || ");
		}
		
		System.out.println("\n--------- EXECUTE --------\n");
		
		Instruction inst = ExecutionUnitALU1.currentExecuting;
		if(inst!=null)
		{
			System.out.print("[ALU1] = " + inst.instruction + " ");
			for(String operand : inst.workingOperands)
			{
				System.out.print(operand + ", ");
			}
		}
		else
		{
			System.out.print("[ALU1] = null");
		}
		System.out.print(" || ");
				
		Instruction inst2 = ExecutionUnitALU2.currentExecuting;
		if(inst2!=null)
		{
			System.out.print("[ALU2] =" + inst2.instruction + " ");
			for(String operand : inst2.workingOperands)
			{
				System.out.print(operand + ", ");
			}
		}
		else
		{
			System.out.print("[ALU2] = null");
		}
		System.out.print(" || ");
		
		Instruction inst3 = ExecutionUnitLS.currentExecuting;
		if(inst3!=null)
		{
			System.out.print("[LS] =" + inst3.instruction  + " ");
			for(String operand : inst3.workingOperands)
			{
				System.out.print(operand + ", ");
			}
		}
		else
		{
			System.out.print("[LS] = null");
		}
		System.out.print(" || ");
		
		Instruction inst4 = ExecutionUnitBranch.currentExecuting;
		if(inst4!=null)
		{
			System.out.print("[BRANCH] =" + inst4.instruction + " ");
			for(String operand : inst4.workingOperands)
			{
				System.out.print(operand + ", ");
			}
		}
		else
		{
			System.out.print("[BRANCH] = null");
		}
		System.out.print(" || ");
		
		System.out.println("\n\n--------- ROB --------\n");
		
		if(Simulator.ROB.size()==0)
		{
			System.out.println("empty buffer");
		}
		
		for(ROBEntry e : Simulator.ROB)
		{
			System.out.print(e.inst.instruction + " (" + e.status + ")");
			if(e.inst.specualtive) System.out.print("*");
			System.out.print(" || ");
		}
		
				
		
		System.out.println("\n\n--------- WRITEBACK (Regs) ----------\n");
		
		System.out.println("[0] " + Simulator.registerFile[0] + "(" + Simulator.scoreboard[0] + ")" + "\t[5] " + Simulator.registerFile[5] + "(" + Simulator.scoreboard[5] + ")" + "\t[10] " + Simulator.registerFile[10] + "(" + Simulator.scoreboard[10] + ")" + "\t[15] " + Simulator.registerFile[15] + "(" + Simulator.scoreboard[15] + ")" + "\t[20] " + Simulator.registerFile[20] + "(" + Simulator.scoreboard[20] + ")" + "\t[25] " + Simulator.registerFile[25] + "(" + Simulator.scoreboard[25] + ")" + "\t[30] " + Simulator.registerFile[30] + "(" + Simulator.scoreboard[30] + ")");
		System.out.println("[1] " + Simulator.registerFile[1] + "(" + Simulator.scoreboard[1] + ")" + "\t[6] " + Simulator.registerFile[6] + "(" + Simulator.scoreboard[6] + ")" + "\t[11] " + Simulator.registerFile[11] + "(" + Simulator.scoreboard[11] + ")" + "\t[16] " + Simulator.registerFile[16] + "(" + Simulator.scoreboard[16] + ")" + "\t[21] " + Simulator.registerFile[21] + "(" + Simulator.scoreboard[21] + ")" + "\t[26] " + Simulator.registerFile[26] + "(" + Simulator.scoreboard[26] + ")" + "\t[31] " + Simulator.registerFile[31] + "(" + Simulator.scoreboard[31] + ")");
		System.out.println("[2] " + Simulator.registerFile[2] + "(" + Simulator.scoreboard[2] + ")" + "\t[7] " + Simulator.registerFile[7] + "(" + Simulator.scoreboard[7] + ")" + "\t[12] " + Simulator.registerFile[12] + "(" + Simulator.scoreboard[12] + ")" + "\t[17] " + Simulator.registerFile[17] + "(" + Simulator.scoreboard[17] + ")" + "\t[22] " + Simulator.registerFile[22] + "(" + Simulator.scoreboard[22] + ")" + "\t[27] " + Simulator.registerFile[27] + "(" + Simulator.scoreboard[27] + ")");
		System.out.println("[3] " + Simulator.registerFile[3] + "(" + Simulator.scoreboard[3] + ")" + "\t[8] " + Simulator.registerFile[8] + "(" + Simulator.scoreboard[8] + ")" + "\t[13] " + Simulator.registerFile[13] + "(" + Simulator.scoreboard[13] + ")" + "\t[18] " + Simulator.registerFile[18] + "(" + Simulator.scoreboard[18] + ")" + "\t[23] " + Simulator.registerFile[23] + "(" + Simulator.scoreboard[23] + ")" + "\t[28] " + Simulator.registerFile[28] + "(" + Simulator.scoreboard[28] + ")");
		System.out.println("[4] " + Simulator.registerFile[4] + "(" + Simulator.scoreboard[4] + ")" + "\t[9] " + Simulator.registerFile[9] + "(" + Simulator.scoreboard[9] + ")" + "\t[14] " + Simulator.registerFile[14] + "(" + Simulator.scoreboard[14] + ")" + "\t[19] " + Simulator.registerFile[19] + "(" + Simulator.scoreboard[19] + ")" + "\t[24] " + Simulator.registerFile[24] + "(" + Simulator.scoreboard[24] + ")" + "\t[29] " + Simulator.registerFile[29] + "(" + Simulator.scoreboard[29] + ")");
		
		System.out.println("\n\n--------- WRITEBACK (Memory) ----------\n");
		
		System.out.println("[0] " + Simulator.memory[0] + "\t[5] " + Simulator.memory[5] + "\t[10] " + Simulator.memory[10] + "\t[15] " + Simulator.memory[15] + "\t[20] " + Simulator.memory[20] + "\t[25] " + Simulator.memory[25] + "\t[30] " + Simulator.memory[30]);
		System.out.println("[1] " + Simulator.memory[1] + "\t[6] " + Simulator.memory[6] + "\t[11] " + Simulator.memory[11] + "\t[16] " + Simulator.memory[16] + "\t[21] " + Simulator.memory[21] + "\t[26] " + Simulator.memory[26] + "\t[31] " + Simulator.memory[31]);
		System.out.println("[2] " + Simulator.memory[2] + "\t[7] " + Simulator.memory[7] + "\t[12] " + Simulator.memory[12] + "\t[17] " + Simulator.memory[17] + "\t[22] " + Simulator.memory[22] + "\t[27] " + Simulator.memory[27]);
		System.out.println("[3] " + Simulator.memory[3] + "\t[8] " + Simulator.memory[8] + "\t[13] " + Simulator.memory[13] + "\t[18] " + Simulator.memory[18] + "\t[23] " + Simulator.memory[23] + "\t[28] " + Simulator.memory[28]);
		System.out.println("[4] " + Simulator.memory[4] + "\t[9] " + Simulator.memory[9] + "\t[14] " + Simulator.memory[14] + "\t[19] " + Simulator.memory[19] + "\t[24] " + Simulator.memory[24] + "\t[29] " + Simulator.memory[29]);
		
		System.out.println("\n/////  PRESS ANY KEY TO STEP //////");
		try {
			if(System.in.read()=='f') Simulator.stepMode=false;
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		try {
			Runtime.getRuntime().exec("clear");
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		
	}
	
	
}
