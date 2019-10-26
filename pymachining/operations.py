import math

from pymachining.units import *


class MachiningOp:
    def __init__(self, tool, stock_material):
        self.tool = tool
        self.stock_material = stock_material


class DrillOp(MachiningOp):
    # Notes
    # The power required to drill stock is proportional to the metal removal rate (MRR).
    # Other than spindle horsepower, axial thrust may be a limiting factor.
    # Spindle speed is calculated using SFM and the drill diameter. However, only the
    # outer surface of the drill is traveling this fast, and the angular velocity goes to 0
    # at the center of the drill bit.
    # If insufficient power is available, then one can step drill. Again, the power required
    # for each step is proportional to the MRR of each step. A reasonable selection of pilot
    # drill would be one with a slightly larger diameter than the web of the desired drill bit.
    # Might even consider annular cutters for large thru-holes, which will produce the hole
    # by creating a disk instead of a pile of chips. Annular cutters are generally an 1-2" in
    # length and have four flats on their shank. There are R8 and straight shank annular cutter
    # holders, at least one with thru-coolant.
    # Hard to beat a drill bit for metal removal rate, but when not practical, helical milling
    # may be the only option.

    def __init__(self, drill, stock_material):
        MachiningOp.__init__(self, drill, stock_material)
        self.cutter_diameter = drill.diameter

    @staticmethod
    @ureg.check('[length]', 'turn / [time]')
    def cutting_speed_(cutter_diameter, rpm):
        """

        :param cutter_diameter:
        :param rpm:
        :return:

        >>> cutter_diameter = 12.7 * ureg.mm
        >>> rpm = 1000 * ureg.revolutions_per_minute
        >>> v_c = DrillOp.cutting_speed_(cutter_diameter, rpm)
        >>> print(cutter_diameter, rpm, v_c, sep='\\n')
        12.7 millimeter
        1000 revolutions_per_minute
        39898.22670059037 millimeter * revolutions_per_minute
        """
        D_c = cutter_diameter
        n = rpm
        v_c = D_c * math.pi * n

        assert (v_c.check('[length] / [time]'))

        return v_c  # unit / min

    @staticmethod
    @ureg.check('[length]', '[length] / [time]')
    def spindle_speed_(cutter_diameter, cutting_speed):
        """

        :param cutter_diameter:
        :param cutting_speed:
        :return:

        >>> cutter_diameter = 12.7 * ureg.mm
        >>> cutting_speed = 40 * ureg.m / ureg.min
        >>> n = DrillOp.spindle_speed_(cutter_diameter, cutting_speed)
        1002.5508226261124 / minute
        >>> print(n)
        1002.5508226261124 revolutions_per_minute
        >>> print(f'{n:.2f}')
        1002.55 revolutions_per_minute
        """
        D_c = cutter_diameter
        v_c = cutting_speed
        n = v_c / (math.pi * D_c)
        print(n)

        # n.ito('revolutions_per_minute') by itself will divide by 2Pi, but change units to rev_per_min
        # *= ureg.turn only adds the unit
        # *= ureg.turn and n.ito('rev...') will not change value and change units to rev_per_min
        n *= ureg.turn
        n.ito('revolutions_per_minute')
        assert (n.check('turn / [time]'))

        return n  # rpm

    @staticmethod
    @ureg.check('[length] / turn', 'turn / [time]')
    def penetration_rate_(speed_per_revolution, spindle_speed):
        """

        :param speed_per_revolution:
        :param spindle_speed:
        :return:

        # speed_per_revolution = 1 * ureg.mm / ureg.revolution
        # spindle_speed = 1000 * ureg.revolutions_per_minute

        # using turn instead of rev_per_min results in simplier final units, without need for to_base_units()

        >>> speed_per_revolution = 1 * ureg.mm / ureg.turn
        >>> spindle_speed = 1000 * (ureg.turn / ureg.minute)
        >>> v_f = DrillOp.penetration_rate_(speed_per_revolution, spindle_speed)
        >>> print(v_f)
        1000.0 millimeter / minute
        """

        f_n = speed_per_revolution
        n = spindle_speed
        v_f = f_n * n

        assert (v_f.check('[length] / [time]'))

        return v_f  # unit / min

    @staticmethod
    # @ureg.wraps('[length] / turn',            (ureg.mile / ureg.min, ureg.revolutions_per_minute))
    @ureg.check('[length] / [time]', 'revolutions_per_minute')
    def feed_per_revolution_(penetration_rate, spindle_speed):
        """

        :param penetration_rate:
        :param spindle_speed:
        :return:

        >>> penetration_rate = 1000 * ureg.mm / ureg.min
        >>> spindle_speed = 1000 * (ureg.turn / ureg.min)
        >>> f_n = DrillOp.feed_per_revolution_(penetration_rate, spindle_speed)
        >>> print(f_n)
        1.0 millimeter / turn
        """
        v_f = penetration_rate
        n = spindle_speed
        f_n = v_f / n

        # convert from radians to turns
        # the conversion is not necessary if turn/min is used instead of revolutions_per_minute

        #     f_n *= 2 * math.pi / ureg.turn

        # Check return type; Pint can only currently force the return type with @wraps()
        assert (f_n.check('[length] / turn'))

        return f_n  # mm / rev

    @staticmethod
    @ureg.check('[length]', '[length] / turn', '[length] / [time]')
    def metal_removal_rate__(cutter_diameter, feed_per_revolution, cutting_speed):
        """

        :param cutter_diameter:
        :param feed_per_revolution:
        :param cutting_speed:
        :return:

        >>> cutter_diameter = 12.7 * ureg.mm
        >>> feed_per_revolution = 1 * ureg.mm / ureg.turn
        >>> cutting_speed = 1000 * ureg.mm / ureg.min
        >>> Q = DrillOp.metal_removal_rate__(cutter_diameter, feed_per_revolution, cutting_speed)
        3175.0 millimeter ** 3 / minute
        False
        True
        True
        True
        True
        >>> print(Q)
        3175.0 millimeter ** 3 / minute
        >>> print((1 * (ureg.turn / ureg.min)) * (1 * (ureg.mm / ureg.turn)))
        1 millimeter / minute
        """

        D_c = cutter_diameter
        f_n = feed_per_revolution
        v_c = cutting_speed
        # / 4
        Q = D_c * f_n * v_c / 4

        Q *= ureg.turn
        print(Q)
        print(Q.check('[length] ** 2 / [time] / turn'))
        print(Q.check('[length] ** 3 / [time] / turn'))
        print(Q.check('[volume] / [time] / turn'))
        print(Q.check('[length] ** 3 / [time]'))
        print(Q.check('[volume] / [time]'))

        return Q  # cm^3 / min

    @staticmethod
    @ureg.check('[length]', '[length] / turn', 'turn / [time]')
    def metal_removal_rate_(cutter_diameter, feed_per_rev, spindle_rpm):
        """

        :param cutter_diameter:
        :param feed_per_rev:
        :param spindle_rpm:
        :return:

        >>> cutter_diameter = 12.7 * ureg.mm
        >>> feed_per_revolution = 1 * ureg.mm / ureg.turn
        >>> # spindle_speed = 1000 * ureg.revolutions_per_minute
        >>> spindle_speed = 1000 * (ureg.turn / ureg.minute)
        >>> Q = DrillOp.metal_removal_rate_(cutter_diameter, feed_per_revolution, spindle_speed)
        >>> print(Q)
        126676.86977437443 millimeter ** 3 / minute
        >>> print(Q.to('cm^3 / min'))
        126.67686977437442 centimeter ** 3 / minute
        """

        f = feed_per_rev  # [mm / rev]
        N = spindle_rpm  # rev / min
        D_c = cutter_diameter

        f_r = f * N  # feed_rate [mm / min]
        # The /4 comes from r^2 = (d/2)^2
        Q = (math.pi * D_c ** 2 / 4) * f_r

        #     Q *= ureg.turn
        #     print(Q)
        #     print(Q.check('[length] ** 2 / [time] / turn'))
        #     print(Q.check('[length] ** 3 / [time] / turn'))
        #     print(Q.check('[volume] / [time] / turn'))
        #     print(Q.check('[length] ** 3 / [time]'))
        #     print(Q.check('[volume] / [time]'))
        assert (Q.check('[volume] / [time]'))

        return Q  # cm^3 / min

    @staticmethod
    @ureg.check('[length]', '[length] / turn', '[length] / [time]', '[force] / [area]')
    def net_power__(cutter_diameter, feed_per_revolution, cutting_speed, specific_cutting_force):
        """

        :param cutter_diameter:
        :param feed_per_revolution:
        :param cutting_speed:
        :param specific_cutting_force:
        :return:

        >>> cutter_diameter = 12.7 * ureg.mm
        >>> feed_per_revolution = .2 * (ureg.mm / ureg.turn)
        >>> cutting_speed = 75 * (ureg.m / ureg.min)
        >>> cutting_speed = 75 * 1000 * (ureg.mm / ureg.min)
        >>> specific_cutting_force = 350 * (ureg.newton / ureg.mm ** 2)
        >>> # specific_cutting_force.to('kilowatt / cm**3 / min')
        >>> print(specific_cutting_force.to_base_units())
        350000000.0 kilogram / meter / second ** 2
        >>> P = DrillOp.net_power__(cutter_diameter, feed_per_revolution, cutting_speed, specific_cutting_force)
        >>> print(P)
        0.7369205437952863 watt
        """
        D_c = cutter_diameter
        f_n = feed_per_revolution
        v_c = cutting_speed
        k_c = specific_cutting_force
        P_c = (f_n * v_c * D_c * k_c) / (240.)

        assert (P_c.check('watt'))
        P_c.ito('watt')

        return P_c  # kW

    @staticmethod
    @ureg.check('[length]', '[length] / turn', 'turn / [time]', '[power] / ([volume] / [time])')
    def net_power_(cutter_diameter, feed_per_revolution, spindle_rpm, specific_cutting_energy):
        """

        :param cutter_diameter:
        :param feed_per_revolution:
        :param spindle_rpm:
        :param specific_cutting_energy:
        :return:

        >>> cutter_diameter = 12.7 * ureg.mm
        >>> feed_per_revolution = .2 * (ureg.mm / ureg.turn)
        >>> spindle_rpm = 1000 * (ureg.turn / ureg.min)
        >>> # Be careful with expressing units, the way they are written in text may not be the way they should be written in code
        >>> # specific_cutting_energy = .065 * (ureg.kilowatt / ureg.cm**3 / ureg.min)
        >>> # print(specific_cutting_energy)
        >>> specific_cutting_energy = .065 * (ureg.kilowatt / (ureg.cm ** 3 / ureg.min))
        >>> # print(specific_cutting_energy)
        >>> P = DrillOp.net_power_(cutter_diameter, feed_per_revolution, spindle_rpm, specific_cutting_energy)
        >>> print(P)
        1.6467993070668676 kilowatt
        """
        Q = DrillOp.metal_removal_rate_(cutter_diameter, feed_per_revolution, spindle_rpm)
        u_s = specific_cutting_energy

        P = Q * u_s

        assert (P.check('watt'))

        return P

    @staticmethod
    def torque_(net_power, spindle_speed):
        P_c = net_power
        n = spindle_speed
        M_c = (P_c * 30 * 10 ** 3) / (math.pi * n)
        return M_c  # N m

    @staticmethod
    def specific_cutting_force_():
        k_c = 0.
        return k_c  # N / mm^2

    @staticmethod
    def feed_force_():
        F_f = 0.
        return F_f  # N

    @staticmethod
    def machining_time_(I_m, penetration_rate):
        I_m = I_m
        v_f = penetration_rate
        T_c = I_m / v_f
        return T_c  # min

    @ureg.check(None, 'turn / [time]')
    def cutting_speed(self, rpm):
        """

        :param cutter_diameter:
        :param rpm:
        :return:

        >>> cutter_diameter = 12.7 * ureg.mm
        >>> rpm = 1000 * ureg.revolutions_per_minute
        >>> v_c = DrillOp(cutter_diameter, Material('aluminum')).cutting_speed(rpm)
        >>> print(cutter_diameter, rpm, v_c, sep='\\n')
        12.7 millimeter
        1000 revolutions_per_minute
        39898.22670059037 millimeter * revolutions_per_minute
        """
        return self.cutting_speed_(self.cutter_diameter, rpm)

    @ureg.check(None, '[length] / [time]')
    def spindle_speed(self, cutting_speed):
        """

        :param cutter_diameter:
        :param cutting_speed:
        :return:

        >>> cutter_diameter = 12.7 * ureg.mm
        >>> cutting_speed = 40 * ureg.m / ureg.min
        >>> n = DrillOp(cutter_diameter, Material('aluminum')).spindle_speed(cutting_speed)
        1002.5508226261124 / minute
        >>> print(n)
        1002.5508226261124 revolutions_per_minute
        >>> print(f'{n:.2f}')
        1002.55 revolutions_per_minute
        """
        return self.spindle_speed_(self.cutter_diameter, cutting_speed)

    @ureg.check(None, '[length] / [time]', 'revolutions_per_minute')
    def feed_per_revolution(self, penetration_rate, spindle_speed):
        """

        :param penetration_rate:
        :param spindle_speed:
        :return:

        >>> penetration_rate = 1000 * ureg.mm / ureg.min
        >>> spindle_speed = 1000 * (ureg.turn / ureg.min)
        >>> f_n = DrillOp(0 * ureg.mm, Material('aluminum')).feed_per_revolution(penetration_rate, spindle_speed)
        >>> print(f_n)
        1.0 millimeter / turn
        """
        return self.feed_per_revolution_(penetration_rate, spindle_speed)

    # @ureg.wraps('[length] / turn',            (ureg.mile / ureg.min, ureg.revolutions_per_minute))
    @ureg.check(None, '[length] / turn', 'turn / [time]')
    def penetration_rate(self, speed_per_revolution, spindle_speed):
        """

        :param speed_per_revolution:
        :param spindle_speed:
        :return:

        # speed_per_revolution = 1 * ureg.mm / ureg.revolution
        # spindle_speed = 1000 * ureg.revolutions_per_minute

        # using turn instead of rev_per_min results in simplier final units, without need for to_base_units()

        >>> speed_per_revolution = 1 * ureg.mm / ureg.turn
        >>> spindle_speed = 1000 * (ureg.turn / ureg.minute)
        >>> v_f = DrillOp(0 * ureg.mm, Material('aluminum')).penetration_rate(speed_per_revolution, spindle_speed)
        >>> print(v_f)
        1000.0 millimeter / minute
        """

        return self.penetration_rate_(speed_per_revolution, spindle_speed)

    @ureg.check(None, '[length] / turn', '[length] / [time]')
    def metal_removal_rate2(self, feed_per_revolution, cutting_speed):
        """

        :param cutter_diameter:
        :param feed_per_revolution:
        :param cutting_speed:
        :return:

        >>> cutter_diameter = 12.7 * ureg.mm
        >>> feed_per_revolution = 1 * ureg.mm / ureg.turn
        >>> cutting_speed = 1000 * ureg.mm / ureg.min
        >>> Q = DrillOp(cutter_diameter, Material('aluminum')).metal_removal_rate2(feed_per_revolution, cutting_speed)
        3175.0 millimeter ** 3 / minute
        False
        True
        True
        True
        True
        >>> print(Q)
        3175.0 millimeter ** 3 / minute
        """
        return self.metal_removal_rate__(self.cutter_diameter, feed_per_revolution, cutting_speed)

    @ureg.check(None, '[length] / turn', 'turn / [time]')
    def metal_removal_rate(self, feed_per_rev, spindle_rpm):
        """

        :param cutter_diameter:
        :param feed_per_rev:
        :param spindle_rpm:
        :return:

        >>> cutter_diameter = 12.7 * ureg.mm
        >>> feed_per_revolution = 1 * ureg.mm / ureg.turn
        >>> # spindle_speed = 1000 * ureg.revolutions_per_minute
        >>> spindle_speed = 1000 * (ureg.turn / ureg.minute)
        >>> Q = DrillOp(cutter_diameter, Material('aluminum')).metal_removal_rate(feed_per_revolution, spindle_speed)
        >>> print(Q)
        126676.86977437443 millimeter ** 3 / minute
        >>> print(Q.to('cm^3 / min'))
        126.67686977437442 centimeter ** 3 / minute
        """
        return self.metal_removal_rate_(self.cutter_diameter, feed_per_rev, spindle_rpm)

    @ureg.check(None, '[length] / turn', '[length] / [time]', '[force] / [area]')
    def net_power2(self, feed_per_revolution, cutting_speed, specific_cutting_force):
        """

        :param cutter_diameter:
        :param feed_per_revolution:
        :param cutting_speed:
        :param specific_cutting_force:
        :return:

        >>> cutter_diameter = 12.7 * ureg.mm
        >>> feed_per_revolution = .2 * (ureg.mm / ureg.turn)
        >>> cutting_speed = 75 * (ureg.m / ureg.min)
        >>> cutting_speed = 75 * 1000 * (ureg.mm / ureg.min)
        >>> specific_cutting_force = 350 * (ureg.newton / ureg.mm ** 2)
        >>> # specific_cutting_force.to('kilowatt / cm**3 / min')
        >>> print(specific_cutting_force.to_base_units())
        350000000.0 kilogram / meter / second ** 2
        >>> P = DrillOp(cutter_diameter, Material('aluminum')).net_power2(feed_per_revolution, cutting_speed, specific_cutting_force)
        >>> print(P)
        0.7369205437952863 watt
        """
        return self.net_power__(self.cutter_diameter, feed_per_revolution, cutting_speed, specific_cutting_force)

    @ureg.check(None, '[length] / turn', 'turn / [time]')
    def net_power(self, feed_per_revolution, spindle_rpm):
        """

        :param cutter_diameter:
        :param feed_per_revolution:
        :param spindle_rpm:
        :param specific_cutting_energy:
        :return:

        >>> cutter_diameter = 12.7 * ureg.mm
        >>> feed_per_revolution = .2 * (ureg.mm / ureg.turn)
        >>> spindle_rpm = 1000 * (ureg.turn / ureg.min)
        >>> # Be careful with expressing units, the way they are written in text may not be the way they should be written in code
        >>> # specific_cutting_energy = .065 * (ureg.kilowatt / ureg.cm**3 / ureg.min)
        >>> # print(specific_cutting_energy)
        >>> specific_cutting_energy = .065 * (ureg.kilowatt / (ureg.cm ** 3 / ureg.min))
        >>> # print(specific_cutting_energy)
        >>> P = DrillOp(cutter_diameter, Material('aluminum')).net_power(feed_per_revolution, spindle_rpm, specific_cutting_energy)
        >>> print(P)
        1.6467993070668676 kilowatt
        """
        return self.net_power_(self.cutter_diameter, feed_per_revolution, spindle_rpm,
                               self.stock_material.specific_cutting_energy)

    def torque(self, net_power, spindle_speed):
        return self.torque_(net_power, spindle_speed)

    def specific_cutting_force(self):
        return self.specific_cutting_force()

    def feed_force(self):
        return self.feed_force()

    def machining_time(self, I_m, penetration_rate):
        return self.machining_time_(I_m, penetration_rate)

    # ureg = pint.UnitRegistry(auto_reduce_dimensions=True)
    # ​
    # cutter_diameter = 12.7 * ureg.mm
    # cutting_speed = 76 * ureg.m / ureg.min
    # rpm = spindle_speed(cutter_diameter, cutting_speed)
    # print(rpm)
    # print(rpm.to_compact())
    #
    # print(cutter_diameter, rpm, cutting_speed(cutter_diameter, rpm))
    # ​
    # spindle_speed = 1000 / ureg.min
    # speed_per_revolution = 1 * ureg.mm
    # ​
    # print(penetration_rate(speed_per_revolution, spindle_speed))
    # ​
    # 3032265.2292448683
    # millimeter ** 2 / minute
    # 3.032265229244868
    # meter ** 2 / minute
    # ---------------------------------------------------------------------------
    # TypeError
    # Traceback(most
    # recent
    # call
    # last)
    # < ipython - input - 11 - 7
    # f9068dfe98a > in < module >
    # 80
    # print(rpm.to_compact())
    # 81
    # ---> 82
    # print(cutter_diameter, rpm, cutting_speed(cutter_diameter, rpm))
    # 83
    # 84
    # spindle_speed = 1000 / ureg.min
    #
    # TypeError: 'Quantity'
    # object is not callable
    #
    # print((1 * (ureg.turn / ureg.min)) * (1 * (ureg.mm / ureg.turn)))
    # 1 millimeter / minute

    @staticmethod
    @ureg.check('[length]', 'turn / [time]')
    def speed_(cutter_diameter, rpm):
        v = cutter_diameter * rpm * math.pi
        assert (v.check('[length] / [time]'))
        return v

    @ureg.check(None, 'turn / [time]')
    def speed(self, rpm):
        return self.speed_(self.cutter_diameter, rpm)

    @staticmethod
    @ureg.check('[length]', 'turn / [time]')
    def sfm_(cutter_diameter, rpm):
        v = DrillOp.speed_(cutter_diameter, rpm)
        assert (v.check('[length] / [time]'))
        v.ito('feet * turn / minute')
        return v

    @ureg.check(None, 'turn / [time]')
    def sfm(self, rpm):
        return self.sfm_(self.cutter_diameter, rpm)

    @staticmethod
    @ureg.check('[length]', '[length] * turn / [time]')
    def rrpm_(cutter_diameter, speed):
        rpm = speed / (cutter_diameter * math.pi)
        assert (rpm.check('turn / [time]'))
        return rpm

    @ureg.check(None, '[length] * turn / [time]')
    def rrpm(self, speed):
        return self.rrpm_(self.cutter_diameter, speed)
