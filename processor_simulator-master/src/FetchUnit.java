import java.util.ArrayList;

// Check for dependencies and issue as many instructions as we can to 
// parallel decoding

public class FetchUnit {
	
//	public static ArrayList<Instruction> issueWindow;
	
	public static ArrayList<Instruction> currentIssue;
	public static ArrayList<Instruction> nextIssue;
	
	public static boolean noDependencies;
	public static boolean specialStall = false; // used to stop fetching until a mispredicted branch instruction retires
	
	FetchUnit()
	{
		currentIssue = new ArrayList<Instruction>();
		nextIssue = new ArrayList<Instruction>();
		noDependencies = true;
	}
	
	public static void superscalarIssue()
	{	
		// Grab the next batch from the buffer into the issue window
		if (!Simulator.isStalled && !specialStall)
		{
			currentIssue = new ArrayList<Instruction>();
			InstructionBuffer.getNextInstructionSS();
			for (int j=0; j<Simulator.ISSUE_WINDOW_SIZE; j++)
			{
				if(InstructionBuffer.currentInstructionSS[j]!=null) currentIssue.add(InstructionBuffer.currentInstructionSS[j]);
			}
			// Push values to decode
			nextIssue = currentIssue;
		}
//		ArrayList<Instruction> inspectIW = currentIssue;
	}	

}
