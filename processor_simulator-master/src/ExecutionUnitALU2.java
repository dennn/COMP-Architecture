public class ExecutionUnitALU2 {
	
	public static Instruction currentExecuting;
	public static Instruction nextExecuting;
	
	public static boolean freeForDispatch;
	
	public static int cyclesLeft;
	
	ExecutionUnitALU2()
	{
		currentExecuting = null;
		nextExecuting = null;
		freeForDispatch = true;
		cyclesLeft=0;
	}
	
	public static void issueInstruction(Instruction in) {
			if(in!=null && (freeForDispatch==false))
			{
				System.err.println("Sending an instruction to ALU1 when it appears busy.");
			}
			if(in==null && cyclesLeft!=0)
			{
				cyclesLeft--;
				if(cyclesLeft == 0)	completeExecution();
			}
			
			if(in==null && currentExecuting==null)
				Simulator.numberOfNullsInEUs++;
		
			if (in != null)
			{
				freeForDispatch = false;
				if(in.instructionType==0) Simulator.clearScoreboardBit(in.destinationRegister); //if writing to a register then it has to be marked in the scoreboard after issue
				if (in.instruction.equals("ADD"))
					add(in);
				else if (in.instruction.equals("ADDI"))
					add(in);
				else if (in.instruction.equals("MOV"))
					mov(in);
				else if (in.instruction.equals("MUL"))
					mul(in);
				else if (in.instruction.equals("DIV"))
					div(in);
				else if (in.instruction.equals("LD"))
					ld(in);
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
				else {
					System.err.println("Error in ALU EXECUTION UNIT:\nInstruction not defined on this processor: " + in.instruction);
					System.exit(0);
				}
			currentExecuting = in;
			if(cyclesLeft == 0)	completeExecution();
			}
	}
	
	// Send the result to be picked up by WriteBack
	public static void completeExecution() {
		nextExecuting = currentExecuting;
		freeForDispatch = true;
	}

	private static void sr(Instruction in) {
		cyclesLeft = 0;
		int o2 = Integer.parseInt(in.workingOperands.get(1));
		int o3 = Integer.parseInt(in.workingOperands.get(2));
		in.result = o2 << o3;
	}

	private static void sl(Instruction in) {
		cyclesLeft = 0;
		int o2 = Integer.parseInt(in.workingOperands.get(1));
		in.result = o2;
	}

	private static void mov(Instruction in) {
		cyclesLeft = 0;
		int o2 = Integer.parseInt(in.workingOperands.get(1));
		in.result = o2;
	}

	private static void mul(Instruction in) {
		cyclesLeft = 4;
		int o2 = Integer.parseInt(in.workingOperands.get(1));
		int o3 = Integer.parseInt(in.workingOperands.get(2));
		in.result = o2*o3;
		freeForDispatch = false;
	}
	
	private static void div(Instruction in) {
		cyclesLeft = 4;
		int o2 = Integer.parseInt(in.workingOperands.get(1));
		int o3 = Integer.parseInt(in.workingOperands.get(2));
		in.result = (int) Math.floor(o2/o3);
		freeForDispatch = false;
	}

	private static void neg(Instruction in) {
		cyclesLeft = 0;
		int o2 = Integer.parseInt(in.workingOperands.get(1));
		in.result = -1*o2;
	}
	
	private static void not(Instruction in) {
		cyclesLeft = 0;
		int o2 = Integer.parseInt(in.workingOperands.get(1));
		in.result = ~o2;
	}

	private static void or(Instruction in) {
		cyclesLeft = 0;
		int o2 = Integer.parseInt(in.workingOperands.get(1));
		int o3 = Integer.parseInt(in.workingOperands.get(2));
		in.result = o2 | o3;
	}

	private static void and(Instruction in) {
		cyclesLeft = 0;
		int o2 = Integer.parseInt(in.workingOperands.get(1));
		int o3 = Integer.parseInt(in.workingOperands.get(2));
		in.result = o2 & o3;
	}

	private static void xor(Instruction in) {
		cyclesLeft = 0;
		int o2 = Integer.parseInt(in.workingOperands.get(1));
		int o3 = Integer.parseInt(in.workingOperands.get(2));
		in.result = o2^o3;
	}

	private static void sub(Instruction in) {
		cyclesLeft = 0;
		int o2 = Integer.parseInt(in.workingOperands.get(1));
		int o3 = Integer.parseInt(in.workingOperands.get(2));
		in.result = o2-o3;
	}

	private static void ld(Instruction in) {
		cyclesLeft = 0;
		int o2 = Integer.parseInt(in.workingOperands.get(1));
		int o3 = Integer.parseInt(in.workingOperands.get(2));
		in.result = Simulator.memory[o2+o3];
	}

	public static void add(Instruction in) {
		cyclesLeft = 0;
		int o2 = Integer.parseInt(in.workingOperands.get(1));
		int o3 = Integer.parseInt(in.workingOperands.get(2));
		in.result = o2+o3;
	}
}
