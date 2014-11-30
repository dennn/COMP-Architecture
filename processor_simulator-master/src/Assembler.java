import java.io.BufferedReader;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;


public class Assembler {

	private ArrayList<Instruction> listOfInstructions;
	public static List<Label> labels;

	
	Assembler()
	{
		listOfInstructions = new ArrayList<Instruction>();
		labels = new ArrayList<Label>();
	}
	
	public ArrayList<Instruction>getListOfInstructions()
	{
		return listOfInstructions;
	}

	public void parse(String filename) throws FileNotFoundException
	{
		try
		{
			BufferedReader r = new BufferedReader(new FileReader(filename));
			doParse(r);
			r.close();
		}
		catch (IOException e)
		{
			e.printStackTrace();
		}
	}

	private void doParse(BufferedReader r)
	{
		String line;
		try {
			int lineNumber = 0;
			
			while ((line = r.readLine()) != null)
			{
				//String[] tokens = line.split(",");
				line = line.trim();
				line = stripComments(line);
				line = stripAndStoreLabels(line, lineNumber);
				line = line.trim();
				buildListOfInstructions(line, lineNumber);
				lineNumber++;
			}
		}
		catch (IOException e)
		{
			e.printStackTrace();
		}

	}

	private void buildListOfInstructions(String line, int lineNumber) {
		// Ignore empty lines
		if (line.equals("")) return;
	
		Instruction newInstruction = new Instruction();
		String[] operation = line.split(" ");
		if (operation.length<1)
		{
			System.err.println("Malformed input: instruction missing or space after instruction missing");
			System.exit(1);
		}
		String[] operands = line.substring(operation[0].length(), line.length()).split(",");

		// Deal with assembly directives
		if(operation[0].equals(".word"))
		{
			try {
				Simulator.memory[listOfInstructions.size()] = Integer.parseInt(operands[0].trim());
			} catch (Exception e) {
				System.err.println(".word directives only defined on the integers");
			}
		}
		
		// Add instruction
		newInstruction.instruction = operation[0];
		// Add instruction type
		if (operation[0].equals("STR"))
			newInstruction.instructionType = 1;
		else if (operation[0].equals("BEQ") || operation[0].equals("BLTH") || operation[0].equals("BNE") || operation[0].equals("B") || operation[0].equals("JR"))
			newInstruction.instructionType = 2;
		else if (operation[0].equals("BREAK") || operation[0].equals(".word"))
			newInstruction.instructionType = 3;
		else
			newInstruction.instructionType = 0;
		
		// Add dynamic branch info
		if(newInstruction.instructionType==2)
		{
			newInstruction.branchSchemeVal = 0;
		}
		
		// Add operands
		for(int i =0; i<operands.length; i++)
		{
			newInstruction.operands.add(operands[i].trim());
			newInstruction.workingOperands.add(operands[i].trim());
		}
		
		// Add memory location
		newInstruction.memoryAddress = listOfInstructions.size();
		
		// Add destination register
		newInstruction.destinationRegister = getDestinationRegister(newInstruction);
		
		//Cull NOPs and add new instruction
		if(!newInstruction.instruction.equals("NOP"))
			listOfInstructions.add(newInstruction);
	}
	
	private String stripComments(String line)
	{
		if (line.startsWith("#")) return "";
		String[] split = line.split("#");

		if (split.length!=0)
		{
			return split[0];
		}
		else
			return line;
	}

	private String stripAndStoreLabels(String line, int lineNumber)
	{
		if (line.equals("")) return line;
		if (line.contains(":"))
		{
			String[] split = line.split(":");
			if (split.length!=0)
				labels.add(new Label(listOfInstructions.size(), split[0]));
			if (split.length>1)
				return split[1];
			else
				return "";
		}
		return line;	
	}

	public void writeLabelLocations() {
		for(int i =0; i<listOfInstructions.size(); i++)
		{
			for(int j=0; j<listOfInstructions.get(i).operands.size(); j++)
			{
				for(Label l : Assembler.labels)
					if(listOfInstructions.get(i).operands.get(j).equals(l.getLabelValue()))
					{
						listOfInstructions.get(i).operands.set(j, l.getMemoryLocation() + "") ;
						listOfInstructions.get(i).workingOperands.set(j, l.getMemoryLocation() + "") ;
					}
			}
		}
	}
	
	public String getDestinationRegister(Instruction inst) {
		if (inst.instructionType!=3)
		{
			try{
				return inst.operands.get(0);
			} catch (Exception e)
			{
				System.err.println("Couldnt pickup destination parameter like expected on instruction: " + inst.instruction);
			}
		}
		return "UNDEFINED";
	}
}
