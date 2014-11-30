import java.util.ArrayList;
import java.util.LinkedList;
import java.util.Queue;


public class ReservationStationALU1 {
	public static Queue<ReservationStationEntry> rseSet;
	public static boolean isFull;
	public static final int maxSize = 4;
	public static boolean stalled;
	
	ReservationStationALU1()
	{
		rseSet = new LinkedList<ReservationStationEntry>();
		isFull = false;
		stalled = false;
	}
	
	public static void issueTo()
	{
		Instruction i = Decoder.issue[0];
				
		if(rseSet.size() == maxSize)
		{
			Simulator.isStalled = true;
			return;
		}
		
		if(i!=null)
		{
			// Issue bound fetch here
			Decoder.decodeWithFetch(i);
			
			// Create new reservation station entry
			ReservationStationEntry rseNew = new ReservationStationEntry(i);
			rseSet.add(rseNew);
			Decoder.issue[0] = null;
			
			// Add to reorder buffer
			Simulator.enterInROB(i);
		}
	}
	
	public static Instruction dispatchAttempt()
	{		
		for(ReservationStationEntry rse_dispatch : ReservationStationALU1.rseSet)
		{	
			// Check for operand availability (valid bits)
			boolean vbits = rse_dispatch.validBits[0] && rse_dispatch.validBits[1]; 
			
			boolean dependency = false;
			
			// Check for dependencies in issue buffer
			for(int i=0; i<4; i++)
			{
				if(Decoder.issue[i]!=null)
					dependency |= Check.dependencyCheck(rse_dispatch.inst, Decoder.issue[i]);
			}
			
			// Check for dependencies in exiting decode
			for(Instruction i : Decoder.nextDecodedInstructionSS)
			{
				dependency |= Check.dependencyCheck(rse_dispatch.inst, i);
			}
				

			// Forward results if possible - write temp results and update valid bits
			ArrayList<Instruction> rawDependentTargets = new ArrayList<Instruction>();
			ArrayList<Instruction> rawDependentTargetsToRemove = new ArrayList<Instruction>();
			for(ROBEntry robe : Simulator.ROB)
			{
				if(Check.rawD(rse_dispatch.inst, robe.inst)) rawDependentTargets.add(robe.inst);
				dependency |= Check.dependencyCheck(rse_dispatch.inst, robe.inst);
			}
			for(Instruction i : rawDependentTargets)
			{
				if (i.memoryAddress>rse_dispatch.inst.memoryAddress) rawDependentTargetsToRemove.add(i);
			}
			rawDependentTargets.removeAll(rawDependentTargetsToRemove);
			if(rawDependentTargets.size()==1)
				Check.attemptResultForwarding(rse_dispatch.inst, rawDependentTargets.get(0), rse_dispatch.validBits);
			
			
			// Dispatch if EU is free
			boolean EUFree = ExecutionUnitALU1.freeForDispatch;
			if(!ExecutionUnitALU1.freeForDispatch) System.err.println("For some reason the EU ins't ready for dispatch"); //todo: remove after subpipelining
			
			if(EUFree && vbits && !dependency)
			{
				if(rseSet.remove(rse_dispatch)==false)
					System.err.println("Trying to remove entry from RSALU1 which doesnt exist...IDIOT!");
								
				return rse_dispatch.inst;
			}
			else
			{
				System.out.println("Dispatch ALU1 failed");
			}
			
			if(!EUFree)
				System.out.println("[RSALU1 BLOCKED] EU not free for dispatch");
			if(!vbits)
				System.out.println("[RSALU1 BLOCKED] Operands not arrived yet");
			if(dependency)
				System.out.println("[RSALU1 BLOCKED] Dependencies exist: ");
			
		}
		return null;
	}

	public static void circulateEUResult(Instruction currentExecuting) {
			for(ReservationStationEntry r: rseSet)
			{
				r.updateWith(currentExecuting);
			}		
	}
}
