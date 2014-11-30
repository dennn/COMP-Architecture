import java.util.ArrayList;

public class Instruction
{
	public String instruction;
	public int instructionType;
	public ArrayList<String> operands = new ArrayList<String>();
	public ArrayList<String> workingOperands = new ArrayList<String>();
	public int memoryAddress;
	public int targetEU;
	public Integer result;
	public String destinationRegister; // "UNDEFINED" or "R7"
	public boolean specualtive = false;
	public boolean branchTaken;
	// INSTRUTCION TYPE DEFINITION
	public boolean mispredicted;
	
	public int clockCycleCreated;
	public int branchSchemeVal;


	public Instruction()
	{
	}
	
	public Instruction(String instruction, int instructionType, ArrayList<String> opeands, ArrayList<String> workingOperands, int memoryAddress, String dest, int cl, int branch)
	{
		this.instruction = instruction;
		this.instructionType = instructionType;
		this.operands = opeands;
		this.workingOperands = workingOperands;
		this.memoryAddress = memoryAddress;
		this.destinationRegister = dest;
		this.clockCycleCreated = cl;
		this.branchSchemeVal = branch;
	}
	
	public Instruction(String instruction, int instructionType)
	{
		this.instruction = instruction;
		this.instructionType = instructionType;
		this.specualtive = false;
	}
	
//	public Instruction(Instruction ni) {
//		this(ni.instruction, ni.instructionType, ni.operands, ni.workingOperands, ni.memoryAddress, ni.destinationRegister);
//		//no defensive copies are created here, since 
//		//there are no mutable object fields (String is immutable)
//		}

}
