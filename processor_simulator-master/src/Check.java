import java.util.ArrayList;

// Used to perform dependency checking
// TRUE: dependency found
// FALSE: dependency not found

public class Check {
	
	public static boolean existPipelineHazards(ArrayList<Instruction> ali)
	{
		boolean decode = false;
		boolean execution = false;
		boolean write = false;
		
		for(Instruction i : ali)
		{
			// Check decode current
			if (Decoder.currentDecodedInstructionSS != null)
			{
				for(Instruction dc : Decoder.currentDecodedInstructionSS)
				{
					decode |= dependencyCheck(i, dc);
				}
			}
			
			// Check execution units current
			execution |= dependencyCheck(i, ExecutionUnitALU1.currentExecuting);
			execution |= dependencyCheck(i, ExecutionUnitALU2.currentExecuting);
			execution |= dependencyCheck(i, ExecutionUnitLS.currentExecuting);
			execution |= dependencyCheck(i, ExecutionUnitBranch.currentExecuting);

			// Check write-back buffer
			if (WriteBack.currentInstructions!=null)
			{
				for(Instruction wbi : WriteBack.currentInstructions)
				{
					write |= dependencyCheck(i, wbi);
				}
			}
		}
		
		return (decode || execution || write);
	}
	
	public static boolean attemptResultForwarding(Instruction i1, Instruction i2, boolean[] validBits)
	{
		if (i2.result!=null)
		{
			if (i1.workingOperands.size()>1 && i1.instructionType==0)
			{
				for (int i=1; i<i1.operands.size(); i++)
				{
					String s = i1.operands.get(i);
					if (s.equals(i2.destinationRegister))
					{
						// Need to circulate the result
						i1.workingOperands.set(i,i2.result + "");
						validBits[i-1] = true;
						return false; //i.e dependency successfully resolved
					}
				}
			}
			else if (i1.workingOperands.size()>1 && i1.instructionType!=0)
			{
				int k = 0;
				for (int i=0; i<i1.operands.size(); i++)
				{
					String s = i1.operands.get(i);
					if (s.equals(i2.destinationRegister))
					{
						if(k>2) System.err.println("Error updating a reservation station entry containing a non type 0 instruction");
						// Need to circulate the result
						i1.workingOperands.set(i,i2.result + "");
						validBits[k] = true;
						k++;
						return false; //i.e dependency successfully resolved
					}
				}
			}
		}
		return true; // no forwarding possibly, dependency still exists
	}
	
	// Is i1 dependent on i2?
	public static boolean dependencyCheck(Instruction i1,	Instruction i2)
	{
		if (i1==null || i2 ==null) return false;
		
	
		boolean 	dataD, controlD, resourceD, rawD, warD, wawD;
		rawD = rawD(i1,i2);
		warD = false;//warD(i1, i2);
		wawD = false;//wawD(i1, i2);
		
		dataD 	 = 	rawD || warD || wawD;
		controlD = 	controlD(i1,i2);
		resourceD = resourceD(i1,i2);
				
		boolean result =  dataD || controlD || resourceD;
		return result;
	}
	
	//************************************************//
	// DATA DEPENDENCIES                              //
	//************************************************//
	
	// RAW DEPENDENCY (TRUE DEPENDENCY)
	//(Read after write: load-use and define-use)
	public static boolean rawD(Instruction i1, Instruction i2)
	{	
		// No dependency on branches or assembly directives
		if (i1.instructionType==3 || i1.instruction.equals("NOP")) return false;
		if (i2.instructionType==3 || i2.instruction.equals("NOP")) return false;

		// Ensure 1 reads after 2 writes
		if(!i1.specualtive && i2.specualtive) return false;
		if(i1.specualtive && !i2.specualtive && i1.memoryAddress<i2.memoryAddress) return true;
		
		if(!(i2.memoryAddress < i1.memoryAddress)) return false;	

		// No writing happening before a read (read should come after a write)
		if (i2.instructionType!=0) return false;

		// Match against all operands in type 1 and 2
		if (i1.instructionType==2 || i1.instructionType==1){
			for (String op : i1.operands){
				if (i2.operands.get(0).equals(op))
				{
					System.out.println("raw dep- " + i1.instruction + " is dependent on " + i2.instruction);
					return true;
				}
			}
		}
		// Match against all operands in type 0 bar the first
		else
		{
			for(int i=1; i<i1.operands.size(); i++)
			{
				if (i2.operands.get(0).equals(i1.operands.get(i))) 
				{
					System.out.println("raw dep- " + i1.instruction + " is dependent on " + i2.instruction);
					return true;
				}
			}
		}		
		return false;
	}
	
	// WAR DEPENDENCY
	// (Write after read: solve by renaming)
	public static boolean warD(Instruction i1, Instruction i2)
	{
		// No dependency on branches or assembly directives
		if (i1.instructionType==3 || i1.instruction.equals("NOP")) return false;
		if (i2.instructionType==3 || i2.instruction.equals("NOP")) return false;

		// Ensure 1 writes after 2 reads
		if(!(i2.memoryAddress < i1.memoryAddress)) return false;	
		
		// No writing happening afterwards
		if (i1.instructionType!=0) return false;
		// Match against all operands in type 1 and 2
		if (i2.instructionType==2 || i2.instructionType==1){
			for (String op : i2.operands){
				if (i1.operands.get(0).equals(op))
				{
					System.out.println("war dep- " + i1.instruction + " is dependent on " + i2.instruction);
					return true;
				}
			}
		}
		// Match against all operands in type 0 bar the first
		else
		{
			for(int i=1; i<i2.operands.size(); i++)
			{
				if (i1.operands.get(0).equals(i2.operands.get(i)))
				{
					System.out.println("war dep- " + i1.instruction + " is dependent on " + i2.instruction);
					return true;
				}
					
			}
		}		
		return false;
	}
	
	
	// WAW DEPENDENCY
	// (Write after write: solve by renaming)
	public static boolean wawD(Instruction i1, Instruction i2)
	{
		// No dependency on branches or assembly directives
		if (i1.instructionType==3 || i1.instruction.equals("NOP")) return false;
		if (i2.instructionType==3 || i2.instruction.equals("NOP")) return false;
		
		// Ensure 1 writes after 2 writes
		if(!(i2.memoryAddress < i1.memoryAddress)) return false; 
		
		// No writing happening
		if (i2.instructionType!=0 || i1.instructionType!=0) return false;
		
		if (i1.operands.get(0).equals(i2.operands.get(0)))
		{
			System.out.println("waw dep- " + i1.instruction + " is dependent on " + i2.instruction);
			return true;
		}

		return false;		
	}
	
	
	/////////////////////////////////////////////////////////////////////////
	// NOTES: loop-carried dependencies are false dependencies; can solve by 
	// renaming but only easy if compiler unrolls the loop
	/////////////////////////////////////////////////////////////////////////
	
	
	//************************************************//
	// CONTROL DEPENDENCIES                           //
	//************************************************//

	// CONDITIONAL TRANSFER OF CONTROL
	// (Instructions following a conditional branch instruction
	//  are dependent on it, solved by speculative execution and
	//  branch prediction)
	
	public static boolean controlD(Instruction instruction1, Instruction instruction2)
	{		
		// No dependency on NOPS?
		if (instruction1.instruction.equals("NOP")) return false;
		if (instruction2.instruction.equals("NOP")) return false;
		
		if(!instruction1.specualtive && instruction2.specualtive) return false;
		
		// If current control inst is preceeded by another inst, dependency is true
		if(instruction1.instructionType == 2 || instruction1.instructionType == 3)
		{
			if(instruction2.memoryAddress < instruction1.memoryAddress)
			{
				System.out.println("Control dep- " + instruction1.instruction + " is dependent on " + instruction2.instruction);
				return true;
			}
		}
		// If current inst is preceeded by a control inst, true //GO SPECULATIVE HERE!!
		else if(instruction2.instructionType == 2 || instruction1.instructionType == 3)
		{
			if((instruction2.memoryAddress < instruction1.memoryAddress))
			{
				System.out.println("Control dep- " + instruction1.instruction + " is dependent on " + instruction2.instruction + " BUT we send continue speculatively");
//				instruction1.specualtive = true; //todo: assert
//				return true; //TODO: SPECULATIVE EXECUTION!!!!!!!!!!! HERE!!!
				return false;
			}
		}	
		return false;
	}

		
	//************************************************//
	// RESOURCE DEPENDENCIES                          //
	//************************************************//
	
	// (Two instructions require the same limited resource)
	
	public static boolean resourceD(Instruction instruction1, Instruction instruction2)
	{
			if(!instruction1.specualtive && instruction2.specualtive) return false;
			if(instruction1.instruction.equals("LD") && instruction2.instruction.equals("STR")) return false;
			if(instruction1.instruction.equals("STR") && instruction2.instruction.equals("LD")) return false;
			if(instruction1.instruction.equals("STR") && instruction2.instruction.equals("STR")) return false;
		
			return !Simulator.isThereACorrectEUFree(instruction1); // if free then no dependency(ie false) //todo: this will always be true until we have subpiplining
	}
	//TODO: model some resource dependencies
	
	public static void main(String[] args)
	{
		////////////////////////////////////////
		// BEQ R1, R3, 40
		////////////////////////////////////////
		Instruction i1 = new Instruction("BEQ", 2);
		ArrayList<String> list = new ArrayList<String>();
		list.add("R1");
		list.add("R3");
		list.add("40");
		i1.operands = list;
		i1.memoryAddress = 1;
		
		////////////////////////////////////////
		// MUL R3, R8, R1
		////////////////////////////////////////		
		Instruction i2 = new Instruction("MUL", 0);
		ArrayList<String> list2 = new ArrayList<String>();
		list2.add("R3");
		list2.add("R8");
		list2.add("R1");
		i2.operands = list2;
		i2.memoryAddress = 2;
		
		////////////////////////////////////////
		// MUL R1, R8, R9
		////////////////////////////////////////		
		Instruction i22 = new Instruction("MUL", 0);
		ArrayList<String> list22 = new ArrayList<String>();
		list22.add("R1");
		list22.add("R8");
		list22.add("R9");
		i22.operands = list22;
		i22.memoryAddress = 6;
		
		////////////////////////////////////////
		// BEQ R1, R3, 40
		////////////////////////////////////////
		Instruction i111 = new Instruction("BEQ", 2);
		ArrayList<String> list111 = new ArrayList<String>();
		list111.add("R1");
		list111.add("R2");
		list111.add("R3");
		i111.operands = list111;
		i111.memoryAddress = 10;
		
		////////////////////////////////////////
		// ADD R1, R2, R3
		////////////////////////////////////////		
		Instruction i4 = new Instruction("ADD", 0);
		ArrayList<String> list4 = new ArrayList<String>();
		list4.add("R1");
		list4.add("R2");
		list4.add("R3");
		i4.operands = list4;
		i4.memoryAddress = 3;
		
		////////////////////////////////////////
		// ADD R1, R4, R5
		////////////////////////////////////////		
		Instruction i3 = new Instruction("ADD", 0);
		ArrayList<String> list3 = new ArrayList<String>();
		list3.add("R1");
		list3.add("R4");
		list3.add("R5");
		i3.operands = list3;
		i3.memoryAddress = 4;
		
		////////////////////////////////////////
		// STR R1, 20, R3
		////////////////////////////////////////		
		Instruction store = new Instruction("STR", 1);
		ArrayList<String> storeList = new ArrayList<String>();
		storeList.add("R1");
		storeList.add("20");
		storeList.add("R3");
		store.operands = storeList;
		store.memoryAddress = 0;
		
		////////////////////////////////////////
		// LD R3, 20, R9
		////////////////////////////////////////		
		Instruction load = new Instruction("LD", 0);
		ArrayList<String> loadList = new ArrayList<String>();
		loadList.add("R3");
		loadList.add("20");
		loadList.add("R9");
		load.operands = loadList;
		load.memoryAddress = 1;
		
		////////////////////////////////////////
		// MUL R2, R3, R9
		////////////////////////////////////////		
		Instruction mul = new Instruction("MUL", 0);
		ArrayList<String> mulList = new ArrayList<String>();
		mulList.add("R2");
		mulList.add("R3");
		mulList.add("R9");
		mul.operands = mulList;
		mul.memoryAddress = 0;
		
		////////////////////////////////////////
		// STR R3, 20, R1
		////////////////////////////////////////		
		Instruction store2 = new Instruction("STR", 1);
		ArrayList<String> storeList2 = new ArrayList<String>();
		storeList2.add("R3");
		storeList2.add("20");
		storeList2.add("R1");
		store2.operands = storeList2;
		store2.memoryAddress = 40;
		
		////////////////////////////////////////
		// STR R4, 20, R2
		////////////////////////////////////////		
		Instruction store3 = new Instruction("STR", 1);
		ArrayList<String> storeList3 = new ArrayList<String>();
		storeList3.add("R3");
		storeList3.add("20");
		storeList3.add("R1");
		store3.operands = storeList3;
		store3.memoryAddress = 41;
		
		// WAR TEST
		System.out.println("-----------------------------------");
		System.out.println("------------ WAR TESTS ------------");
		System.out.println("TRUE  TEST 1 = " + Check.warD(i1, i2)); 		// beq(op 2) then mul
		System.out.println("TRUE  TEST 2 = " + Check.warD(i1, i22)); 		// beq(op 1) then mul
		System.out.println("TRUE  TEST 3 = " + Check.warD(i2, i22));		// mul then mul
		System.out.println("TRUE  TEST 4 = " + Check.warD(store, load));	// str then ld
		System.out.println("TRUE  TEST 4r= " + Check.warD(load, store));	// str then ld
		System.out.println("TRUE  TEST 5 = " + Check.warD(store, i2));		// str then mul (same first operand)
		System.out.println("TRUE  TEST 6 = " + Check.warD(mul, load));		// mul then load (diagonal match)
	
		System.out.println("");

		System.out.println("FALSE TEST 1 = " + Check.warD(i1,store2)); 		// beq then store
		System.out.println("FALSE TEST 2 = " + Check.warD(i2, i111)); 		// mul then beq
		System.out.println("FALSE TEST 3 = " + Check.warD(store2, store3));	// store then store

		
		// WAW TEST
		System.out.println("-----------------------------------");
		System.out.println("------------ WAW TESTS ------------");
		System.out.println("TRUE TEST 1 = " + Check.wawD(i4, i3));
		System.out.println("TRUE TEST 1 = " + Check.wawD(i2, load));

		System.out.println("");
		
		System.out.println("FALSE TEST 1 = " + Check.wawD(i1, i4));
		System.out.println("FALSE TEST 2 = " + Check.wawD(i1, i22));
		System.out.println("FALSE TEST 3 = " + Check.wawD(store2, store3));	// store then store

		
		// RAW TEST
		System.out.println("-----------------------------------");
		System.out.println("------------ RAW TESTS ------------");
		System.out.println("TRUE TEST 1 = " + Check.rawD(i2, i111)); // mul then beq
		System.out.println("TRUE TEST 2 = " + Check.rawD(i2, i4));   // mul then add
		System.out.println("TRUE TEST 3 = " + Check.rawD(load, i4)); // load then add
		
		System.out.println("");
		
		System.out.println("FALSE TEST 1 = " + Check.rawD(store, i3));
		System.out.println("FALSE TEST 2 = " + Check.rawD(store, i2));
		System.out.println("FALSE TEST 3 = " + Check.rawD(store2, store3));	// store then store


		
	}
	
}
