import java.io.FileNotFoundException;
import java.util.ArrayList;
import java.util.LinkedList;
import java.util.Queue;
import java.util.Random;

public class Simulator {

	private static InstructionBuffer instBuff;
	public FetchUnit fetchUnit;

	public static Assembler assembler;
	public Decoder decoder;
	
	public ReservationStationALU1 rsALU1;
	public ReservationStationALU2 rsALU2;
	public ReservationStationLS rsLS;
	public ReservationStationBranch rsBranch;
	
	public ExecutionUnitALU1 euALU1;
	public ExecutionUnitALU2 euALU2;
	public ExecutionUnitLS euLS;
	public ExecutionUnitBranch euBranch;

	public WriteBack writeBack;
	
//	private static final String fileName = "fibs.asm";
//	private static final String fileName = "fibsSS.asm";
//	private static final String fileName = "fibsSSOptimised.asm";
	
//	private static final String fileName = "instruction_test.asm";
//	private static final String fileName = "branch_test.asm";
//	private static final String fileName = "lsbypassing_test.asm";
//	private static final String fileName = "renaming_test.asm";
//	private static final String fileName = "bubbleSort.asm";
//	private static final String fileName = "bubbleSortOptimised.asm";
	public static String fileName = "src/hydro_fragment_forward_branch.asm";
	
//	private static final String fileName = "inner_product.asm";
//	private static final String fileName = "inner_product_unrolled.asm";

//	private static final String fileName = "vadd.asm";
//	private static final String fileName = "vector_xor.asm";
	
	// Physical resources
	public static int[] registerFile;
	public static Queue<Integer> renameRegistersPool;
	public static boolean[] scoreboard; //true is available, false is taken
	public static int[] memory;
	public static Queue<ROBEntry> ROB;
	public static Random generator = new Random();
	public static Boolean dbp; //dynamic branch prediction

	// Pipeline management
	public static final int ISSUE_WINDOW_SIZE = 4;
	public static int clockCycles;	
	public static int ALUAvailable 					= 2;
	public static int branchAvailable 				= 1;
	public static int LSAvailable 					= 1;
	public static boolean continueExecution;
	public static boolean isStalled = false;	
	public static int origPC;
	public static int PCFetch;
	public static boolean speculativeMode;
	
	// Statistics
	public static float totalNumberOfBranchPredictions;
	public static float totalNumberOfCorrectBranchPredictions;
	public static float numberOfNullsInEUs;
	public static boolean stepMode = true;
	public static float instructionCount;
	
	Simulator()
	{
		assembler = new Assembler();
		
		registerFile = new int[32];
		renameRegistersPool = new LinkedList<Integer>();
		scoreboard = new boolean[32];
		memory = new int[1024];
		ROB = new LinkedList<ROBEntry>();
		initRenameRegisters();

		PCFetch = 0;			//PC for fetching
		speculativeMode = false;
		registerFile[31] = 0; 	//PC
		registerFile[0] = 0;  	// Always 0
		clockCycles = 0;
		continueExecution = true;
		
		fetchUnit = new FetchUnit();
		instBuff = new InstructionBuffer();
		
		decoder = new Decoder();
				
		rsALU1 = new ReservationStationALU1();
		rsALU2 = new ReservationStationALU2();
		rsLS = new ReservationStationLS();
		rsBranch = new ReservationStationBranch();
		
		euALU1 = new ExecutionUnitALU1();
		euALU2 = new ExecutionUnitALU2();
		euLS = new ExecutionUnitLS();
		euBranch = new ExecutionUnitBranch();
		
		writeBack = new WriteBack();
		
		totalNumberOfBranchPredictions = 0;
		totalNumberOfCorrectBranchPredictions = 0;
		numberOfNullsInEUs =0;
		instructionCount = 0;
	}
	
	private void initRenameRegisters() {
		for(int i=0; i<128; i++)
			renameRegistersPool.add(i);
	}
	
	
	public static void enterInROB(Instruction in) {
		ROB.add(new ROBEntry(in));
	}

	public void run()
	{
		try 
		{
			assembler.parse(fileName);													// ASSEMBLE INPUT
		}
		catch (FileNotFoundException e)
		{
			e.printStackTrace();
		}
		assembler.writeLabelLocations();
		instBuff.fill();
//		List<Instruction> listOfInstructions = Simulator.assembler.getListOfInstructions();
		resetScoreboard();
		
		do
		{	
			////////////////////////////////////////////////
			// Write back
			////////////////////////////////////////////////
//			boolean [] showS = scoreboard;
			WriteBack.writeResults();
//			Queue<ROBEntry> r = Simulator.ROB;
//			List<Instruction> ali = Simulator.assembler.getListOfInstructions();
			////////////////////////////////////////////////
			// Execute
			////////////////////////////////////////////////
						
			ExecutionUnitALU1.issueInstruction(		ReservationStationALU1.dispatchAttempt());						// EXECUTE
			ExecutionUnitALU2.issueInstruction(		ReservationStationALU2.dispatchAttempt());
			ExecutionUnitLS.issueInstruction(		ReservationStationLS.dispatchAttempt());
			ExecutionUnitBranch.issueInstruction(	ReservationStationBranch.dispatchAttempt());
			
			Simulator.resetResourceCount();
						
			////////////////////////////////////////////////
			// Dispatch
			////////////////////////////////////////////////
			
			ReservationStationALU1.issueTo();
			ReservationStationALU2.issueTo();
			ReservationStationLS.issueTo();
			ReservationStationBranch.issueTo();
			
			////////////////////////////////////////////////
			// Decode
			////////////////////////////////////////////////			
			
			// ISSUE IF RESERVATION STATIONS ARE FREE
//			boolean[] showScoreboar = scoreboard;
			Decoder.decodeSS();															// DECODE
//			ArrayList<Instruction> inst12 = Decoder.currentDecodedInstructionSS; 		// WHATS JUST BEEN decoded
//			Instruction[] dispatch = Decoder.issue;										// WHATS GOING TO RESERVATION STATIONS NOW

			////////////////////////////////////////////////
			// Fetch
			////////////////////////////////////////////////			
			
			FetchUnit.superscalarIssue(); 												// FETCH

//			ArrayList<Instruction> issued1 = FetchUnit.currentIssue; 					// WHATS JUST BEEN DECODED
//			ArrayList<Instruction> issued2 = FetchUnit.nextIssue; 						// WHATS GOING TO DECODE NOW
			
			/////////////////////////////////////////////////
			// Pipeline management - branching, clock and PC
			/////////////////////////////////////////////////
			
			clockCycles++;
			isStalled = false;
			if(stepMode)
				Print.printState();
			
		}while(Simulator.continueExecution);
		
		System.out.println("-----------------EXECUTION FINISHED-------------------");
		System.out.println("Clock cycles: " + clockCycles);
		System.out.println("Correct branch predictions: " + (totalNumberOfCorrectBranchPredictions/totalNumberOfBranchPredictions)*100 + " %");
		System.out.println("Percentage of time EUs are full: " + (numberOfNullsInEUs/(clockCycles*4))*100 + " %");
		System.out.println("CPI: " + Float.parseFloat(clockCycles +"")/Float.parseFloat(Simulator.instructionCount +""));
		System.out.println("Total instruction count: " + Simulator.instructionCount);
		System.out.println("------------------------------------------------------");

		totalNumberOfBranchPredictions = 0;
		totalNumberOfCorrectBranchPredictions = 0;
	}
	
	//************************************************//
	// HELPER FUNCTIONS                               //
	//************************************************//
	public static void resetScoreboard()
	{
		for (int i = 0; i < scoreboard.length; i++) // INIT SCOREBOARD
		{
			scoreboard[i] = true;
		}
	}

	public static void restartFromMispredictedBranch()
	{
			InstructionBuffer.completeFlushAndFill(registerFile[31]);
			
			FetchUnit.currentIssue = new ArrayList<Instruction>();
			FetchUnit.nextIssue = new ArrayList<Instruction>();
			FetchUnit.specialStall = false;
			
			Decoder.currentDecodedInstructionSS = new ArrayList<Instruction>();
			Decoder.nextDecodedInstructionSS = new ArrayList<Instruction>();
			
			Decoder.issue[0] = null;
			Decoder.issue[1] = null;
			Decoder.issue[2] = null;
			Decoder.issue[3] = null;
			
			
			ReservationStationALU1.rseSet.clear();
			ReservationStationALU2.rseSet.clear();
			ReservationStationLS.rseSet.clear();
			ReservationStationBranch.rseSet.clear();
			
			// Delete possibly)( the incorrect speculative entries in the ROB
			Simulator.ROB.clear();
			
			resetScoreboard();
			
//			System.out.println(registerFile[9]);
	}
	
	public static ArrayList<Instruction> uncompletedInstructionsInROB()
	{
		ArrayList<Instruction> insts = new ArrayList<Instruction>();
		for(ROBEntry re : ROB)
		{
				if (re.status != 2)
				{
					insts.add(re.inst);
				}
		}
		return insts;
	}
	
//	public void incrementProgramCounter()
//	{
//		registerFile[31]+=4; //TODO: change to size of issue window
//	}
	
	public static void clearScoreboardBit(String destinationRegister)
	{
		try{
		if (destinationRegister!=null && !destinationRegister.equals("") && !destinationRegister.equals("UNDEFINED"))
		{
			if (destinationRegister.charAt(0) == 'R')
			{
				int registerNumber = Decoder.stripReg(destinationRegister);
				if (registerNumber<0 || registerNumber>31)
					System.err.println("Scoardboard does not have a register entry for " + registerNumber);
				scoreboard[registerNumber] = false;
			}
			else
				System.err.println("Destination register not recognised");
		}}catch(Exception e)
		{
			System.err.println("Problem clearing register with this string: " + destinationRegister);
			System.exit(0);
		}
	}
	
	public static void setScoreboardBit(int registerNumber)
	{
		if (registerNumber<0 || registerNumber>31)
			System.err.println("Scoardboard does not have a register entry for " + registerNumber);
		scoreboard[registerNumber] = true;
	}
	
	public static boolean canFetchOperand(int registerNumber)
	{
		return scoreboard[registerNumber]==true;
	}
	
	//************************************************//
	// EXECUTION HELPER FUNCTIONS                     //
	//************************************************//
	
	// 0/1 	ALU
	// 2	CONTROL FLOW
	// 3	LOAD/STORE
	public static int getCorrectUnit(Instruction inst)
	{
		 if (inst.instructionType==1 || inst.instruction.equals("LD")){
				return 2;
		}
		 else if (inst.instructionType==0){
			return 0;
		}
		else
		{
			return 3;
		}
	}
	
	public static void resetResourceCount()
	{
		ALUAvailable 		= 2;
		branchAvailable 	= 1;
		LSAvailable 		= 1;
	}
	
	public static void updateResources(Instruction i)
	{
		int unitDestination = getCorrectUnit(i);
		if (unitDestination == 0)
		{
			ALUAvailable--;
			i.targetEU = ALUAvailable;
		}
		else if(unitDestination ==2)
		{
			branchAvailable--;
			i.targetEU = 2;
		}
		else
		{
			LSAvailable--;
			i.targetEU = 3;
		}
	}	
	
	public static boolean isThereACorrectEUFree(Instruction i)
	{		
		int unitDestination = getCorrectUnit(i);
		if (unitDestination == 0)
		{
			return (ALUAvailable > 0) ? true : false;
		}
		else if(unitDestination ==2)
		{
			return (branchAvailable > 0) ? true : false;
		}
		else
		{
			return (LSAvailable > 0) ? true : false;
		}
	}
		
	
	public static void main(String[] args)
	{
		Simulator sim = new Simulator();
		sim.fileName = args[0];
		dbp = (Integer.parseInt(args[1])==1)?  true : false;
		sim.run();
	}


}
