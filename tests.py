import numpy as np

import pymachining as pm
from pymachining import ureg


def test_drilling_range():
    stock_material = pm.Material('aluminum')
    pm.DrillHSS.plot_feedrate(stock_material)
    pm.DrillHSS.plot_thrust(stock_material)

    cutter_diameter = 12.7 * ureg.mm
    drill = pm.DrillHSS(cutter_diameter)

    drill_op = pm.DrillOp(drill, stock_material)

    feed_per_revolution = drill.feed_rate(stock_material)
    sfm = stock_material.sfm()
    spindle_rpm = drill_op.rrpm(sfm)

    P = drill_op.net_power(feed_per_revolution, spindle_rpm)
    print(feed_per_revolution, spindle_rpm, P, sep='\n')

    m = pm.MachinePM25MV_DMMServo()
    m.plot_torque_speed_curve(highlight_power=P, highlight_rpm=spindle_rpm)

    do_once = True
    for diam in np.linspace(1 / 64., .5, 50):
        cutter_diameter = diam * ureg.inch

        drill = pm.DrillHSS(cutter_diameter)
        drill_op = pm.DrillOp(drill, stock_material)

        sfm = stock_material.sfm() * 1
        feed_per_revolution = drill.feed_rate(stock_material)
        spindle_rpm_r = drill_op.rrpm(sfm)

        spindle_rpm, _ = m.clamp_speed(spindle_rpm_r)

        t_c = m.torque_continuous(spindle_rpm)
        t_i = m.torque_intermittent(spindle_rpm)
        p_c = m.power_continuous(spindle_rpm).to('watt')
        p_i = m.power_intermittent(spindle_rpm).to('watt')
        P = drill_op.net_power(feed_per_revolution, spindle_rpm).to('watt')

        row = [cutter_diameter, sfm, feed_per_revolution, spindle_rpm_r, spindle_rpm, t_c, t_i, p_c, p_i, P]
        if do_once:
            print('[cutter_diameter, sfm, feed_per_revolution, spindle_rpm_r, spindle_rpm, t_c, t_i, p_c, p_i, P]')
            print(' '.join(f'[{x.units}]' for x in row))
            do_once = False
        print(' '.join(f'{x.magnitude:.4f}' for x in row))


def main():
    test_drilling_range()


if __name__ == "__main__":
    main()


def old_stuff():
    feed_per_revolution = .2 * (ureg.mm / ureg.turn)
    spindle_rpm = 1000 * ureg.tpm

    P = drill_op.net_power(feed_per_revolution, spindle_rpm)

    print(P)

    # Each stock material will have a recommended cutting rate (sfm).
    # Each tool will have a recommended feed rate (ipr) determined by its diameter and cut stock material.
    # Given a tool,

    exit(1)

    # %%
    v_c = pm.DrillOp.cutting_speed_(cutter_diameter, rpm)

    print(cutter_diameter, rpm, v_c, sep='\n')

    print(pm.DrillOp.speed_(cutter_diameter, rpm))
    print(pm.DrillOp.sfm_(cutter_diameter, rpm))

    # %%

    # %%

    rpm = 1000 * ureg.tpm

    v_c = drill_op.cutting_speed(rpm)

    print(cutter_diameter, rpm, v_c, sep='\n')

    print(drill_op.speed(rpm))
    print(drill_op.sfm(rpm))
    print(drill_op.rrpm(drill_op.speed(rpm)))
    print(drill_op.rrpm(drill_op.sfm(rpm)))
    print(drill_op.rrpm(stock_material.sfm()))

    # %%

    cutter_diameter = 12.7 * ureg.mm
    cutting_speed = 40 * ureg.m / ureg.min

    n = pm.DrillOp.spindle_speed_(cutter_diameter, cutting_speed)
    print(n)
    print(f'{n:.2f}')

    # %%

    cutting_speed = 40 * ureg.m / ureg.min

    n = drill_op.spindle_speed(cutting_speed)
    print(n)
    print(f'{n:.2f}')

    # %%

    # speed_per_revolution = 1 * ureg.mm / ureg.revolution
    # spindle_speed = 1000 * ureg.revolutions_per_minute

    # using turn instead of rev_per_min results in simplier final units, without need for to_base_units()
    speed_per_revolution = 1 * ureg.mm / ureg.turn
    spindle_speed = 1000 * (ureg.turn / ureg.minute)

    v_f = pm.DrillOp.penetration_rate_(speed_per_revolution, spindle_speed)

    print(v_f)
    # print(v_f.to_compact())
    # print(v_f.to_base_units())
    # print(v_f.to_reduced_units())
    # print(v_f.to(ureg.mm / ureg.min))

    # %%

    # speed_per_revolution = 1 * ureg.mm / ureg.revolution
    # spindle_speed = 1000 * ureg.revolutions_per_minute

    # using turn instead of rev_per_min results in simplier final units, without need for to_base_units()
    speed_per_revolution = 1 * ureg.mm / ureg.turn
    spindle_speed = 1000 * (ureg.turn / ureg.minute)

    v_f = drill_op.penetration_rate_(speed_per_revolution, spindle_speed)

    print(v_f)
    # print(v_f.to_compact())
    # print(v_f.to_base_units())
    # print(v_f.to_reduced_units())
    # print(v_f.to(ureg.mm / ureg.min))

    # %%

    penetration_rate = 1000 * ureg.mm / ureg.min
    spindle_speed = 1000 * (ureg.turn / ureg.min)

    f_n = pm.DrillOp.feed_per_revolution_(penetration_rate, spindle_speed)

    print(f_n)

    # %%

    penetration_rate = 1000 * ureg.mm / ureg.min
    spindle_speed = 1000 * (ureg.turn / ureg.min)

    f_n = drill_op.feed_per_revolution(penetration_rate, spindle_speed)

    print(f_n)

    # %%

    cutter_diameter = 12.7 * ureg.mm
    feed_per_revolution = 1 * ureg.mm / ureg.turn
    # spindle_speed = 1000 * ureg.revolutions_per_minute
    cutting_speed = 1000 * ureg.mm / ureg.min

    Q = pm.DrillOp.metal_removal_rate_(cutter_diameter, feed_per_revolution, spindle_speed)

    print(Q)
    print(Q.to('cm^3 / min'))

    # %%

    feed_per_revolution = 1 * ureg.mm / ureg.turn
    # spindle_speed = 1000 * ureg.revolutions_per_minute
    cutting_speed = 1000 * ureg.mm / ureg.min

    Q = drill_op.metal_removal_rate(feed_per_revolution, spindle_speed)

    print(Q)
    print(Q.to('cm^3 / min'))

    # %%

    cutter_diameter = 12.7 * ureg.mm
    feed_per_revolution = 1 * ureg.mm / ureg.turn
    # spindle_speed = 1000 * ureg.revolutions_per_minute
    spindle_speed = 1000 * (ureg.turn / ureg.minute)

    Q = pm.DrillOp.metal_removal_rate_(cutter_diameter, feed_per_revolution, spindle_speed)

    print(Q)
    print(Q.to('cm^3 / min'))

    # %%

    cutter_diameter = 12.7 * ureg.mm
    feed_per_revolution = 1 * ureg.mm / ureg.turn
    # spindle_speed = 1000 * ureg.revolutions_per_minute
    spindle_speed = 1000 * (ureg.turn / ureg.minute)

    Q = drill_op.metal_removal_rate(feed_per_revolution, spindle_speed)

    print(Q)
    print(Q.to('cm^3 / min'))

    # %%

    cutter_diameter = 12.7 * ureg.mm
    feed_per_revolution = .2 * (ureg.mm / ureg.turn)
    cutting_speed = 75 * (ureg.m / ureg.min)
    cutting_speed = 75 * 1000 * (ureg.mm / ureg.min)
    specific_cutting_force = 350 * (ureg.newton / ureg.mm ** 2)
    # specific_cutting_force.to('kilowatt / cm**3 / min')

    print(specific_cutting_force.to_base_units())
    P = pm.DrillOp.net_power__(cutter_diameter, feed_per_revolution, cutting_speed, specific_cutting_force)

    # print(P)

    # %%

    cutter_diameter = 12.7 * ureg.mm
    feed_per_revolution = .2 * (ureg.mm / ureg.turn)
    cutting_speed = 75 * (ureg.m / ureg.min)
    cutting_speed = 75 * 1000 * (ureg.mm / ureg.min)
    specific_cutting_force = 350 * (ureg.newton / ureg.mm ** 2)
    # specific_cutting_force.to('kilowatt / cm**3 / min')

    print(specific_cutting_force.to_base_units())
    P = drill_op.net_power2(feed_per_revolution, cutting_speed, specific_cutting_force)

    # print(P)

    # %%

    cutter_diameter = 12.7 * ureg.mm
    feed_per_revolution = .2 * (ureg.mm / ureg.turn)
    feed_per_revolution = .01 * .75 * (ureg.inch / ureg.turn)
    spindle_rpm = 1000 * (ureg.turn / ureg.min)

    # Be careful with expressing units, the way they are written in text may not be the way they should be written in code
    # specific_cutting_energy = .065 * (ureg.kilowatt / ureg.cm**3 / ureg.min)
    # print(specific_cutting_energy)
    specific_cutting_energy = .065 * (ureg.kilowatt / (ureg.cm ** 3 / ureg.min))
    # print(specific_cutting_energy)

    P = pm.DrillOp.net_power_(cutter_diameter, feed_per_revolution, spindle_rpm, specific_cutting_energy)

    print(P)

    # %%

    cutter_diameter = 12.7 * ureg.mm
    feed_per_revolution = .2 * (ureg.mm / ureg.turn)
    spindle_rpm = 1000 * (ureg.turn / ureg.min)

    # Be careful with expressing units, the way they are written in text may not be the way they should be written in code
    # specific_cutting_energy = .065 * (ureg.kilowatt / ureg.cm**3 / ureg.min)
    # print(specific_cutting_energy)
    specific_cutting_energy = .065 * (ureg.kilowatt / (ureg.cm ** 3 / ureg.min))
    # print(specific_cutting_energy)

    P = drill_op.net_power(feed_per_revolution, spindle_rpm, specific_cutting_energy)

    print(P)