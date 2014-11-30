import java.util.ArrayList;

// Decode as much of the instruction as we can
// If the scoreboard bit is set to false then we just
// leave the operand as "R3"
public class Decoder {
	
	// Decode this clock cycle
	public static ArrayList<Instruction> nextDecodedInstructionSS = null;

	// Grab the last decoded instruction and make it available to be issued
	// This is ready to be pushed out
	public static ArrayList<Instruction> currentDecodedInstructionSS = null; //TODO: make this an array for SS issue
	
	
	public static Instruction[] issue;
	
	Decoder()
	{
		nextDecodedInstructionSS = new ArrayList<Instruction>();
		currentDecodedInstructionSS = new ArrayList<Instruction>();
		issue = new Instruction[4];
	}

	public static void decodeSS()
	{	
		// Empty decode and fill issue as far as possible
		if (!(nextDecodedInstructionSS.size()==0) && !Simulator.isStalled)
		{
			issue = reorderForIssue(Decoder.nextDecodedInstructionSS);
			if (!(nextDecodedInstructionSS.size()==0)) Simulator.isStalled = true;
		}
		
		// If decode completely empty, refill
		if(!Simulator.isStalled && nextDecodedInstructionSS.size()==0)
		{
			currentDecodedInstructionSS = new ArrayList<Instruction>();
			decodeWithoutFetch();
			nextDecodedInstructionSS = currentDecodedInstructionSS;
		}
	}
	
	public static void decodeWithoutFetch()
	{
		for(Instruction nextInstruction : FetchUnit.nextIssue)
		{
			if (nextInstruction!=null)
			{
				int operandsSize = nextInstruction.operands.size();

				// ***************************************** //			
				// DECODE CATEGORY 0 (plus loads) 
				// ***************************************** //				
				// Standard type : strip r off 1st and perform lookup on rest of operands
				if(operandsSize>1 && nextInstruction.instructionType==0)
				{
					String s0 = nextInstruction.operands.get(0);
					if (s0.charAt(0) == 'R')
					{
						int registerNumber = Decoder.stripReg(s0);
						nextInstruction.workingOperands.set(0, registerNumber + "");
					}
				}
			}
			currentDecodedInstructionSS.add(nextInstruction); // this could be NOP instead of null, perhaps
		}
	}
	
	public static void decodeWithFetch(Instruction nextInstruction)
	{
			if (nextInstruction!=null)
			{
				int operandsSize = nextInstruction.operands.size();
				
				// ***************************************** //			
				// DECODE CATEGORY 3 (plus loads) 
				// ***************************************** //	
				
				// do nothing!!
				
				
				// ***************************************** //			
				// DECODE CATEGORY 2
				// ***************************************** //
				if (nextInstruction.instructionType == 2)
				{
					// DECODE JR
					if(nextInstruction.operands.size()==1)
					{
						String s = nextInstruction.operands.get(0);
						if (s.charAt(0) == 'R')
						{
							int registerNumber = Decoder.stripReg(s);
							if(Simulator.canFetchOperand(registerNumber))
								nextInstruction.workingOperands.set(0, Simulator.registerFile[registerNumber] + "");
						}
					}
					
					// DECODE B
					if(nextInstruction.operands.size()==0)
					{
						//do nothing?
					}
							
					// DECODE BEQ, BNE and BLTH
					if(nextInstruction.operands.size()>1)
					{						
						for (int i=0; i<2; i++)
						{
							String s = nextInstruction.operands.get(i);
							if (s.charAt(0) == 'R')
							{
								int registerNumber = Decoder.stripReg(s);
								if(Simulator.canFetchOperand(registerNumber))
									nextInstruction.workingOperands.set(i, Simulator.registerFile[registerNumber] + "");
							}
						}
					}
						//previousDecodedInstructionSS.add(nextInstruction);				
				}
				
				// ***************************************** //			
				// DECODE CATEGORY 1 (just stores) 
				// ***************************************** //
				//Inverse store type : perform register lookup for all the operands
				else if (nextInstruction.instructionType == 1)
				{
					if (operandsSize>1)
					{
						for (int i=0; i<nextInstruction.operands.size(); i++)
						{
							String s = nextInstruction.operands.get(i);
							if (s.charAt(0) == 'R')
							{
								int registerNumber = Decoder.stripReg(s);
								if(Simulator.canFetchOperand(registerNumber))
									nextInstruction.workingOperands.set(i, Simulator.registerFile[registerNumber] + "");
							}
						}
					}
					//previousDecodedInstructionSS.add(nextInstruction);
				}
				
				// ***************************************** //			
				// DECODE CATEGORY 0 (plus loads) 
				// ***************************************** //				
				// Standard type : strip r off 1st and perform lookup on rest of operands
				else if(nextInstruction.operands.size()>1)
				{
					String s0 = nextInstruction.operands.get(0);
					if (s0.charAt(0) == 'R')
					{
						int registerNumber = Decoder.stripReg(s0);
						nextInstruction.workingOperands.set(0, registerNumber + "");
					}
					
					if (operandsSize>1)
					{
						for (int i=1; i<nextInstruction.operands.size(); i++)
						{
							String s = nextInstruction.operands.get(i);
							if (s.charAt(0) == 'R')
							{
								int registerNumber = Decoder.stripReg(s);
								if(Simulator.canFetchOperand(registerNumber))
									nextInstruction.workingOperands.set(i, Simulator.registerFile[registerNumber] + "");
							}
						}
					}
				}
			}
	}
	
	public static Instruction[] reorderForIssue(ArrayList<Instruction> insts)
	{
		Instruction[] ia = new Instruction[4];
		
		ia[0] = null; //TODO: change this to a nop
		ia[1] = null;
		ia[2] = null;
		ia[3] = null;
		
		boolean failedToEnter = false;
		
		for(int i=0; i<insts.size() && !failedToEnter; i++)
		{
			if(insts.get(i).instructionType==0 && !insts.get(i).instruction.equals("LD"))
			{
				if(ia[0]==null){ ia[0] = insts.get(i); continue; }
				else if(ia[1]==null) {ia[1] = insts.get(i); continue; }
			}
			
			if(insts.get(i).instructionType==1 || insts.get(i).instruction.equals("LD") || insts.get(i).instruction.equals("BREAK"))
			{
				if(ia[2]==null) {ia[2] = insts.get(i); continue;}
			}
			
			if(insts.get(i).instructionType==2)
			{
				if(ia[3]==null) {ia[3] = insts.get(i); continue;}
			}
			failedToEnter = true;
		}
		
		insts.remove(ia[0]);
		insts.remove(ia[1]);
		insts.remove(ia[2]);
		insts.remove(ia[3]);
		
		// Update new NOP targets
		for(int i =0; (i<4); i++)
		{
			if(ia[i]!=null)
			{
				if(ia[i].instruction.equals("NOP"))
				{	
					ia[i].targetEU=i;
				}
			}
		}	
		
		return ia;
	}
	
	
	public void updateNOP(Instruction i, int dest)
	{
		i.targetEU=dest;
	}
	
	public static int stripReg(String val)
	{
		String[] split = val.split("R");
		if(split.length < 2)
		{
			System.err.println("Trying to split a register string with problems: " + val);
			System.exit(1);
		}
		
		return Integer.parseInt(split[1]);
	}
	
	public static void main(String[] args)
	{
//		Decoder d = new Decoder();
//		int i = stripReg("R423");
//		System.out.println(i);
	}
}
