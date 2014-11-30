  
public class ReservationStationEntry {
	public Instruction inst;
	
	// Define the operand availability of two possible operands
	// 0 WAITING FOR AVAILABILITY | 1 READY FOR DISPATCH
	public boolean validBits[];
	
	// Define the register to write to with this instruction
	// -1 DOESNT WRITE | i = Ri
	public int destinationRegister;
	
	ReservationStationEntry(Instruction i)
	{
		inst = i;
		validBits = new boolean[2];
		validBits[0] = true;
		validBits[1] = true;
		destinationRegister = -1;
		
		updateValidBits();
		markScoreboardAsIssued();
	}
	

	private void markScoreboardAsIssued() {
		if (destinationRegister!=-1)
		{
			if (destinationRegister<0 || destinationRegister>31)
				System.err.println("Tried to score an invalid register in the scoreboard: " + destinationRegister);
			
			Simulator.scoreboard[destinationRegister] = false;
		}
	}

	public void updateValidBits()
	{
		if (inst.workingOperands.size()>1 && inst.instructionType==0)
		{
			for (int i=1; i<inst.workingOperands.size(); i++)
			{
				String s = inst.workingOperands.get(i);
				String s2 = inst.operands.get(i);
				if (s.charAt(0) == 'R' && s2.charAt(0)=='R')
					validBits[i-1] = false;
			}
		}
		else if (inst.workingOperands.size()>1 && inst.instructionType!=0)
		{
			int j = 0;
			for (int i=0; i<inst.workingOperands.size(); i++)
			{
				String s = inst.workingOperands.get(i);
				String s2 = inst.operands.get(i);
				if (s.charAt(0) == 'R' && s2.charAt(0)=='R')
				{
					validBits[j] = false;
					j++;
				}
				else if(s.charAt(0) == 'R' || s2.charAt(0)=='R')
				{
					validBits[j] = true;
					j++;
				}
			}
		}

	}


	public void updateWith(Instruction currentExecuting)
	{
			if (inst.workingOperands.size()>1 && inst.instructionType==0)
			{
				for (int i=1; i<inst.operands.size(); i++)
				{
					String s = inst.operands.get(i);
					if (s.equals(currentExecuting.destinationRegister))
					{
						// Need to circulate the result
						inst.workingOperands.set(i,currentExecuting.result + "");
						validBits[i-1] = true;
					}
				}
			}
			else if (inst.workingOperands.size()>1 && inst.instructionType!=0)
			{
				int k = 0;
				for (int i=0; i<inst.operands.size(); i++)
				{
					String s = inst.operands.get(i);
					if (s.equals(currentExecuting.destinationRegister))
					{
						if(k>2) System.err.println("Error updating a reservation station entry containing a non type 0 instruction");
						// Need to circulate the result
						inst.workingOperands.set(i,currentExecuting.result + "");
						validBits[k] = true;
						k++;
					}
				}
			}
			updateValidBits();
		
	}

}
