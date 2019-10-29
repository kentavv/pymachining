from .base import *
from .units import *


class ToolMaterialUnknown(PyMachiningException):
    def __init__(self, s=''):
        PyMachiningException.__init__(self)
        self.description = s


def ToolMaterial(material_name):
    if material_name.lower() in ['hss']:
        return ToolMaterialHSS()
    elif material_name.lower() in ['carbide']:
        return ToolMaterialCarbide()
    else:
        raise ToolMaterialUnknown(material_name)


class ToolMaterialType(PyMachiningBase):
    def __init__(self):
        PyMachiningBase.__init__(self)
        self.description = 'Unknown tool material'


class ToolMaterialHSS(ToolMaterialType):
    def __init__(self):
        ToolMaterialType.__init__(self)
        self.description = 'High speed steel tool material'


class ToolMaterialCarbide(ToolMaterialType):
    def __init__(self):
        ToolMaterialType.__init__(self)
        self.description = 'Carbide tool material'
