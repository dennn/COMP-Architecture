public class Label {
	private int memoryLocation;
	private String labelValue;
	
	Label(int a, String b)
	{
		memoryLocation = a;
		labelValue = b;
	}
	
	public int getMemoryLocation() {
		return memoryLocation;
	}

	public void setMemoryLocation(int memoryLocation) {
		this.memoryLocation = memoryLocation;
	}

	public String getLabelValue() {
		return labelValue;
	}

	public void setLabelValue(String labelValue) {
		this.labelValue = labelValue;
	}

}
