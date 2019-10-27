from pymachining.units import *


class ToolMaterialUnknown(Exception):
    def __init__(self, s):
        self.aaa = s


def ToolMaterial(material_name):
    if material_name.lower() in ['hss']:
        return ToolMaterialHSS()
    elif material_name.lower() in ['carbide']:
        return ToolMaterialCarbide()
    else:
        raise ToolMaterialUnknown(material_name)


class ToolMaterialType:
    def __init__(self):
        self.description = 'Unknown tool material'


class ToolMaterialHSS(ToolMaterialType):
    def __init__(self):
        ToolMaterialType.__init__(self)
        self.description = 'High speed steel tool material'


class ToolMaterialCarbide(ToolMaterialType):
    def __init__(self):
        ToolMaterialType.__init__(self)
        self.description = 'Carbide tool material'
