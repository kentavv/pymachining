from pymachining.base import *
from pymachining.units import *
from pymachining.tool_materials import *


class MaterialUnknown(PyMachiningException):
    def __init__(self, material_name=''):
        PyMachiningException.__init__(self)
        self.material_name = material_name


def Material(material_name):
    if material_name.lower() in ['aluminum', '6061']:
        return MaterialAluminum()
    elif material_name.lower() in ['steel', 'steel-mild', '12l14']:
        # low-carbon steel, 0.04% to 0.30% carbon
        # related, free-machining steels are steels that easily produce chips
        return MaterialSteelMild()
    elif material_name.lower() in ['steel-medium']:
        # medium-carbon steel, 0.31% to 0.60% carbon
        return MaterialSteelMedium()
    elif material_name.lower() in ['steel-high']:
        # high-carbon steel, tool steel, 0.61% to 1.50% carbon
        return MaterialSteelHigh()
    else:
        raise MaterialUnknown(material_name)


class MaterialType(PyMachiningBase):
    def __init__(self):
        PyMachiningBase.__init__(self)
        self.description = 'Unknown material'
        self.specific_cutting_force = float('inf')
        self.specific_cutting_energy = float('inf')

    def sfm(self):
        # Roughing and finishing cuts could have different sfms, as could different operations
        # E.g., https://engmachineshop.wustl.edu/items/cutting-speeds-for-materials/
        # and https://www.autodesk.com/products/fusion-360/blog/speeds-feeds-new-cnc-machinists/
        return Q_(float('inf'), 'feet tpm')

    def speed(self):
        return self.sfm().to('mm * turn / minute')

    def specific_cutting_energy(self):
        return float('inf')

    def machinability(self):
        return 1.


class MaterialAluminum(MaterialType):
    def __init__(self):
        MaterialType.__init__(self)
        self.description = 'Aluminum material'
        self.specific_cutting_force = float('inf')

        # The way units are written in text may not be the way they should be written in code.
        # From Metal Cutting Theory and Practice, Table 2.1
        # book:spec
        # v = Q_(.012, 'kilowatt / cm**3 / min')
        # code:
        # v = Q_(.012, 'kilowatt / (cm ** 3 / min)')

        # From Metal Cutting Theory and Practice, Table 2.1, Aluminum alloys row
        specific_cutting_energy = [0.012, 0.022]
        specific_cutting_energy_avg = (specific_cutting_energy[0] + specific_cutting_energy[1]) / 2.
        self.specific_cutting_energy = Q_(specific_cutting_energy_avg, 'kilowatt / (cm ** 3 / min)')
        self.specific_cutting_energy = Q_(specific_cutting_energy[0], 'kilowatt / (cm ** 3 / min)')

    def sfm(self, tool_material=None):
        if tool_material is None:
            tool_material = ToolMaterialHSS()

        # Aluminum and its Alloys
        if isinstance(tool_material, ToolMaterialHSS):
            sfm_range = [200, 300]
        elif isinstance(tool_material, ToolMaterialCarbide):
            sfm_range = [1200, 1200]
            # The upper limit could be max(1200, spindle.max_rpm)

        v = Q_((sfm_range[0] + sfm_range[1]) / 2., 'feet tpm')
        v = Q_(sfm_range[0], 'feet tpm')

        return v

    def machinability(self):
        return machinability('aluminum, cold drawn')


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


class MaterialSteel(MaterialType):
    def __init__(self):
        MaterialType.__init__(self)
        self.description = 'Unknown steel material'
        self.specific_cutting_force = float('inf')


class MaterialSteelMild(MaterialSteel):
    def __init__(self):
        MaterialSteel.__init__(self)
        self.description = 'Steel, low-carbon steel, 0.04% to 0.30% carbon, material'

        # From Metal Cutting Theory and Practice, Table 2.1, Steels-soft row
        specific_cutting_energy = [0.05, 0.066]
        specific_cutting_energy_avg = (specific_cutting_energy[0] + specific_cutting_energy[1]) / 2.
        self.specific_cutting_energy = Q_(specific_cutting_energy_avg, 'kilowatt / (cm ** 3 / min)')
        self.specific_cutting_energy = Q_(specific_cutting_energy[0], 'kilowatt / (cm ** 3 / min)')

    def sfm(self, tool_material=None):
        if tool_material is None:
            tool_material = ToolMaterialHSS()

        # Values from https://www.autodesk.com/products/fusion-360/blog/speeds-feeds-new-cnc-machinists/
        if isinstance(tool_material, ToolMaterialHSS):
            sfm_range = [30, 50]
        elif isinstance(tool_material, ToolMaterialCarbide):
            sfm_range = [60, 90]

        v = Q_((sfm_range[0] + sfm_range[1]) / 2., 'feet tpm')
        v = Q_(sfm_range[0], 'feet tpm')

        return v

    def machinability(self):
        return machinability('1212')


class MaterialSteelMedium(MaterialSteel):
    def __init__(self):
        MaterialSteel.__init__(self)
        self.description = 'Steel, medium-carbon steel, 0.31% to 0.60% carbon, material'

        # From Metal Cutting Theory and Practice, Table 2.1, Steels-0<Rc<45 row
        specific_cutting_energy = [0.065, 0.09]
        specific_cutting_energy_avg = (specific_cutting_energy[0] + specific_cutting_energy[1]) / 2.
        self.specific_cutting_energy = Q_(specific_cutting_energy_avg, 'kilowatt / (cm ** 3 / min)')
        self.specific_cutting_energy = Q_(specific_cutting_energy[0], 'kilowatt / (cm ** 3 / min)')

    def sfm(self, tool_material=None):
        if tool_material is None:
            tool_material = ToolMaterialHSS()

        # Values from https://www.autodesk.com/products/fusion-360/blog/speeds-feeds-new-cnc-machinists/
        if isinstance(tool_material, ToolMaterialHSS):
            sfm_range = [15, 20]
        elif isinstance(tool_material, ToolMaterialCarbide):
            sfm_range = [60, 90]

        v = Q_((sfm_range[0] + sfm_range[1]) / 2., 'feet tpm')
        v = Q_(sfm_range[0], 'feet tpm')

        return v

    def machinability(self):
        return machinability('1050')


class MaterialSteelHigh(MaterialSteel):
    def __init__(self):
        MaterialSteel.__init__(self)
        self.description = 'Steel, high-carbon steel, 0.61% to 1.50% carbon, tool steel, material'

        # From Metal Cutting Theory and Practice, Table 2.1, Steels-50<Rc<60 row
        specific_cutting_energy = [0.09, 0.2]
        specific_cutting_energy_avg = (specific_cutting_energy[0] + specific_cutting_energy[1]) / 2.
        self.specific_cutting_energy = Q_(specific_cutting_energy_avg, 'kilowatt / (cm ** 3 / min)')
        self.specific_cutting_energy = Q_(specific_cutting_energy[0], 'kilowatt / (cm ** 3 / min)')

    def sfm(self, tool_material=None):
        if tool_material is None:
            tool_material = ToolMaterialHSS()

        # Values from https://www.autodesk.com/products/fusion-360/blog/speeds-feeds-new-cnc-machinists/
        if isinstance(tool_material, ToolMaterialHSS):
            sfm_range = [7, 15]
        elif isinstance(tool_material, ToolMaterialCarbide):
            sfm_range = [60, 90]

        v = Q_((sfm_range[0] + sfm_range[1]) / 2., 'feet tpm')
        v = Q_(sfm_range[0], 'feet tpm')

        return v

    def machinability(self):
        return machinability('A-2')


def machinability(s):
    # May be able to scale cutting parameters, SFM in particular, using machinability values.
    # https://en.wikipedia.org/wiki/Machinability

    # machinability table from: http://www.carbidedepot.com/formulas-machinability.htm
    d = {
        # Carbon steels
        '1015': .72,
        '1018': .78,
        '1020': .72,
        '1022': .78,
        '1030': .70,
        '1040': .64,
        '1042': .64,
        '1050': .54,
        '1095': .42,
        '1117': .91,
        '1137': .72,
        '1141': .70,
        '1141-annealed': .81,
        '1144': .76,
        '1144-annealed': .85,
        '1144-stressproof': .83,
        '1212': 1.00,
        '1213': 1.36,
        '12L14': 1.70,
        '1215': 1.36,

        # Alloy steels:
        '2355-annealed': .70,
        '4130-annealed': .72,
        '4140-annealed': .66,
        '4142-annealed': .66,
        '41L42-annealed': .77,
        '4150-annealed': .60,
        '4340-annealed': .57,
        '4620': .66,
        '4820-annealed': .49,
        '52100-annealed': .40,
        '6150-annealed': .60,
        '8620': .66,
        '86L20': .77,
        '9310-annealed': .51,

        # Stainless Steels and Super Alloys:
        '302-annealed': .45,
        '303-annealed': .78,
        '304-annealed': .45,
        '316-annealed': .45,
        '321-annealed': .36,
        '347-annealed': .36,
        '410-annealed': .54,
        '416-annealed': 1.10,
        '420-annealed': .45,
        '430-annealed': .54,
        '431-annealed': .45,
        '440A': .45,
        '15-5PH condition A': .48,
        '17-4PH condition A': .48,
        'A286 aged': .33,
        'Hastelloy X': .19,

        # Tool Steels
        'A-2': .42,
        'A-6': .33,
        'D-2': .27,
        'D-3': .27,
        'M-2': .39,
        'O-1': .42,
        'O-2': .42,

        # Gray Cast Iron
        'ASTM class 20 annealed': .73,
        'ASTM class 25': .55,
        'ASTM class 30': .48,
        'ASTM class 35': .48,
        'ASTM class 40': .48,
        'ASTM class 45': .36,
        'ASTM class 50': .36,

        # Nodular Iron
        '60-40-18 annealed': .61,
        '65-45-12 annealed': .61,
        '80-55-06': .39,

        # Aluminum and Magnesium Alloys:
        'aluminum, cold drawn': 3.60,
        'aluminum, cast': 4.50,
        'aluminum, die cast': .76,
        'magnesium, cold drawn': 4.80,
        'magnesium, cast': 4.80
    }

    try:
        return d[s]
    except IndexError:
        raise MaterialUnknown(s)
