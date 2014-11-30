
public class ROBEntry {
	// 0 - ISSUED
	// 1 - EXECUTED
	// 2 - FINISHED	
	public int status;
	
	public int architecturalRegister;
	
	public Instruction inst;
	
	ROBEntry(Instruction i)
	{
		status = 0;
		inst = i;
	}
}
