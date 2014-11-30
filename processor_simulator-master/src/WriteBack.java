import java.util.ArrayList;

public class WriteBack {
	
		static ArrayList<Instruction> currentInstructions = null; 		// entries in ROB to retire
		static ArrayList<Instruction> recentInstructionsForROB = null;  // results to update ROB with

		WriteBack()
		{
			currentInstructions = new ArrayList<Instruction>();
			recentInstructionsForROB = new ArrayList<Instruction>();
		}
		
		public static void getResultsFromEUsIntoROB()
		{
			if (ExecutionUnitALU1.nextExecuting!=null)
			{
				recentInstructionsForROB.add(ExecutionUnitALU1.nextExecuting);
				ExecutionUnitALU1.nextExecuting = null;
				ExecutionUnitALU1.currentExecuting = null;
			}
			
			if (ExecutionUnitALU2.nextExecuting!=null)
			{
				recentInstructionsForROB.add(ExecutionUnitALU2.nextExecuting);
				ExecutionUnitALU2.nextExecuting = null;
				ExecutionUnitALU2.currentExecuting = null;
			}

			if (ExecutionUnitLS.nextExecuting!=null)
			{
				recentInstructionsForROB.add(ExecutionUnitLS.nextExecuting);
				ExecutionUnitLS.nextExecuting = null;
				ExecutionUnitLS.currentExecuting = null;
			}
			
			if (ExecutionUnitBranch.nextExecuting!=null)
			{
				recentInstructionsForROB.add(ExecutionUnitBranch.nextExecuting);
				ExecutionUnitBranch.nextExecuting = null;
				ExecutionUnitBranch.currentExecuting = null;
			}
			
			for(Instruction i : recentInstructionsForROB)
			{
				for(ROBEntry e : Simulator.ROB)
				{
					if (e.inst.equals(i))
					{
						e.status = 2;
					}
				}
			}
			recentInstructionsForROB = new ArrayList<Instruction>();
		}
		
		public static void getResultsToRetire()
		{	
			ArrayList<ROBEntry> todelete = new ArrayList<ROBEntry>();
			int tempPC = Simulator.registerFile[31];
			boolean nextFound = true;
			
			while(nextFound)
			{
				nextFound = false;
				for(ROBEntry robe : Simulator.ROB)
				{
					if (robe.status == 2 && robe.inst.memoryAddress == tempPC){
						todelete.add(robe);
						currentInstructions.add(robe.inst);
						tempPC++;
						nextFound = true;
					}
				}
			}
			
			for(ROBEntry robe : todelete)
				Simulator.ROB.remove(robe);
		}
		
		public static void deleteSpeculativeInstsFromROB()
		{
			ArrayList<ROBEntry> todelete = new ArrayList<ROBEntry>();
			for(ROBEntry robe : Simulator.ROB)
			{
				if (robe.inst.specualtive == true){
					todelete.add(robe);
				}
			}
			for(ROBEntry robe : todelete)
				Simulator.ROB.remove(robe);
		}
		
		public static void deleteSpeculativeInstsFromReservationStations()
		{
			ArrayList<ReservationStationEntry> todelete = new ArrayList<ReservationStationEntry>();
			for(ReservationStationEntry rset: ReservationStationALU1.rseSet)
			{
				if(rset.inst.specualtive) todelete.add(rset);					
			}
			ReservationStationALU1.rseSet.removeAll(todelete);
			
			todelete = new ArrayList<ReservationStationEntry>();
			for(ReservationStationEntry rset: ReservationStationALU2.rseSet)
			{
				if(rset.inst.specualtive) todelete.add(rset);					
			}
			ReservationStationALU2.rseSet.removeAll(todelete);
			
			todelete = new ArrayList<ReservationStationEntry>();
			for(ReservationStationEntry rset: ReservationStationLS.rseSet)
			{
				if(rset.inst.specualtive) todelete.add(rset);					
			}
			ReservationStationLS.rseSet.removeAll(todelete);
			
			todelete = new ArrayList<ReservationStationEntry>();
			for(ReservationStationEntry rset: ReservationStationBranch.rseSet)
			{
				if(rset.inst.specualtive) todelete.add(rset);					
			}
			ReservationStationBranch.rseSet.removeAll(todelete);
		}
		
		public static void affirmSpeculativeInsts() {
			for(ROBEntry robe : Simulator.ROB)
				robe.inst.specualtive = false;
			
			for(ReservationStationEntry rset: ReservationStationALU1.rseSet)
				rset.inst.specualtive=false;					
			
			for(ReservationStationEntry rset: ReservationStationALU2.rseSet)
				rset.inst.specualtive=false;					
			
			for(ReservationStationEntry rset: ReservationStationLS.rseSet)
				rset.inst.specualtive=false;										
			
			for(ReservationStationEntry rset: ReservationStationBranch.rseSet)
				rset.inst.specualtive=false;										
	
			for(Instruction i : FetchUnit.currentIssue)
				i.specualtive=false;
			
			for(Instruction i : FetchUnit.nextIssue)
				i.specualtive=false;

			for(Instruction i : Decoder.currentDecodedInstructionSS)
				i.specualtive=false;

			for(Instruction i : Decoder.nextDecodedInstructionSS)
				i.specualtive=false;

			if (Decoder.issue[0] != null) Decoder.issue[0].specualtive=false;
			if (Decoder.issue[1] != null) Decoder.issue[1].specualtive=false;
			if (Decoder.issue[2] != null) Decoder.issue[2].specualtive=false;
			if (Decoder.issue[3] != null) Decoder.issue[3].specualtive=false;		
			
		}	
		
		public static void writeResults() {

			getResultsFromEUsIntoROB();
			getResultsToRetire();
			
			// Iterate over instructions to retire
			if (currentInstructions != null) {
				for (Instruction in : currentInstructions) {
					Simulator.instructionCount++;
					int origPC = Simulator.registerFile[31];

					System.out.println("Retiring " + in.instruction + " on line " + in.memoryAddress);
					if (in != null && Simulator.continueExecution) {
						if (in.instruction.equals("ADD"))
							add(in);
						else if (in.instruction.equals("ADDI"))
							add(in);
						else if (in.instruction.equals("MOV"))
							mov(in);
						else if (in.instruction.equals("MUL"))
							mul(in);
						else if(in.instruction.equals("DIV"))
							div(in);
						else if (in.instruction.equals("STR"))
							str(in);
						else if (in.instruction.equals("BEQ"))
							beq(in);
						else if (in.instruction.equals("BNE"))
							bne(in);
						else if (in.instruction.equals("LD"))
							ld(in);
						else if (in.instruction.equals("B"))
							b(in);
						else if (in.instruction.equals("BLTH"))
							blth(in);
						else if (in.instruction.equals("SUB"))
							sub(in);
						else if (in.instruction.equals("SUBI"))
							sub(in);
						else if (in.instruction.equals("NOP"))
							return;
						else if (in.instruction.equals("XOR"))
							xor(in);
						else if (in.instruction.equals("AND"))
							and(in);
						else if (in.instruction.equals("OR"))
							or(in);
						else if (in.instruction.equals("NOT"))
							not(in);
						else if (in.instruction.equals("SL"))
							sl(in);
						else if (in.instruction.equals("SR"))
							sr(in);
						else if (in.instruction.equals("NEG"))
							neg(in);
						else if (in.instruction.equals("BREAK"))
							breakCmd(in);
						else {
							System.err
									.println("Error in EXECUTION UNIT:\nInstruction not defined on processor: "
											+ in.instruction);
							System.exit(0);
						}
						
						if(in.instructionType==0)
						{
							ReservationStationALU1.circulateEUResult(in);
							ReservationStationALU2.circulateEUResult(in);
							ReservationStationLS.circulateEUResult(in);
							ReservationStationBranch.circulateEUResult(in);
						}
						
						if (origPC==Simulator.registerFile[31] && !Simulator.isStalled) 
						{
							Simulator.registerFile[31]++;
						}
					}
				currentInstructions = new ArrayList<Instruction>();
			}
		}
	}

		private static void breakCmd(Instruction in) {
			System.out.println("BREAK CALLED - HALTING....");
			Simulator.continueExecution = false;
			Simulator.isStalled = true;
		}

		private static void sr(Instruction in) {
			int o1 = Integer.parseInt(in.workingOperands.get(0));
			Simulator.registerFile[o1] = in.result;
			Simulator.scoreboard[o1] = true;
		}

		private static void sl(Instruction in) {
			int o1 = Integer.parseInt(in.workingOperands.get(0));
			Simulator.registerFile[o1] = in.result;
			Simulator.scoreboard[o1] = true;
		}

		private static void mov(Instruction in) {
			int o1 = Integer.parseInt(in.workingOperands.get(0));
			Simulator.registerFile[o1] = in.result;
			Simulator.scoreboard[o1] = true;
		}

		private static void mul(Instruction in) {
			int o1 = Integer.parseInt(in.workingOperands.get(0));
			Simulator.registerFile[o1] = in.result;
			Simulator.scoreboard[o1] = true;
		}
		
		private static void div(Instruction in) {
			int o1 = Integer.parseInt(in.workingOperands.get(0));
			Simulator.registerFile[o1] = in.result;
			Simulator.scoreboard[o1] = true;
		}

		private static void neg(Instruction in) {
			int o1 = Integer.parseInt(in.workingOperands.get(0));
			Simulator.registerFile[o1] = in.result;
			Simulator.scoreboard[o1] = true;
		}
		
		private static void not(Instruction in) {
			int o1 = Integer.parseInt(in.workingOperands.get(0));
			Simulator.registerFile[o1] = in.result;
			Simulator.scoreboard[o1] = true;
		}

		private static void or(Instruction in) {
			int o1 = Integer.parseInt(in.workingOperands.get(0));
			Simulator.registerFile[o1] = in.result;
			Simulator.scoreboard[o1] = true;
		}

		private static void and(Instruction in) {
			int o1 = Integer.parseInt(in.workingOperands.get(0));
			Simulator.registerFile[o1] = in.result;
			Simulator.scoreboard[o1] = true;
		}

		private static void xor(Instruction in) {
			int o1 = Integer.parseInt(in.workingOperands.get(0));
			Simulator.registerFile[o1] = in.result;
			Simulator.scoreboard[o1] = true;
		}

		private static void sub(Instruction in) {
			int o1 = Integer.parseInt(in.workingOperands.get(0));
			Simulator.registerFile[o1] = in.result;
			Simulator.scoreboard[o1] = true;
		}

		private static void blth(Instruction in) {
			int o1 = Integer.parseInt(in.workingOperands.get(0));
			int o2 = Integer.parseInt(in.workingOperands.get(1));
			
			if (o1<o2) Simulator.registerFile[31] = in.result;
			else Simulator.registerFile[31] = in.memoryAddress+1;
			
			Simulator.scoreboard[31] = true;
			if(in.mispredicted) Simulator.restartFromMispredictedBranch();
		}

		private static void str(Instruction in) {
			int o2 = Integer.parseInt(in.workingOperands.get(1));
			int o3 = Integer.parseInt(in.workingOperands.get(2));
			Simulator.memory[o2+o3] = in.result;		
		}

		private static void beq(Instruction in) {
			int o1 = Integer.parseInt(in.workingOperands.get(0));
			int o2 = Integer.parseInt(in.workingOperands.get(1));
			
			if (o1==o2) Simulator.registerFile[31] = in.result;
			else Simulator.registerFile[31] = in.memoryAddress+1;
			
			Simulator.scoreboard[31] = true;
			if(in.mispredicted) Simulator.restartFromMispredictedBranch();
		}

		private static void bne(Instruction in) {
			int o1 = Integer.parseInt(in.workingOperands.get(0));
			int o2 = Integer.parseInt(in.workingOperands.get(1));
			
			if (o1!=o2) Simulator.registerFile[31] = in.result;
			else Simulator.registerFile[31] = in.memoryAddress+1;
			
			Simulator.scoreboard[31] = true;
			if(in.mispredicted) Simulator.restartFromMispredictedBranch();
		}
		
		private static void ld(Instruction in) {
			int o1 = Integer.parseInt(in.workingOperands.get(0));
			Simulator.registerFile[o1] = in.result;
			Simulator.scoreboard[o1] = true;
		}

		private static void b(Instruction in) {
			Simulator.registerFile[31] = in.result;
			Simulator.scoreboard[31] = true;
			if(in.mispredicted) Simulator.restartFromMispredictedBranch(); //shouldnt need this
		}

		public static void add(Instruction in)
		{
			int o1 = Integer.parseInt(in.workingOperands.get(0));
			Simulator.registerFile[o1] = in.result;
			Simulator.scoreboard[o1] = true;
		}
}