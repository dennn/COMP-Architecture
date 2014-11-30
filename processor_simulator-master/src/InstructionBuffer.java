import java.util.ArrayList;
import java.util.LinkedList;
import java.util.Queue;

public class InstructionBuffer {

	public static Queue<Instruction> buffer;
	public static final int sizeOfBuffer = 10;
	
//	// Fetch this clock cycle
//	public static Instruction nextInstruction = null;
//	public static Instruction[] nextInstructionSS = null;
//
//	// Grab the last current instruction and make it nextInst
//	// This is ready to be pushed out
//	public static Instruction previousInstruction = null;
	public static Instruction[] currentInstructionSS = null;
		
	public static boolean speculativeMode = false; 
	
	InstructionBuffer()
	{
		buffer = new LinkedList<Instruction>();
	}
	
	public void fill()
	{
		ArrayList<Instruction> li = Simulator.assembler.getListOfInstructions();
		
		int sizeToFill = Math.min(li.size(), sizeOfBuffer);
		
		for (int i=0; i<sizeToFill; i++)
		{
			Instruction itc = li.get(i);
			buffer.add(new Instruction(itc.instruction, itc.instructionType, itc.operands, itc.workingOperands, itc.memoryAddress, itc.destinationRegister, Simulator.clockCycles, itc.branchSchemeVal));
		}
	}
	
//	/** Issue window size 1 */
//	public static void getNextInstruction()
//	{
//		nextInstruction = previousInstruction;
//		
//		Simulator.clockCycles++;
//		Instruction result;
//		
//		// Grab next instruction out of buffer if it is available
//		try{
//			result = buffer.remove();
//		} catch(Exception e) {
//			result = null;
//		}
//		
//		// If there are instructions we can still pull into buffer at the end, do it
//		if ((Simulator.registerFile[31]+10) < Assembler.listOfInstructions.size())
//		{
//			buffer.add(Assembler.listOfInstructions.get(Simulator.registerFile[31]+10));
//		}
//		previousInstruction = result;
//	}
	
	/** Issue window size n */
	public static void getNextInstructionSS()
	{		
		Instruction[] window = new Instruction[4];
		
		// Grab next instruction out of buffer if it is available
		for (int i=0; i<Simulator.ISSUE_WINDOW_SIZE; i++)
		{
			try{
				// Stall if two branches
				if(speculativeMode && (buffer.peek().instructionType==2)) //&& !buffer.peek().instruction.endsWith("B")))
				{
					Simulator.isStalled = true;
					break;
				}
				else
				{
					window[i] = buffer.remove();
									
					// Tag as speculative if in speculative mode
					if(speculativeMode)
						window[i].specualtive = true;			
					
					// Pick up branch and start fetching most probable instructions
					// Take unconditional branches - call branch predictor on conditional branches
//					if(window[i].instruction.equals("B"))
//					{
//						if(window[i].operands.size()<1) System.err.println("Branch instruction malformed");
//						int target = Integer.parseInt(window[i].operands.get(0));
//						refillFetchBuffer(target);
//						Simulator.PCFetch = target;
//					}
//					else if(window[i].instructionType==2)
					if(window[i].instructionType==2)
					{
						speculativeMode = true;
						window[i].branchTaken = predictBranchAndAct(window[i]);
					}
					
					ArrayList<Instruction> li = Simulator.assembler.getListOfInstructions();

					// If there are instructions we can still pull into buffer at the end, do it
					if ((Simulator.PCFetch+10) < li.size())
					{
						Instruction itc = li.get(Simulator.PCFetch+10);
						buffer.add(new Instruction(itc.instruction, itc.instructionType, itc.operands, itc.workingOperands, itc.memoryAddress, itc.destinationRegister, Simulator.clockCycles, itc.branchSchemeVal));
						
					}
					Simulator.PCFetch++;
				}
			} catch(Exception e) {
//				System.err.println("ExceptiON!!!" + e.getMessage());
				window[i] = null;
			}
		}
		currentInstructionSS = window;
	}
	
	public static boolean predictBranchAndAct(Instruction branchInst)
	{
		System.out.println("Branch prediction started");
		if(branchInst.operands.size()<1) System.err.println("Branch instruction malformed");
		
		// Unconditional branch - awlays taken
		if (branchInst.instruction.equals("B"))
		{
			int target = Integer.parseInt(branchInst.operands.get(0));
			refillFetchBuffer(target);
			Simulator.PCFetch = target;
			return true;
		}
		else
		{
			if(branchInst.operands.size()!=3) System.err.println("Conditional branch instruction malformed - no target in position 3");
			int target = Integer.parseInt(branchInst.operands.get(2));
			// Loop closing conditional branches - always taken
//			if(Simulator.generator.nextInt(3)==0) return false;
			if (target<branchInst.memoryAddress)
			{
				refillFetchBuffer(target);
				Simulator.PCFetch = target;
				return true;
			}
			
			// Other conditional branches - (use dynamic branch prediction)
			if(branchInst.branchSchemeVal>=2 && Simulator.dbp)
			{
				refillFetchBuffer(target);
				Simulator.PCFetch = target;
				return true;
			}
			// Dont take
			return false;
		}

	}
	
	public static void completeFlushAndFill(int startingAddress)
	{
		Simulator.PCFetch = startingAddress;
		buffer.clear();
		currentInstructionSS = null;
		Decoder.nextDecodedInstructionSS = new ArrayList<Instruction>();
		Decoder.currentDecodedInstructionSS = new ArrayList<Instruction>();
		ArrayList<Instruction> li = Simulator.assembler.getListOfInstructions();

		int sizeToFill = Math.min(li.size()-startingAddress, sizeOfBuffer);
		for (int j=0; j<sizeToFill; j++)
		{
			Instruction itc = li.get(startingAddress+j);
			buffer.add(new Instruction(itc.instruction, itc.instructionType, itc.operands, itc.workingOperands, itc.memoryAddress, itc.destinationRegister, Simulator.clockCycles, itc.branchSchemeVal));
		}
	}
	
	public static void refillFetchBuffer(int startingAddress)
	{
		buffer.clear();
		ArrayList<Instruction> li = Simulator.assembler.getListOfInstructions();
		int sizeToFill = Math.min(li.size()-startingAddress, sizeOfBuffer);
		for (int j=0; j<sizeToFill; j++)
		{
			Instruction itc = li.get(startingAddress+j);
			buffer.add(new Instruction(itc.instruction, itc.instructionType, itc.operands, itc.workingOperands, itc.memoryAddress, itc.destinationRegister, Simulator.clockCycles, itc.branchSchemeVal));
		}
	}
	
	

}
