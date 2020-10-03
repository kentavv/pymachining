# PyMachining
PyMachining is a Python module to help understand and optimize machining
operations. Values including operational parameters (feeds and speeds),
efficiency (material removal rate), and demand (power requirements)
are easily calculated. 

After a machine is defined, tool and stock materials selected, tool selected,
and an operation is defined, calculations can be performed. With all this
information, one can optimize parameters, find theoretical limits, and plot
alternatives.

There are other applications, offline and online, for performing similar
calculations; each tool manufacturer seems to have one. There are also
tools that are more general advisors. These may be perfect for a production
environment. 

I wrote PyMachining to help compare theoretical and empirical machining
measurements and to generate good starting parameters for use in CAM programs
including Autodesk Fusion360. Already available tools are generally
blackboxes and I wanted to better understand the theory of machining. When
equations are shown, it's not always clear how they were derived. PyMachining
tries to improve the documentation of the equations by Pint quantities that
hold a value and unit. Initial attention was on drilling since it's a
relatively easy operation to measure. 

For examples of how to use PyMachining start with real-world useful examples
in assistant.py. This file uses PyMachining to help generate CAM parameters.
Tests.py might also be for examples lesser used routines.
