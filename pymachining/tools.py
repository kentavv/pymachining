import numpy as np
import pylab

from .base import *
from .units import *
from .materials import *
from .tool_materials import *


class ToolIncompatibleMaterial(PyMachiningException):
    def __init__(self, s=''):
        PyMachiningException.__init__(self)
        self.description = s


class Tool(PyMachiningBase):
    def __init__(self, diameter, tool_material):
        PyMachiningBase.__init__(self)
        self.description = 'Unknown tool'
        self.diameter = diameter
        self.tool_material = tool_material
        pass

    def feed(self, stock_material):
        pass

    def speed(self, stock_material):
        pass

    def feed_rate(self, stock_material):
        return float('inf')

    def sfm(self, stock_material):
        return float('inf')

    @classmethod
    def plot_feedrate(cls, stock_material):
        pass


class Drill(Tool):
    def __init__(self, diameter, tool_material):
        Tool.__init__(self, diameter, tool_material)
        self.description = 'Unknown drill'
        if diameter in self.letters_and_numbers_and_fractions:
            self.diameter = Q_(self.letters_and_numbers_and_fractions[diameter][1], 'mm')
        self.drill_style = 'unknown'

    # Table values from https://en.wikipedia.org/wiki/Drill_bit_sizes
    letters_and_numbers_and_fractions = {'#104': [0.0031, 0.079],
                                         '#103': [0.0035, 0.089],
                                         '#102': [0.0039, 0.099],
                                         '#101': [0.0043, 0.109],
                                         '#100': [0.0047, 0.119],
                                         '#99': [0.0051, 0.130],
                                         '#98': [0.0055, 0.140],
                                         '#97': [0.0059, 0.150],
                                         '#96': [0.0063, 0.160],
                                         '#95': [0.0067, 0.170],
                                         '#94': [0.0071, 0.180],
                                         '#93': [0.0075, 0.191],
                                         '#92': [0.0079, 0.201],
                                         '#91': [0.0083, 0.211],
                                         '#90': [0.0087, 0.221],
                                         '#89': [0.0091, 0.231],
                                         '#88': [0.0095, 0.241],
                                         '#87': [0.010, 0.254],
                                         '#86': [0.0105, 0.267],
                                         '#85': [0.011, 0.279],
                                         '#84': [0.0115, 0.292],
                                         '#83': [0.012, 0.305],
                                         '#82': [0.0125, 0.318],
                                         '#81': [0.013, 0.330],
                                         '#80': [0.0135, 0.343],
                                         '#79': [0.0145, 0.368],
                                         '#78': [0.016, 0.406],
                                         '#77': [0.018, 0.457],
                                         '#76': [0.020, 0.508],
                                         '#75': [0.021, 0.533],
                                         '#74': [0.0225, 0.572],
                                         '#73': [0.024, 0.610],
                                         '#72': [0.025, 0.635],
                                         '#71': [0.026, 0.660],
                                         '#70': [0.028, 0.711],
                                         '#69': [0.0292, 0.742],
                                         '#68': [0.031, 0.787],
                                         '#67': [0.032, 0.813],
                                         '#66': [0.033, 0.838],
                                         '#65': [0.035, 0.889],
                                         '#64': [0.036, 0.914],
                                         '#63': [0.037, 0.940],
                                         '#62': [0.038, 0.965],
                                         '#61': [0.039, 0.991],
                                         '#60': [0.040, 1.016],
                                         '#59': [0.041, 1.041],
                                         '#58': [0.042, 1.067],
                                         '#57': [0.043, 1.092],
                                         '#56': [0.0465, 1.181],
                                         '#55': [0.052, 1.321],
                                         '#54': [0.055, 1.397],
                                         '#53': [0.0595, 1.511],
                                         '#52': [0.0635, 1.613],
                                         '#51': [0.067, 1.702],
                                         '#50': [0.070, 1.778],
                                         '#49': [0.073, 1.854],
                                         '#48': [0.076, 1.930],
                                         '#47': [0.0785, 1.994],
                                         '#46': [0.081, 2.057],
                                         '#45': [0.082, 2.083],
                                         '#44': [0.086, 2.184],
                                         '#43': [0.089, 2.261],
                                         '#42': [0.0935, 2.375],
                                         '#41': [0.096, 2.438],
                                         '#40': [0.098, 2.489],
                                         '#39': [0.0995, 2.527],
                                         '#38': [0.1015, 2.578],
                                         '#37': [0.104, 2.642],
                                         '#36': [0.1065, 2.705],
                                         '#35': [0.110, 2.794],
                                         '#34': [0.111, 2.819],
                                         '#33': [0.113, 2.870],
                                         '#32': [0.116, 2.946],
                                         '#31': [0.120, 3.048],
                                         '#30': [0.1285, 3.264],
                                         '#29': [0.136, 3.454],
                                         '#28': [0.1405, 3.569],
                                         '#27': [0.144, 3.658],
                                         '#26': [0.147, 3.734],
                                         '#25': [0.1495, 3.797],
                                         '#24': [0.152, 3.861],
                                         '#23': [0.154, 3.912],
                                         '#22': [0.157, 3.988],
                                         '#21': [0.159, 4.039],
                                         '#20': [0.161, 4.089],
                                         '#19': [0.166, 4.216],
                                         '#18': [0.1695, 4.305],
                                         '#17': [0.173, 4.394],
                                         '#16': [0.177, 4.496],
                                         '#15': [0.180, 4.572],
                                         '#14': [0.182, 4.623],
                                         '#13': [0.185, 4.699],
                                         '#12': [0.189, 4.801],
                                         '#11': [0.191, 4.851],
                                         '#10': [0.1935, 4.915],
                                         '#9': [0.196, 4.978],
                                         '#8': [0.199, 5.055],
                                         '#7': [0.201, 5.105],
                                         '#6': [0.204, 5.182],
                                         '#5': [0.2055, 5.220],
                                         '#4': [0.209, 5.309],
                                         '#3': [0.213, 5.410],
                                         '#2': [0.221, 5.613],
                                         '#1': [0.228, 5.791],
                                         'A': [0.234, 5.944],
                                         'B': [0.238, 6.045],
                                         'C': [0.242, 6.147],
                                         'D': [0.246, 6.248],
                                         'E': [0.250, 6.350],
                                         'F': [0.257, 6.528],
                                         'G': [0.261, 6.629],
                                         'H': [0.266, 6.756],
                                         'I': [0.272, 6.909],
                                         'J': [0.277, 7.036],
                                         'K': [0.281, 7.137],
                                         'L': [0.290, 7.366],
                                         'M': [0.295, 7.493],
                                         'N': [0.302, 7.671],
                                         'O': [0.316, 8.026],
                                         'P': [0.323, 8.204],
                                         'Q': [0.332, 8.433],
                                         'R': [0.339, 8.611],
                                         'S': [0.348, 8.839],
                                         'T': [0.358, 9.093],
                                         'U': [0.368, 9.347],
                                         'V': [0.377, 9.576],
                                         'W': [0.386, 9.804],
                                         'X': [0.397, 10.08],
                                         'Y': [0.404, 10.26],
                                         'Z': [0.413, 10.49],
                                         '1⁄64': [0.015625, 0.396875],
                                         '1⁄32': [0.03125, 0.79375],
                                         '3⁄64': [0.046875, 1.190625],
                                         '1⁄16': [0.0625, 1.5875],
                                         '5⁄64': [0.078125, 1.984375],
                                         '3⁄32': [0.09375, 2.38125],
                                         '7⁄64': [0.109375, 2.778125],
                                         '1⁄8': [0.125, 3.175],
                                         '9⁄64': [0.140625, 3.571875],
                                         '5⁄32': [0.15625, 3.96875],
                                         '11⁄64': [0.171875, 4.365625],
                                         '3⁄16': [0.1875, 4.7625],
                                         '13⁄64': [0.203125, 5.159375],
                                         '7⁄32': [0.21875, 5.55625],
                                         '15⁄64': [0.234375, 5.953125],
                                         '1⁄4': [0.250, 6.350],
                                         '17⁄64': [0.265625, 6.746875],
                                         '9⁄32': [0.28125, 7.14375],
                                         '19⁄64': [0.296875, 7.540625],
                                         '5⁄16': [0.3125, 7.9375],
                                         '21⁄64': [0.328125, 8.334375],
                                         '11⁄32': [0.34375, 8.73125],
                                         '23⁄64': [0.359375, 9.128125],
                                         '3⁄8': [0.375, 9.525],
                                         '25⁄64': [0.390625, 9.921875],
                                         '13⁄32': [0.40625, 10.31875],
                                         '27⁄64': [0.421875, 10.715625],
                                         '7⁄16': [0.4375, 11.1125],
                                         '29⁄64': [0.453125, 11.509375],
                                         '15⁄32': [0.46875, 11.90625],
                                         '31⁄64': [0.484375, 12.303125],
                                         '1⁄2': [0.500, 12.700],
                                         '33⁄64': [0.515625, 13.096875],
                                         '17⁄32': [0.53125, 13.49375],
                                         '35⁄64': [0.546875, 13.890625],
                                         '9⁄16': [0.5625, 14.2875],
                                         '37⁄64': [0.578125, 14.684375],
                                         '19⁄32': [0.59375, 15.08125],
                                         '39⁄64': [0.609375, 15.478125],
                                         '5⁄8': [0.625, 15.875],
                                         '41⁄64': [0.640625, 16.271875],
                                         '21⁄32': [0.65625, 16.66875],
                                         '43⁄64': [0.671875, 17.065625],
                                         '11⁄16': [0.6875, 17.4625],
                                         '45⁄64': [0.703125, 17.859375],
                                         '23⁄32': [0.71875, 18.25625],
                                         '47⁄64': [0.734375, 18.653125],
                                         '3⁄4': [0.750, 19.050],
                                         '49⁄64': [0.765625, 19.446875],
                                         '25⁄32': [0.78125, 19.84375],
                                         '51⁄64': [0.796875, 20.240625],
                                         '13⁄16': [0.8125, 20.6375],
                                         '53⁄64': [0.828125, 21.034375],
                                         '27⁄32': [0.84375, 21.43125],
                                         '55⁄64': [0.859375, 21.828125],
                                         '7⁄8': [0.875, 22.225],
                                         '57⁄64': [0.890625, 22.621875],
                                         '29⁄32': [0.90625, 23.01875],
                                         '59⁄64': [0.921875, 23.415625],
                                         '15⁄16': [0.9375, 23.8125],
                                         '61⁄64': [0.953125, 24.209375],
                                         '31⁄32': [0.96875, 24.60625],
                                         '63⁄64': [0.984375, 25.003125],
                                         '1': [1.000, 25.400]
                                         }


class DrillHSS(Drill):
    def __init__(self, diameter):
        Drill.__init__(self, diameter, ToolMaterialHSS())
        self.description = 'HSS (jobber?) drill'
        self.drill_style = 'jobber'

    def feed_rate_(self, stock_material, drill_len, fit=True):
        # https://www.dormerpramet.com/Downloads/RoundTool_Speeds_and_Feeds.pdf

        # The drill sets that I have are:

        # Jobber length:
        #     Precision Twist Drill C252A 1-13MX.5M PTD BRT MET JOBBER DR SET
        #         1 to 13mm, 118° Point, Bright Finish High Speed Steel Jobber Length Drill Bit Set
        #         General Purpose, Standard Point, Straight Shank
        #         DIN338, 4xD, 118°
        #         Style: 2A    7.2:98I, 7.3:89H
        #     Precision Twist Drill C29R10P 1/16-1/2X64THS PTD BRT JOBBER DRILL SET
        #         1/16 to 1/2", 118° Point, Bright Finish High Speed Steel Jobber Length Drill Bit Set
        #         General Purpose, Standard Point, Straight Shank, Series R10P
        #         ANSI, 4xD, 118°
        #         Style: R10P  7.2:98I, 7.3:89H
        #     Precision Twist Drill C60R18P #1-#60 W/CS PTD BRT JOBBER DRILL SET
        #         #60 to 1, 118° Point, Bright Finish High Speed Steel Jobber Length Drill Bit Set
        #         General Purpose, Standard Point, Straight Shank, Series R18P
        #         ANSI, 4xD, 118°
        #         Style: R18P  7.2:98I, 7.3:89H
        #     Precision Twist Drill C26R15P A-Z W/CS PTD HSS JOBBER DRILL SET
        #         A to Z, 118° Point, Bright Finish High Speed Steel Jobber Length Drill Bit Set
        #         General Purpose, Standard Point, Straight Shank, Series R15P
        #         ANSI, 4xD, 118°
        #         Style: R15P  7.2:98I, 7.3:89H
        #
        # Screw-machine length
        #     Precision Twist Drill C29R40 1/16-1/2X64THS PTD BRT SCREW MACH DR SET
        #         1/16 to 1/2", 118° Point, Bright Finish, High Speed Steel Screw Machine Length Drill Bit Set
        #         29 Piece, Standard Point, Straight Shank, Series R40
        #         ANSI, 2.5xD, 118°
        #         Style: R40  7.2:98J, 7.3:98I
        #     Precision Twist Drill C26R42 A-Z W/CS PTD BRT SCREW MACH DR SET
        #         118° Point, Bright Finish, High Speed Steel Screw Machine Length Drill Bit Set
        #         26 Piece, Standard Point, Straight Shank, Series R42
        #         ANSI, 2.5xD, 118°
        #         Style: R42  7.2:98J, 7.3:98I
        #     Precision Twist Drill C60R41 #1-#60 W/CS PTD BRT SCREW MACH DR SET
        #         118° Point, Bright Finish, High Speed Steel Screw Machine Length Drill Bit Set
        #         60 Piece, Standard Point, Straight Shank, Series R41
        #         ANSI, 2.5xD, 118°
        #         Style: R41  7.2:98J, 7.3:98I

        # Application Material Groups (AMG), Hardness HRC, ISO
        # 1. Steel
        # 1.1 Magnetic soft steel 12L14, 12L15 <120 HB P 1
        # 1.2 Structural Steel/ case carburising steel 1005-1025, 1214, 1215, A36 <200 HB P 1
        # 1.3 Plain Carbon steel 1030-1060, 1050-1060, 1144-1146 <24 P 2
        # 1.4 Alloy steel 4140,4340,52100,8620 H11-H41,A2,D2,01,P20,420 <24 P 3
        # 1.5 Alloy steel/ Hardened and tempered steel 4140,4340,52100,8620 H11-H41,A2,D2,01,P20,420 >24<38 P 4
        # 1.6 Alloy steel/ Hardened and tempered steel 4140,4340,52100,8620 H11-H41,A2,D2,01,P20,420 >38 H 1
        # 1.7 Alloy steel Hardened A2-D2, H10-H41, L1-L6, M1-M42, T1 49-55 H 3
        # 1.8 Alloy steel Hardened A2-D2, H10-H41, L1-L6, M1-M42, T1 55-63 H 4
        # 2. Stainless Steel
        # 2.1 Free machining Stainless Steel 200, 303, 416, 420F, 430F, 440 <24 M 1
        # 2.2 Austenitic 301, 302, 304, 316, 321, 330, CUSTOM 455, AM-350 <24 M 3
        # 2.3 Ferritic + Austenitic, Martensitic 318-329, 400-446, DUPLEX <32 M 2
        # 2.4 Precipitation Hardened 15-5PH, Custom 450 17-4PH <32 S 2
        # 3. Cast Iron
        # 3.1 Lamellar graphite Grey, G10, Gg40, J431C, A48 CLASS 20 <150 HB K 1
        # 3.2 Lamellar graphite Grey, GG25-Gg40, J158, A48 CLASS 40-60 >150 HB<32 K 2
        # 3.3 Nodular graphite/ Malleable Cast Iron A220, A436, A439, A602, Black, GGG40-GGG70 <200 HB K 3
        # 3.4 Nodular graphite/ Malleable Cast Iron Black Gts/Gtw, J434C >200 HB<32 K 4
        # 4.Titanium
        # 4.1 Titanium, unalloyed Commercially Pure <200 HB S 1
        # 4.2 Titanium, alloyed 6AI4V, 6A14V-2Sn, Monel, Monel K <28 S 2
        # 4.3 Titanium, alloyed 6AI4V-4Mo, 7A14V-4Mo, 4911-4967 >28<38 S 3
        # 5. Nickel
        # 5.1 Nickel, unalloyed Commercially Pure, 17644, 200, 5553 <150 HB S 1
        # 5.2 Nickel, alloyed Monel 400, Hastelloy C, Inconel 625, Waspaloy <28 S 2
        # 5.3 Nickel, alloyed Iconel 718,Nimonic 75-95,Rene 41,Iconel 825,A286 >28<38 S 3
        # 6. Copper
        # 6.1 Copper Commercially Pure <100 HB N 3
        # 6.2 ß-Brass, Bronze 314-340, 350-370 <200 HB N 4
        # 6.3 α-Brass Alloyed Cu + Al + Fe, Long Chipping <200 HB N 3
        # 6.4 High Strength Bronze Ampco 18-25 <49 N 4
        # 7. Aluminium & Magnesium
        # 7.1 Al, Mg, unalloyed Commercially Pure <100 HB N 1
        # 7.2 Al alloyed, Si<0.5% 6061 T6, 7075, 314-340 <150 HB N 1
        # 7.3 Al alloyed, Si>0.5%<10% 6061 T6, 380-390 <120 HB N 1
        # 7.4 Al alloyed, Si>10% Mg alloys Magnesium Whisker Reinforced <120 HB N 2
        # 8.Synthetic Materials
        # 8.1 Thermoplastics Ultramid, Polystrol --- O
        # 8.2 Thermosetting plastics Bakelit, Pertinax --- O
        # 8.3 Reinforced plastic materials CFK, GFKAFK --- O
        # 9.Hard Mat.
        # 9.1 Cermets (Metal-ceramics) Ferrotic <54 H
        # 10.Graphite
        # 10.1 Standard graphite --- O

        # Feed in Inches per Revolution (IPR) ± 25% Ø Diameter
        # 1mm,1/32”  2mm,3/32”    3mm,1/8”    4mm,5/32”   5mm,3/16”   6mm,1/4”    8mm,5/16”   10mm,3/8”   12mm,1/2”   15mm,9/16”  16mm,5/8”   20mm,3/4”   25mm,1” 30mm,1.1/8” 40mm,1.5/8” 50mm,2”
        # A 0.0004 0.0009 0.0011 0.0013 0.0014 0.0017 0.0021 0.0024 0.0027 0.0032 0.0034 0.0043 0.0049 0.0053 0.0061 0.0069
        # B 0.0006 0.0011 0.0015 0.0016 0.0018 0.0021 0.0026 0.0031 0.0035 0.0041 0.0043 0.0053 0.0060 0.0065 0.0074 0.0082
        # C 0.0006 0.0013 0.0017 0.0020 0.0022 0.0025 0.0031 0.0039 0.0043 0.0049 0.0051 0.0063 0.0071 0.0077 0.0087 0.0094
        # D 0.0006 0.0015 0.0021 0.0024 0.0027 0.0031 0.0039 0.0047 0.0051 0.0059 0.0061 0.0074 0.0083 0.0090 0.0100 0.0108
        # E 0.0007 0.0017 0.0024 0.0028 0.0031 0.0037 0.0045 0.0055 0.0059 0.0068 0.0071 0.0085 0.0094 0.0102 0.0112 0.0122
        # F 0.0007 0.0020 0.0029 0.0033 0.0037 0.0043 0.0054 0.0065 0.0070 0.0080 0.0083 0.0098 0.0108 0.0116 0.0126 0.0135
        # G 0.0007 0.0022 0.0033 0.0038 0.0043 0.0050 0.0063 0.0075 0.0081 0.0091 0.0094 0.0110 0.0122 0.0130 0.0140 0.0148
        # H 0.0008 0.0026 0.0040 0.0046 0.0051 0.0059 0.0075 0.0090 0.0096 0.0107 0.0110 0.0126 0.0140 0.0148 0.0157 0.0165
        # I 0.0008 0.0030 0.0047 0.0053 0.0059 0.0068 0.0087 0.0104 0.0110 0.0122 0.0126 0.0142 0.0157 0.0165 0.0173 0.0181
        # J 0.0009 0.0033 0.0053 0.0060 0.0067 0.0078 0.0098 0.0117 0.0124 0.0137 0.0142 0.0159 0.0175 0.0183 0.0191 0.0198
        # K 0.0010 0.0036 0.0059 0.0067 0.0075 0.0087 0.0110 0.0130 0.0138 0.0153 0.0157 0.0177 0.0193 0.0201 0.0209 0.0215
        # L 0.0011 0.0040 0.0065 0.0073 0.0082 0.0094 0.0120 0.0142 0.0152 0.0165 0.0169 0.0191 0.0207 0.0215 0.0224 0.0231
        # M 0.0012 0.0043 0.0071 0.0080 0.0089 0.0102 0.0130 0.0154 0.0165 0.0177 0.0181 0.0205 0.0220 0.0228 0.0238 0.0248
        # N 0.0013 0.0047 0.0077 0.0086 0.0095 0.0110 0.0140 0.0165 0.0179 0.0189 0.0193 0.0219 0.0234 0.0242 0.0253 0.0265
        # S 0.0003 0.0006 0.0008 0.0010 0.0012 0.0015 0.0020 0.0031 0.0039 0.0048 0.0051 0.0059 0.0070 0.0070 0.0090
        # T 0.0006 0.0011 0.0016 0.0020 0.0024 0.0028 0.0035 0.0043 0.0051 0.0063 0.0067 0.0075 0.0080 0.0090 0.0100
        # U 0.0010 0.0019 0.0028 0.0031 0.0035 0.0042 0.0055 0.0067 0.0079 0.0088 0.0091 0.0094 0.0110 0.0120 0.0140
        # V 0.0015 0.0027 0.0039 0.0045 0.0051 0.0060 0.0079 0.0098 0.0110 0.0122 0.0126 0.0134 0.0160 0.0170 0.0200
        # W 0.0019 0.0035 0.0051 0.0059 0.0067 0.0079 0.0102 0.0130 0.0150 0.0165 0.0169 0.0177 0.0190 0.0190 0.0200
        # X 0.0022 0.0041 0.0059 0.0071 0.0083 0.0098 0.0130 0.0165 0.0189 0.0210 0.0217 0.0228
        # Y 0.0027 0.0049 0.0071 0.0087 0.0102 0.0125 0.0169 0.0217 0.0276 0.0276 0.0276 0.0291
        # Z 0.0037 0.0068 0.0098 0.0128 0.0157 0.0210 0.0315 0.0394 0.0433 0.0463 0.0472 0.0472

        diam = self.diameter

        diam_mm = [1, 2, 3, 4, 5, 6, 8, 10, 12, 15, 16, 20, 25, 30, 40, 50]
        diam_str = ['1/32"', '3/32"', '1/8"', '5/32"', '3/16"', '1/4"', '5/16"', '3/8"', '1/2"', '9/16"', '5/8"',
                    '3/4"', '1"', '1.1/8"', '1.5/8"', '2"']
        diam_in_ = [1 / 32., 3 / 32., 1 / 8., 5 / 32., 3 / 16., 1 / 4., 5 / 16., 3 / 8., 1 / 2., 9 / 16., 5 / 8.,
                    3 / 4., 1., 1 + 1 / 8., 1 + 5 / 8., 2.]
        feed_ipr_d_ = [0.0006, 0.0015, 0.0021, 0.0024, 0.0027, 0.0031, 0.0039, 0.0047, 0.0051, 0.0059, 0.0061, 0.0074,
                       0.0083, 0.0090, 0.0100, 0.0108]
        feed_ipr_e_ = [0.0007, 0.0017, 0.0024, 0.0028, 0.0031, 0.0037, 0.0045, 0.0055, 0.0059, 0.0068, 0.0071, 0.0085,
                       0.0094, 0.0102, 0.0112, 0.0122]
        feed_ipr_f_ = [0.0007, 0.0020, 0.0029, 0.0033, 0.0037, 0.0043, 0.0054, 0.0065, 0.0070, 0.0080, 0.0083, 0.0098,
                       0.0108, 0.0116, 0.0126, 0.0135]
        feed_ipr_g_ = [0.0007, 0.0022, 0.0033, 0.0038, 0.0043, 0.0050, 0.0063, 0.0075, 0.0081, 0.0091, 0.0094, 0.0110,
                       0.0122, 0.0130, 0.0140, 0.0148]
        feed_ipr_h_ = [0.0008, 0.0026, 0.0040, 0.0046, 0.0051, 0.0059, 0.0075, 0.0090, 0.0096, 0.0107, 0.0110, 0.0126,
                       0.0140, 0.0148, 0.0157, 0.0165]
        feed_ipr_i_ = [0.0008, 0.0030, 0.0047, 0.0053, 0.0059, 0.0068, 0.0087, 0.0104, 0.0110, 0.0122, 0.0126, 0.0142,
                       0.0157, 0.0165, 0.0173, 0.0181]
        feed_ipr_j_ = [0.0009, 0.0033, 0.0053, 0.0060, 0.0067, 0.0078, 0.0098, 0.0117, 0.0124, 0.0137, 0.0142, 0.0159,
                       0.0175, 0.0183, 0.0191, 0.0198]
        if isinstance(stock_material, MaterialAluminum):
            if drill_len == 'stub':
                feed_ipr_ = feed_ipr_i_
                # feed_ipr_ = feed_ipr_j_
            else:  # elif drill_len == 'jobber':
                feed_ipr_ = feed_ipr_h_
        elif isinstance(stock_material, MaterialSteelMild):
            if drill_len == 'stub':
                feed_ipr_ = feed_ipr_j_
            else:  # elif drill_len == 'jobber':
                feed_ipr_ = feed_ipr_f_
        elif isinstance(stock_material, MaterialSteelMedium):
            if drill_len == 'stub':
                feed_ipr_ = feed_ipr_e_
            else:  # elif drill_len == 'jobber':
                feed_ipr_ = feed_ipr_d_
        elif isinstance(stock_material, MaterialSteelHigh):
            raise ToolIncompatibleMaterial('hss tool vs. tool steel')
        else:
            feed_ipr_ = feed_ipr_h_

        diam_in = [Q_(x, 'inch') for x in diam_in_]
        feed_ipr = [Q_(x, 'inch / turn') for x in feed_ipr_]

        # print(diam_in)
        ipr = None
        if diam < diam_in[0]:
            ipr = feed_ipr[0]
        elif diam >= diam_in[-1]:
            ipr = feed_ipr[-1]
        else:
            if fit:
                import numpy.polynomial.polynomial as poly
                deg = 4
                coef, (residuals, rank, singular_values, rcond) = poly.polyfit(diam_in_, feed_ipr_, deg, full=True)
                # print(coef, residuals[0])
                # Convert to inches, which are the units of the regressed source data. Then select magnitude of
                # measurement, else the calculated values will be in terms of [inch]^rank, the rank of the
                # fitted polynomial. Finally, add units in/turn to calculated ipr value.
                ipr = Q_(poly.polyval(diam.to('inch').magnitude, coef), 'inch / turn')
            else:
                for i in range(len(diam_in) - 1):
                    # print(i, diam_in[i], diam_in[i+1])
                    if diam_in[i] <= diam <= diam_in[i + 1]:
                        x = diam
                        x1, x2 = diam_in[i:i + 2]
                        y1, y2 = feed_ipr[i:i + 2]
                        y = (x - x1) / (x2 - x1) * (y2 - y1) + y1
                        ipr = y
                        break
        return ipr

    def feed_rate(self, stock_material, fit=True):
        return self.feed_rate_(stock_material, 'jobber', fit=fit)

    @classmethod
    def plot_feedrate(cls, stock_material):
        x = np.linspace(0, 2.5, 100) * ureg.inch

        def f(diam, fit):
            d = cls(diam)
            v = d.feed_rate(stock_material, fit)
            return v

        y1 = [f(x_, False).magnitude for x_ in x]
        y2 = [f(x_, True).magnitude for x_ in x]
        pylab.title('Feed rate', fontsize=16.)
        pylab.xlabel('drill size [in]')
        pylab.ylabel('feed rate [in / rev]')
        pylab.xlim(0, 2.5)
        pylab.plot(x, y1, label='linear regression')
        pylab.plot(x, y2, label='polynomial regression')
        pylab.legend()
        pylab.show()

    def thrust(self, stock_material, fit='poly'):
        # Trust numbers from:
        # http://www.drill-hq.com/products/multiple-heads/custom-heads/multiple-spindle-drilling-head-for-different-size-tooling/recommended-tool-speed-chart/

        diam = self.diameter

        diam_in_ = [1 / 16., 1 / 8., 3 / 16., 1 / 4., 5 / 16., 3 / 8., 1 / 2., 5 / 8., 3 / 4., 1, ]
        thrust_lbs_d_ = {'aluminum': [6, 25, 50, 80, 100, 125, 200, 260, 335, 450],
                         'brass': [10, 25, 45, 70, 100, 135, 215, 295, 395, 525],
                         'Cast Iron': [15, 40, 100, 150, 200, 260, 350, 480, 550, 800],
                         'Low Carbon Steel': [30, 80, 145, 230, 340, 440, 700, 1050, 1300, 2000],
                         'Stainless Steel': [40, 100, 180, 290, 425, 465, 780, 1100, 1500, 1900],
                         'Plastic/Wood': [10, 20, 40, 60, 70, 90, 145, 175, 220, 330]}

        thrust_lbs_ = thrust_lbs_d_['aluminum']
        diam_in = [Q_(x, 'inch') for x in diam_in_]
        thrust_lbs = [Q_(x, 'lbs') for x in thrust_lbs_]

        # print(diam_in)
        v = None
        if diam < diam_in[0]:
            v = thrust_lbs[0]
        elif diam >= diam_in[-1]:
            v = thrust_lbs[-1]
        else:
            if fit == 'poly':
                import numpy.polynomial.polynomial as poly
                deg = 4
                coef, (residuals, rank, singular_values, rcond) = poly.polyfit(diam_in_, thrust_lbs_, deg, full=True)
                # print(coef, residuals[0])
                # Convert to inches, which are the units of the regressed source data. Then select magnitude of
                # measurement, else the calculated values will be in terms of [inch]^rank, the rank of the
                # fitted polynomial. Finally, add units in/turn to calculated ipr value.
                v = Q_(poly.polyval(diam.to('inch').magnitude, coef), 'lbs')
            elif fit == 'linear':
                for i in range(len(diam_in) - 1):
                    # print(i, diam_in[i], diam_in[i+1])
                    if diam_in[i] <= diam <= diam_in[i + 1]:
                        x = diam
                        x1, x2 = diam_in[i:i + 2]
                        y1, y2 = thrust_lbs[i:i + 2]
                        y = (x - x1) / (x2 - x1) * (y2 - y1) + y1
                        v = y
                        break
            else:
                raise Exception('fit must be from [fit, linear]')

        return v

    def thrust2(self, stock_material, feed_rate):
        # Thrust equation from:
        # http://media.guhring.com/documents/tech/Formulas/Drilling.pdf

        diam = self.diameter.to('inch')
        f = feed_rate.to('inch / turn')

        # specific cutting force for aluminum
        kc = Q_(800 * 10 ** 6, 'pascal')
        feed_force = .7 * diam / 2. * f * kc
        # Convert from pascal to lbs/in^2
        feed_force = Q_(feed_force.magnitude / 6894.75728, 'lbs')

        return feed_force

    @classmethod
    def plot_thrust(cls, stock_material, highlight=None):
        x = np.linspace(0, 2.5, 100) * ureg.inch

        def f(diam, fit):
            d = cls(diam)
            v = d.thrust(stock_material, fit)
            return v

        def f2(diam):
            d = cls(diam)
            fr = d.feed_rate(stock_material)
            v = d.thrust2(stock_material, fr)
            return v

        y1 = [f(x_, 'linear').m_as('lbs') for x_ in x]
        y2 = [f(x_, 'poly').m_as('lbs') for x_ in x]
        y3 = [f2(x_).m_as('lbs') for x_ in x]
        pylab.title('Feed thrust', fontsize=16.)
        pylab.xlabel('drill size [in]')
        pylab.ylabel('thrust [lbs]')
        pylab.xlim(0, 2.5)
        pylab.plot(x.m_as('inch'), y1, label='linear regression')
        pylab.plot(x.m_as('inch'), y2, label='polynomial regression')
        pylab.plot(x.m_as('inch'), y3, label='calculated estimate')
        if highlight is not None:
            pylab.axhline(y=highlight.to('lbs').magnitude, color='#ff3333ee', label='max thrust')
        pylab.legend()
        pylab.show()


class DrillHSSJobber(DrillHSS):
    def __init__(self, diameter):
        DrillHSS.__init__(self, diameter)
        self.description = 'HSS jobber drill'
        self.drill_style = 'jobber'

    def feed_rate(self, stock_material, fit=True):
        return self.feed_rate_(stock_material, 'jobber', fit=fit)


class DrillHSSStub(DrillHSS):
    def __init__(self, diameter):
        DrillHSS.__init__(self, diameter)
        self.description = 'HSS stub drill'
        self.drill_style = 'stub'

    def feed_rate(self, stock_material, fit=True):
        return self.feed_rate_(stock_material, 'stub', fit=fit)


class Tap(Tool):
    def __init__(self, diameter, tool_material=''):
        Tool.__init__(self, diameter, tool_material)
        self.description = 'Unknown tap'
        if diameter in Drill.letters_and_numbers_and_fractions:
            self.diameter = Q_(Drill.letters_and_numbers_and_fractions[diameter][1], 'mm')
        self.tap_style = 'unknown'

    def feed(self, stock_material):
        pass

    def speed(self, stock_material):
        # https://www.parlec.com/Parlec/media/technical_specs/Tapping-Speeds-Torque-Requirements.pdf?ext=.pdf

        sfm_d = {
            'aluminum': [90 - 110],
            'brass': [80, 100],
            'bronze': [40 - 60],
            'copper': [70 - 90],
            'copper-beryllium': [40 - 50],
            'inconel, hastalloy, waspalloy': [5 - 15],
            'iron-cast': [65 - 75],
            'iron-malleable': [30 - 60],
            'magnesium': [90 - 110],
            'plastics': [60 - 90],
            'steel-cast': [30 - 40],
            'steel-free machining': [50 - 80],
            'steel-chromium': [25 - 40],
            'steel-alloy': [20 - 35],
            'steel-stainless': [15 - 30],
            'titanium': [10 - 25],
            'zinc-die cast': [80 - 120]
        }
        pass

    def torque_(self, stock_material, fit=True):
        # https://www.parlec.com/Parlec/media/technical_specs/Tapping-Speeds-Torque-Requirements.pdf?ext=.pdf

        arr = [
            # Tap Size  Brass   Aluminum and Leaded Brass   200 BHN Steel   300 BHN Steel   400 BHN Steel   Approximate Breaking Torque
            # #6 4 2 7 9 10 8
            [0.13, 4, 2, 7, 9, 10, 8],
            # #8 4.5 2.25 8 10 11 30
            [0.16, 4.5, 2.25, 8, 10, 11, 30],
            # #10 8.5 4.25 15 19 21 42
            [0.19, 8.5, 4.25, 15, 19, 21, 42],
            # 1/4 16 8 28 36 40 106
            [1 / 4., 16, 8, 28, 36, 40, 106],
            # 5/16 24 12 42 54 60 180
            [5 / 16., 24, 12, 42, 54, 60, 180],
            # 3/8 37 18.5065 83 93 240
            [3 / 8., 37, 18.50, 65, 83, 93, 240],
            # 7/16 54 27 94.5 122 135 500
            [7 / 16., 54, 27, 94.5, 122, 135, 500],
            # 1/2 68 34 119 153 170 700
            [1 / 2., 68, 34, 119, 153, 170, 700],
            # 9/16 88 44 154 198 220 850
            [9 / 16., 88, 44, 154, 198, 220, 850],
            # 5/8 119 59.50 208 268 298 1000
            [5 / 8., 119, 59.50, 208, 268, 298, 1000],
            # 3/4 170 85 298 383 425 1500
            [3 / 4., 170, 85, 298, 383, 425, 1500],
            # 7/8 238 119 416 536 595 2100
            [7 / 8., 238, 119, 416, 536, 595, 2100],
            # 1 337 168.50 590 758 842 2700
            [1., 337, 168.50, 590, 758, 842, 2700],
            # 1 1/4 544 277 970 1246 1385 3000+
            [1 + 1 / 4., 544, 277, 970, 1246, 1385, 3000],
            # 1 1/2 850 425 1488 1912 2125 3000+
            [1 + 1 / 2., 850, 425, 1488, 1912, 2125, 3000],
            # 1 3/4 1411 706 2471 3177 3530 3000+
            [1 + 3 / 4., 1411, 706, 2471, 3177, 3530, 3000],
            # 2 1904 952 3332 4284 4760 3000+
            [2., 1904, 952, 3332, 4284, 4760, 3000],
            # 2 1/4 2159 1080 3780 4860 5400 3000+
            [2 + 1 / 4., 2159, 1080, 3780, 4860, 5400, 3000],
            # 2 1/2 2975 1488 5208 6996 7440 3000+
            [2 + 1 / 2., 2975, 1488, 5208, 6996, 7440, 3000]
        ]

        # Are these fine threads?
        # 2 - 8 533 267 933 1199 1333 3000+
        # 2 1/2 - 8 663 332 1160 1492 1658 3000+
        # 3 - 8 1139 570 1995 2565 2850 3000+
        # 4 -  8 1411 706 2471 3177 3530 3000+
        # 5 - 8 1768 884 3094 3978 4420 3000+
        # 6 - 8 2125 1063 3720 4784 5315 3000+

        # All values in table above are in inch/Ibs. Approximate values based on sharp, 4 Flute coarse pitch hand taps at 65% thread height. Dull taps require approximately 50% more torque. For 55% and 75% thread heights, multiply above values by .75 and 1.25 respectively. Torque values for helical flute taps are approximately 70% of those shown. Torque values for chip drive taps are approximately 60% of those shown. Torque values for fine pitch threads are approximately 50% of those show

        diam = self.diameter

        diam_in_ = [x[0] for x in arr]
        torque_ = []
        if isinstance(stock_material, MaterialAluminum):
            torque_ = [x[2] for x in arr]
        elif isinstance(stock_material, MaterialSteelMild):
            torque_ = [x[3] for x in arr]
        elif isinstance(stock_material, MaterialSteelMedium):
            torque_ = [x[4] for x in arr]
        elif isinstance(stock_material, MaterialSteelHigh):
            raise ToolIncompatibleMaterial('hss tool vs. tool steel')
        else:
            raise ToolIncompatibleMaterial('unknown material')

        diam_in = [Q_(x, 'inch') for x in diam_in_]
        torque = [Q_(x, 'inch lbf') for x in torque_]

        # print(diam_in)
        v = None
        if diam < diam_in[0]:
            v = torque[0]
        elif diam >= diam_in[-1]:
            v = torque[-1]
        else:
            if fit:
                import numpy.polynomial.polynomial as poly
                deg = 4
                coef, (residuals, rank, singular_values, rcond) = poly.polyfit(diam_in_, torque_, deg, full=True)
                # print(coef, residuals[0])
                # Convert to inches, which are the units of the regressed source data. Then select magnitude of
                # measurement, else the calculated values will be in terms of [inch]^rank, the rank of the
                # fitted polynomial. Finally, add units in/turn to calculated ipr value.
                v = Q_(poly.polyval(diam.to('inch').magnitude, coef), 'inch lbf')
            else:
                for i in range(len(diam_in) - 1):
                    # print(i, diam_in[i], diam_in[i+1])
                    if diam_in[i] <= diam <= diam_in[i + 1]:
                        x = diam
                        x1, x2 = diam_in[i:i + 2]
                        y1, y2 = torque[i:i + 2]
                        y = (x - x1) / (x2 - x1) * (y2 - y1) + y1
                        v = y
                        break
        return v.to('newton meter')

    def torque(self, stock_material, fit=True):
        return self.torque_(stock_material, fit=fit)

    def sfm(self, stock_material):
        return self.speed(stock_material)

    @classmethod
    def plot_torque(cls, stock_material, highlight=None, min_diam=0, max_diam=2.5, title=None):
        if title is None:
            title = 'Required Torque'

        x = np.linspace(min_diam, max_diam, 100) * ureg.inch

        def f(diam, fit):
            d = cls(diam)
            v = d.torque(stock_material, fit)
            return v

        y1 = [f(x_, False).magnitude for x_ in x]
        y2 = [f(x_, True).magnitude for x_ in x]
        pylab.title(title, fontsize=16.)
        pylab.xlabel('tap size [in]')
        # pylab.ylabel('torque [in lbs]')
        # pylab.ylabel('torque [in lbf]')
        pylab.ylabel('torque [N m]')
        pylab.xlim(min_diam, max_diam)
        pylab.plot(x, y1, label='linear regression')
        pylab.plot(x, y2, label='polynomial regression')
        if highlight is not None:
            if not (isinstance(highlight, list) or isinstance(highlight, tuple)):
                highlight = [highlight]
            for v in highlight:
                v = v.to('newton meter').magnitude
                pylab.axhline(y=v, color='#ff3333ee', label=f'torque = {v:.1f}')
        pylab.yscale('log')
        pylab.ylim(bottom=0)
        pylab.legend()
        pylab.show()
