from pymachining.units import *
from pymachining.tool_materials import *


class MaterialUnknown(Exception):
    def __init__(self, s):
        self.aaa = s


def Material(material_name):
    if material_name.lower() in ['aluminum', '6061']:
        return MaterialAluminum()
    else:
        raise MaterialUnknown(material_name)


class MaterialType:
    def __init__(self):
        self.specific_cutting_force = float('inf')
        self.specific_cutting_energy = float('inf')

    def sfm(self):
        return float('inf') * (ureg.feet * ureg.tpm)

    def speed(self):
        return self.sfm().to('mm * turn / minute')

    def specific_cutting_energy(self):
        return float('inf')


class MaterialAluminum(MaterialType):
    def __init__(self):
        MaterialType.__init__(self)
        self.specific_cutting_force = float('inf')

        # The way units are written in text may not be the way they should be written in code.
        # From Metal Cutting Theory and Practice, Table 2.1
        # book:spec
        # v = .065 * (ureg.kilowatt / ureg.cm**3 / ureg.min)
        # code:
        # v = .065 * (ureg.kilowatt / (ureg.cm ** 3 / ureg.min))
        specific_cutting_energy = [0.012, 0.022]
        self.specific_cutting_energy = (specific_cutting_energy[0] + specific_cutting_energy[1]) / 2. * (ureg.kilowatt / (ureg.cm ** 3 / ureg.min))
        self.specific_cutting_energy = specific_cutting_energy[0] * (ureg.kilowatt / (ureg.cm ** 3 / ureg.min))

    def sfm(self, tool_material=None):
        if tool_material is None:
            tool_material = ToolMaterialHSS()

        # Aluminum and its Alloys
        if isinstance(tool_material, ToolMaterialHSS):
            sfm_range = [200, 300]
        v = (sfm_range[0] + sfm_range[1]) / 2.
        v = sfm_range[0]
        v *= ureg.feet * ureg.tpm
        # v.ito('feet * turn / minute')
        return v

# def sfm_(self):
#     v = float('inf')
#
#     # Ranges from http://www.norsemandrill.com/feeds-speeds-drill.php
#
#     if isinstance(self.tool_material, ToolMaterialHSS):
#         material = ''
#
#         # Recommended Speeds for Standard Materials with H.S.S. Drills
#         if isinstance(self.material, MaterialAluminum) or material == 'aluminum':
#             # Aluminum and its Alloys
#             sfm_range = [200, 300]
#         elif material in ['brass', 'bronze']:
#             # Brass and Bronze (Ordinary)
#             sfm_range = [150, 300]
#         elif material == 'bronze_high_tensile':
#             # Bronze (High Tensile)
#             sfm_range = [70, 150]
#         elif material == 'die_casting_zinc_base':
#             # Die Casting (Zinc Base)
#             sfm_range = [300, 400]
#         elif material == 'iron_cast_soft':
#             # Iron-Cast (Soft)
#             sfm_range = [75, 125]
#         elif material == 'iron_cast_medium_hard':
#             # Iron-Cast (Medium Hard)
#             sfm_range = [50, 100]
#         elif material == 'iron_cast_hard_chilled':
#             # Iron-Cast (Hard Chilled)
#             sfm_range = [10, 20]
#         elif material == 'iron_cast_malleable':
#             # Iron-Cast (Malleable)
#             sfm_range = [80, 90]
#         elif material == 'magnesium':
#             # Magnesium and its Alloys
#             sfm_range = [250, 400]
#         elif material in ['monel_metal', 'high-nickel_steel', 'stainless_steel']:
#             # Monel Metal or High-Nickel Steel, Stainless Steel
#             sfm_range = [30, 50]
#         elif material in ['plastics']:
#             # Plastics or Similar Materials
#             sfm_range = [100, 300]
#         elif material in ['steel_mild']:
#             # Steel - Mild .2 carbon to .3 carbon
#             sfm_range = [80, 110]
#         elif material in ['steel']:
#             # Steel - Steel .4 carbon to .5 carbon
#             sfm_range = [70, 80]
#         elif material in ['steel_tool']:
#             # Steel - Tool 1.2 carbon
#             sfm_range = [50, 60]
#         elif material in ['steel_forgings']:
#             # Steel - Forgings
#             sfm_range = [40, 50]
#         elif material in ['steel_alloy']:
#             # Steel - Alloy - 300 to 400 Brinell
#             sfm_range = [20, 30]
#
#         v = sfm_range[0]
#
#     return v
