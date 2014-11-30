public class ExecutionUnitLS {
	
	public static Instruction currentExecuting;
	public static Instruction nextExecuting;
	
	public static boolean freeForDispatch;
	
	ExecutionUnitLS()
	{
		currentExecuting = null;
		nextExecuting = null;
		freeForDispatch = true;
	}
	

	public static void issueInstruction(Instruction in) {
		if(in!=null && (freeForDispatch==false))
		{
			System.err.println("Sending an instruction to LS when it appears busy.");
		}
		
		if(in==null && currentExecuting==null)
			Simulator.numberOfNullsInEUs++;
	
		if (in != null) {
			freeForDispatch = false;
			if(in.instructionType==0) Simulator.clearScoreboardBit(in.destinationRegister); //if writing to a register then it has to be marked in the scoreboard after issue
			if (in.instruction.equals("STR"))
				str(in);
			else if (in.instruction.equals("LD"))
				ld(in);
			else if (in.instruction.equals("BREAK"))
				breakcmd(in);
			else if (in.instruction.equals("NOP"))
				return;
			else {
				System.err.println("Error in LS EXECUTION UNIT:\nInstruction not defined on this processor: " + in.instruction);
				System.exit(0);
			}
			currentExecuting = in;
			completeExecution();
		}
	}

	// Circulate results to reservation stations
	// Send the result to be picked up by WriteBack
	public static void completeExecution() {
		// Send to WB
//		if(currentExecuting!=null)
//		{
//			ReservationStationALU1.circulateEUResult(currentExecuting);
//			ReservationStationALU2.circulateEUResult(currentExecuting);
//			ReservationStationLS.circulateEUResult(currentExecuting);
//			ReservationStationBranch.circulateEUResult(currentExecuting);
//		}
		nextExecuting = currentExecuting;
		freeForDispatch = true;
	}
	
	private static void breakcmd(Instruction in) {
		// do this at writeback
	}

	private static void str(Instruction in) {
		int o1 = Integer.parseInt(in.workingOperands.get(0));
		in.result = o1;
	}

	private static void ld(Instruction in) {
		int o2 = Integer.parseInt(in.workingOperands.get(1));
		int o3 = Integer.parseInt(in.workingOperands.get(2));
		in.result = Simulator.memory[o2+o3];
	}
}
