import pint
import math

ureg = pint.UnitRegistry(auto_reduce_dimensions=True)


@ureg.check('[length]', 'turn / [time]')
def cutting_speed(cutter_diameter, rpm):
    """

    :param cutter_diameter:
    :param rpm:
    :return:

    >>> cutter_diameter = 12.7 * ureg.mm
    >>> rpm = 1000 * ureg.revolutions_per_minute
​
    >>> v_c = cutting_speed(cutter_diameter, rpm)
​
    >>> print(cutter_diameter, rpm, v_c, sep='\n')
    12.7 millimeter
    1000 revolutions_per_minute
    39898.22670059037 millimeter * revolutions_per_minute
    """
    D_c = cutter_diameter
    n = rpm
    v_c = D_c * math.pi * n

    assert (v_c.check('[length] / [time]'))

    return v_c  # unit / min


@ureg.check('[length]', '[length] / [time]')
def spindle_speed(cutter_diameter, cutting_speed):
    """

    :param cutter_diameter:
    :param cutting_speed:
    :return:

    >>> cutter_diameter = 12.7 * ureg.mm
    >>> cutting_speed = 40 * ureg.m / ureg.min
​
    >>> n = spindle_speed(cutter_diameter, cutting_speed)
    1002.5508226261124 / minute
    >>> print(n)
    1002.5508226261124  revolutions_per_minute
    >>>> print(f'{n:.2f}')
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


@ureg.check('[length] / turn', 'turn / [time]')
def penetration_rate(speed_per_revolution, spindle_speed):
    """

    :param speed_per_revolution:
    :param spindle_speed:
    :return:

    # speed_per_revolution = 1 * ureg.mm / ureg.revolution
    # spindle_speed = 1000 * ureg.revolutions_per_minute

    # using turn instead of rev_per_min results in simplier final units, without need for to_base_units()

    >>> speed_per_revolution = 1 * ureg.mm / ureg.turn
    >>> spindle_speed = 1000 * (ureg.turn / ureg.minute)
​
    >>> v_f = penetration_rate(speed_per_revolution, spindle_speed)
​
    >>> print(v_f)
    1000.0 millimeter / minute
    """

    f_n = speed_per_revolution
    n = spindle_speed
    v_f = f_n * n

    assert (v_f.check('[length] / [time]'))

    return v_f  # unit / min


# @ureg.wraps('[length] / turn',            (ureg.mile / ureg.min, ureg.revolutions_per_minute))
@ureg.check('[length] / [time]', 'revolutions_per_minute')
def feed_per_revolution(penetration_rate, spindle_speed):
    """

    :param penetration_rate:
    :param spindle_speed:
    :return:

    >>> penetration_rate = 1000 * ureg.mm / ureg.min
    >>> spindle_speed = 1000 * (ureg.turn / ureg.min)
​
    >>> f_n = feed_per_revolution(penetration_rate, spindle_speed)
​
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


@ureg.check('[length]', '[length] / turn', '[length] / [time]')
def metal_removal_rate_(cutter_diameter, feed_per_revolution, cutting_speed):
    """

    :param cutter_diameter:
    :param feed_per_revolution:
    :param cutting_speed:
    :return:

    >>> cutter_diameter = 12.7 * ureg.mm
    >>> feed_per_revolution = 1 * ureg.mm / ureg.turn
    >>> cutting_speed = 1000 * ureg.mm / ureg.min
​
    >>> Q = metal_removal_rate(cutter_diameter, feed_per_revolution, cutting_speed)
    3175.0 millimeter ** 3 / minute
    False
    True
    True
    True
    True
    >>> print(Q)
    3175.0 millimeter ** 3 / minute
    print((1 * (ureg.turn / ureg.min)) * (1 * (ureg.mm / ureg.turn)))
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


@ureg.check('[length]', '[length] / turn', 'turn / [time]')
def metal_removal_rate(cutter_diameter, feed_per_rev, spindle_rpm):
    """

    :param cutter_diameter:
    :param feed_per_rev:
    :param spindle_rpm:
    :return:

    >>> cutter_diameter = 12.7 * ureg.mm
    >>> feed_per_revolution = 1 * ureg.mm / ureg.turn
    # spindle_speed = 1000 * ureg.revolutions_per_minute
    >>> spindle_speed = 1000 * (ureg.turn / ureg.minute)
​
    >>> Q = metal_removal_rate(cutter_diameter, feed_per_revolution, spindle_speed)
​
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


@ureg.check('[length]', '[length] / turn', '[length] / [time]', '[force] / [area]')
def net_power_(cutter_diameter, feed_per_revolution, cutting_speed, specific_cutting_force):
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
    # specific_cutting_force.to('kilowatt / cm**3 / min')
​
    >>> print(specific_cutting_force.to_base_units())
    350000000.0 kilogram / meter / second ** 2
    # P = net_power(cutter_diameter, feed_per_revolution, cutting_speed, specific_cutting_force)
​
    # print(P)
    """
    D_c = cutter_diameter
    f_n = feed_per_revolution
    v_c = cutting_speed
    k_c = specific_cutting_force
    P_c = (f_n * v_c * D_c * k_c) / (240.)

    assert (P_c.check('watt'))
    P_c.ito('watt')

    return P_c  # kW


@ureg.check('[length]', '[length] / turn', 'turn / [time]', '[power] / ([volume] / [time])')
def net_power(cutter_diameter, feed_per_revolution, spindle_rpm, specific_cutting_energy):
    """

    :param cutter_diameter:
    :param feed_per_revolution:
    :param spindle_rpm:
    :param specific_cutting_energy:
    :return:

    >>> cutter_diameter = 12.7 * ureg.mm
    >>> feed_per_revolution = .2 * (ureg.mm / ureg.turn)
    >>> spindle_rpm = 1000 * (ureg.turn / ureg.min)
​
# Be careful with expressing units, the way they are written in text may not be the way they should be written in code
# specific_cutting_energy = .065 * (ureg.kilowatt / ureg.cm**3 / ureg.min)
# print(specific_cutting_energy)
    >>> specific_cutting_energy = .065 * (ureg.kilowatt / (ureg.cm ** 3 / ureg.min))
# print(specific_cutting_energy)
​
    >>> P = net_power(cutter_diameter, feed_per_revolution, spindle_rpm, specific_cutting_energy)
    >>> print(P)
    1.6467993070668676 kilowatt
    """
    Q = metal_removal_rate(cutter_diameter, feed_per_revolution, spindle_rpm)
    u_s = specific_cutting_energy

    P = Q * u_s

    assert (P.check('watt'))

    return P


def torque(net_power, spindle_speed):
    P_c = net_power
    n = spindle_speed
    M_c = (P_c * 30 * 10 ** 3) / (math.pi * n)
    return M_c  # N m


def specific_cutting_force():
    k_c = 0.
    return k_c  # N / mm^2


def feed_force():
    F_f = 0.
    return F_f  # N


def machining_time(I_m, penetration_rate):
    I_m = I_m
    v_f = penetration_rate
    T_c = I_m / v_f
    return T_c  # min


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
