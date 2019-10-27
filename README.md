# pymachining
A Python module to help with machining calculations. 
I needed this to compare theoretical and empirical measurements from machining. 

The (possibly outdated) class hierarchy is: 
<pre>
PyMachiningBase (pymachining.base)
    Tool(PyMachiningBase) (pymachining.tools)
        Drill(Tool) (pymachining.tools)
            DrillHSS(Drill) (pymachining.tools)
                DrillHSSJobber(DrillHSS) (pymachining.tools)
                DrillHSSStub(DrillHSS) (pymachining.tools)
    MachineType(PyMachiningBase) (pymachining.machines)
        LatheMachine(MachineType) (pymachining.machines)
        MillingMachine(MachineType) (pymachining.machines)
            VerticalMillingMachine(MillingMachine) (pymachining.machines)
                MachinePM25MV(VerticalMillingMachine) (pymachining.machines)
                MachinePM25MV_DMMServo(VerticalMillingMachine) (pymachining.machines)
    MachiningOp(PyMachiningBase) (pymachining.operations)
        DrillOp(MachiningOp) (pymachining.operations)
        MillingOp(MachiningOp) (pymachining.operations)
            FaceMillOp(MillingOp) (pymachining.operations)
    MaterialType(PyMachiningBase) (pymachining.materials)
        MaterialAluminum(MaterialType) (pymachining.materials)
        MaterialSteel(MaterialType) (pymachining.materials)
            MaterialSteelMild(MaterialSteel) (pymachining.materials)
            MaterialSteelMedium(MaterialSteel) (pymachining.materials)
            MaterialSteelHigh(MaterialSteel) (pymachining.materials)
    ToolMaterialType(PyMachiningBase) (pymachining.tool_materials)
        ToolMaterialHSS(ToolMaterialType) (pymachining.tool_materials)
        ToolMaterialCarbide(ToolMaterialType) (pymachining.tool_materials)
        
BaseException(object) (builtins)
    Exception(BaseException) (builtins)
        PyMachiningException(Exception) (pymachining.base)
            ToolMaterialUnknown(PyMachiningException) (pymachining.tool_materials)
            MaterialUnknown(PyMachiningException) (pymachining.materials)
            ToolIncompatibleMaterial(PyMachiningException) (pymachining.tools)
</pre>