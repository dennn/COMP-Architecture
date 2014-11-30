import java.util.ArrayList;

public class ExecutionUnitBranch {
	
	public static Instruction currentExecuting;
	public static Instruction nextExecuting;
	
	public static boolean freeForDispatch;
	
	ExecutionUnitBranch()
	{
		currentExecuting = null;
		nextExecuting = null;
		freeForDispatch = true;
	}
	
	public static void issueInstruction(Instruction in) {	
		if(in!=null && (freeForDispatch==false))
		{
			System.err.println("Sending an instruction to BRANCH when it appears busy.");
		}
		
		if(in==null && currentExecuting==null)
			Simulator.numberOfNullsInEUs++;
	
		if (in != null) {
			freeForDispatch = false;
			if(in.instructionType==0) Simulator.clearScoreboardBit(in.destinationRegister); //if writing to a register then it has to be marked in the scoreboard after issue
			if (in.instruction.equals("BEQ"))
				beq(in);
			else if (in.instruction.equals("B"))
				b(in);
			else if (in.instruction.equals("BLTH"))
				blth(in);
			else if (in.instruction.equals("BNE"))
				blth(in);
			else if (in.instruction.equals("NOP"))
				return;
			else {
				System.err
						.println("Error in BRANCH EXECUTION UNIT:\nInstruction not defined on this processor: "
								+ in.instruction);
				System.exit(0);
			}
			currentExecuting = in;
			completeExecution();
		}
	}

	// Send the result to be picked up by WriteBack
	public static void completeExecution() {		
		nextExecuting = currentExecuting;
		freeForDispatch = true;
		Simulator.totalNumberOfBranchPredictions++;
	}
	
	public static void broadcastBranchResult(boolean taken, Instruction in)
	{
		// Find permanent instruction in assembler
		Instruction perm=null;
		for(Instruction i: Simulator.assembler.getListOfInstructions())
		{
			if(in.memoryAddress==i.memoryAddress)
				perm = i;
		}
		if (perm == null){System.err.println("Could not find instruction to update branching history.");System.exit(1);}
		
		if(in.branchTaken == taken)
		{
			// Affirm and remove speculative marks, return to normal mode
			WriteBack.affirmSpeculativeInsts();
			InstructionBuffer.speculativeMode = false;
			in.mispredicted = false;
			Simulator.totalNumberOfCorrectBranchPredictions++;
			// Dynamic branch prediction update
			if(in.branchTaken)
				perm.branchSchemeVal = Math.min(3, in.branchSchemeVal+1);
			else
				perm.branchSchemeVal = Math.max(0, in.branchSchemeVal-1);
		}
		else
		{
			// Delete incorrect instructions
			WriteBack.deleteSpeculativeInstsFromROB();
			WriteBack.deleteSpeculativeInstsFromReservationStations();
			
			// Flush beginning of pipeline
			FetchUnit.currentIssue = new ArrayList<Instruction>();
			FetchUnit.nextIssue = new ArrayList<Instruction>();
			Decoder.currentDecodedInstructionSS = new ArrayList<Instruction>();
			Decoder.nextDecodedInstructionSS = new ArrayList<Instruction>();
			Decoder.issue[0] = null;
			Decoder.issue[1] = null;
			Decoder.issue[2] = null;
			Decoder.issue[3] = null;
			
			// Stall the fetch until branch instruction retires
			FetchUnit.specialStall = true;
			InstructionBuffer.speculativeMode = false;
			in.mispredicted = true;
			
			// Dynamic branch prediction update
			if(in.branchTaken)
				perm.branchSchemeVal--;
			else 
				perm.branchSchemeVal++;
		}
	}

	private static void blth(Instruction in) {
		int o1 = Integer.parseInt(in.workingOperands.get(0));
		int o2 = Integer.parseInt(in.workingOperands.get(1));
		int o3 = Integer.parseInt(in.workingOperands.get(2));
		in.result = o3;
		broadcastBranchResult((o1<o2),in);
	}

	private static void beq(Instruction in) {
		int o1 = Integer.parseInt(in.workingOperands.get(0));
		int o2 = Integer.parseInt(in.workingOperands.get(1));
		int o3 = Integer.parseInt(in.workingOperands.get(2));
		in.result = o3;
		broadcastBranchResult((o1==o2),in);
	}
	
	private static void bneq(Instruction in) {
		int o1 = Integer.parseInt(in.workingOperands.get(0));
		int o2 = Integer.parseInt(in.workingOperands.get(1));
		int o3 = Integer.parseInt(in.workingOperands.get(2));
		in.result = o3;
		broadcastBranchResult((o1!=o2),in);
	}

	private static void b(Instruction in) {
		int o1 = Integer.parseInt(in.workingOperands.get(0));
		in.result = o1;
		broadcastBranchResult(true,in);
	}
}
