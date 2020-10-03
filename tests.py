import numpy as np

import pylab

import pymachining as pm

Q_ = pm.getQ()


def test_drill1(stock_material):
    cutter_diameter = Q_(12.7, 'mm')
    drill = pm.DrillHSS(cutter_diameter)

    drill_op = pm.DrillOp(drill, stock_material)

    feed_per_revolution = drill.feed_rate(stock_material)
    sfm = stock_material.sfm()
    spindle_rpm = drill_op.rrpm(sfm)

    P = drill_op.net_power(feed_per_revolution, spindle_rpm)
    print(feed_per_revolution, spindle_rpm, P, sep='\n')


def test_drill2(m, stock_material):
    cutter_diameter = Q_(12.7, 'mm')
    drill = pm.DrillHSS(cutter_diameter)

    drill_op = pm.DrillOp(drill, stock_material)

    feed_per_revolution = drill.feed_rate(stock_material)
    sfm = stock_material.sfm()
    spindle_rpm = drill_op.rrpm(sfm)

    P = drill_op.net_power(feed_per_revolution, spindle_rpm)
    print(feed_per_revolution, spindle_rpm, P, sep='\n')

    m.plot_torque_speed_curve(highlight_power=P, highlight_rpm=spindle_rpm)

    pm.DrillHSS.plot_feedrate(stock_material)
    pm.DrillHSS.plot_thrust(stock_material, highlight=m.max_feed_force)


def test_drill3(m, stock_material):
    do_once = True
    x = []
    y1 = []
    y2 = []
    ax = []
    ay1 = []
    ay2 = []
    ay3 = []
    ay4 = []
    for diam in np.linspace(1 / 64., 1., 100):
        cutter_diameter = Q_(diam, 'inch')

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
        t = drill.thrust(stock_material)

        row = [cutter_diameter, sfm, feed_per_revolution, spindle_rpm_r, spindle_rpm, t_c, t_i, p_c, p_i, P, t]
        if do_once:
            header = '[cutter_diameter, sfm, feed_per_revolution, spindle_rpm_r, spindle_rpm, t_c, t_i, p_c, p_i, P, feed_force]'
            print(header)
            print(' '.join(f'[{x.units}]' for x in row))
            do_once = False
        print(' '.join(f'{x.magnitude:.4f}' for x in row))

        ax += [diam]
        ay1 += [spindle_rpm.magnitude]
        ay2 += [feed_per_revolution.magnitude]
        ay3 += [P.magnitude]
        ay4 += [p_c.magnitude]

    pylab.plot(ax, ay3, label='Requested power')
    pylab.plot(ax, ay4, label='Available power')
    pylab.title('Drilling Power Demands')
    pylab.xlabel('Drill diameter [inch]')
    pylab.ylabel('Power [watt]')
    pylab.legend()
    pylab.show()

    fig, ax1 = pylab.subplots()
    ax1.set_title('Drilling Speeds-Feeds-Power Demands', fontsize=16.)
    ax1.set_xlabel('Drill diameter [inch]', fontsize=12)
    ax1.set_ylabel("Speed [rpm]", fontsize=12)
    ax1.set_xlim([ax[0], ax[-1]])

    ax2 = ax1.twinx()
    ax3 = ax1.twinx()
    ax2.set_ylabel("Feed [ipr]", fontsize=12)
    ax3.set_ylabel("Power [watt]", fontsize=12)

    def make_patch_spines_invisible(ax):
        ax.set_frame_on(True)
        ax.patch.set_visible(False)
        for sp in ax.spines.values():
            sp.set_visible(False)

    ax3.spines["right"].set_position(("axes", 1.2))
    make_patch_spines_invisible(ax3)
    ax3.spines["right"].set_visible(True)

    colors = ['#ff0000ee', '#773300ee', '#00ff00ee', '#005533ee',
              '#555533ee', '#22ff22ee', '#ff5533ee']

    lns = []
    lns += ax1.plot(ax, ay1, color=colors[0], label='Speed')
    lns += ax2.plot(ax, ay2, color=colors[1], label='Feed')
    lns += ax3.plot(ax, ay3, color=colors[2], label='Power requested')
    lns += ax3.plot(ax, ay4, color=colors[3], label='Power available')

    # ax1.yaxis.label.set_color(lns[0][0].get_color())
    # ax2.yaxis.label.set_color(lns[0][0].get_color())
    # ax2.yaxis.label.set_color(lns[0][0].get_color())

    ax1.set_ylim(bottom=0)
    ax2.set_ylim(bottom=0)
    ax3.set_ylim(bottom=0)

    labs = [l.get_label() for l in lns]
    ax1.legend(lns, labs, loc='upper left')

    fig.tight_layout()
    pylab.show()


def test_drilling_range(m, stock_material):
    test_drill1(stock_material)
    test_drill2(m, stock_material)
    test_drill3(m, stock_material)


def test_tap(m, stock_material):
    title = f'Required Tap Torque in {stock_material.name}'
    pm.Tap.plot_torque(stock_material, title=title, highlight=m.torque_range())
    pm.Tap.plot_torque(stock_material, title=title, highlight=m.torque_range(), min_diam=0, max_diam=.75)


def raw_tests():
    m = pm.MachinePM25MV_DMMServo()
    # m = pm.MachinePM25MV_HS()

    m.plot_torque_speed_curve()

    stock_material = pm.Material('aluminum')
    # stock_material = pm.Material('steel-mild')

    test_drilling_range(m, stock_material)
    # test_tap(m, stock_material)


def drill_op(m, material_name, drill_diam, depth):
    stock_material = pm.Material(material_name)
    tool = pm.DrillHSSStub(drill_diam)
    op = pm.DrillOp(tool, stock_material)

    sfm = stock_material.sfm(tool.tool_material)
    material_sfm = sfm

    print('Operation:')
    print('', stock_material)
    print('  SFM:', material_sfm)
    print('', tool)
    print('', op)

    feed_per_revolution = tool.feed_rate(stock_material)
    max_spindle_rpm = m.max_rpm
    requested_spindle_rpm = op.rrpm(sfm)
    spindle_rpm = min(requested_spindle_rpm, max_spindle_rpm)
    spindle_limited = False
    if spindle_rpm < requested_spindle_rpm:
        # SFM is now limited by the spindle RPM
        sfm = (drill_diam * np.pi * spindle_rpm).to('foot * tpm')
        spindle_limited = True
    if spindle_rpm < m.min_rpm:
        spindle_rpm = m.min_rpm
        sfm = (drill_diam * np.pi * spindle_rpm).to('foot * tpm')
        spindle_limited = True
        # May now exceed the material SFM

    P = op.net_power(feed_per_revolution, spindle_rpm).to('watt')
    max_P = m.power_continuous(spindle_rpm).to('watt')
    Q = op.metal_removal_rate(feed_per_revolution, spindle_rpm)
    T = op.torque(P.to('watt'), spindle_rpm)
    max_T = m.torque_intermittent(spindle_rpm)
    torque_limited = False
    if T > max_T:
        torque_limited = True
    thrust1 = tool.thrust(stock_material).to('lbs')
    thrust2 = tool.thrust2(stock_material, feed_per_revolution).to('lbs')
    max_thrust = m.max_feed_force.to('lbs')
    thrust_limited = False
    if thrust1 > max_thrust:
        thrust_limited = True
    op_time = op.machining_time(depth, feed_per_revolution * spindle_rpm).to('min')
    plunge_feedrate = (feed_per_revolution * spindle_rpm).to('inch / minute')
    max_plunge_feedrate = m.max_z_rate
    plunge_limited = False
    if plunge_feedrate > max_plunge_feedrate:
        plunge_limited = True
    def per_warning2(v):
        return ' (!!!)' if t_ > 100 else ''

    def per_warning(v):
        return ' (!!!)' if t_ >= 100 else ' (!!)' if t_ >= 90 else ' (!)' if t_ >= 80 else ''

    print('\nMachining parameters:')
    print(' Supplied to F360:')
    if spindle_limited:
        print(f'  Spindle RPM (limited): {spindle_rpm:.2f}')
    else:
        t_ = (sfm / material_sfm).m_as('') * 100
        print(f'  Surface speed ({t_:.1f}%): {sfm:.2f}')
    print(f'  Feed per revolution: {feed_per_revolution.to("inch / turn"):.4f} {feed_per_revolution.to("mm / turn"):.4f}')
    print(' Calculated by F360:')
    if spindle_limited:
        t_ = (sfm / material_sfm).m_as('') * 100
        print(f'  Surface speed ({t_:.1f}%): {sfm:.2f} (limited by maximum spindle speed)')
    else:
        t_ = (spindle_rpm / max_spindle_rpm).m_as('') * 100
        ts_ = per_warning2(t_)
        print(f'  Spindle RPM{ts_}: {spindle_rpm:.2f} (calculated by f360 using tool diam and sfm)')
    t_ = (plunge_feedrate / max_plunge_feedrate).m_as('') * 100
    ts_ = per_warning(t_)
    print(f'  Plunge feedrate{ts_} ({t_:.1f}%): {plunge_feedrate.to("inch / minute"):.2f} {plunge_feedrate.to("mm / minute"):.2f} (calculated by f360 using feed/rev and spindle rpm)')

    print('\nOperation analysis:')
    t_ = (depth / drill_diam).m_as('')
    print(f' Cycle type:')
    print(f'  D / diam: {t_:.2f}')
    if t_ < 4:
        print()
        print('  Standard drilling may be fine.')
        print('  Peck drilling may still be preferred to break chips.')
        print('  One retraction before final breakthrough may be preferred to allow coolant to hole bottom.')
        # Before the final breakthrough, there is minimal material remaining and the heat carrying capacity
        # of the stock is low.

    print('\n Limited by:')
    if sfm > material_sfm:
        print(f'  Warning: SFM ({sfm:.1f}) exceeds material SFM ({material_sfm:.1f})')
    t_ = False
    if spindle_limited:
        print(f'  Limited by spindle RPM: requested spindle rpm {requested_spindle_rpm:.2f} changed to {spindle_rpm:.2f}')
        t_ = True
    if torque_limited:
        print('  Limited by spindle torque')
        t_ = True
    if thrust_limited:
        print('  Limited by thrust')
        t_ = True
    if plunge_limited:
        print('  Limited by plunge feedrate')
        t_ = True
    if not t_:
        print('  Not limited.')

    print('\n Machine demands:')
    t_ = (thrust1 / max_thrust).m_as('') * 100
    ts_ = per_warning(t_)
    print(f'  Thrust1{ts_}: {t_:.1f}% ({thrust1.to("pound"):.2f} {thrust1.to("kg"):.2f})')
    t_ = (thrust2 / max_thrust).m_as('') * 100
    ts_ = per_warning(t_)
    print(f'  Thrust2{ts_}: {t_:.1f}% ({thrust2.to("pound"):.2f} {thrust2.to("kg"):.2f})')
    if spindle_limited:
        print(f'  Spindle RPM (limited): {spindle_rpm:.2f}')
    else:
        t_ = (spindle_rpm / max_spindle_rpm).m_as('') * 100
        ts_ = per_warning2(t_)
        print(f'  Spindle RPM{ts_}: {spindle_rpm:.2f}')
    t_ = (P / max_P).m_as('') * 100
    ts_ = per_warning(t_)
    print(f'  Power{ts_}: {t_:.1f}% ({P.to("watt"):.2f})')
    t_ = (T / max_T).m_as('') * 100
    ts_ = per_warning(t_)
    print(f'  Torque{ts_}: {t_:.1f}% ({T.to("ft lbf"):.2f} {T.to("N m"):.2f})')

    print('\n Efficiency:')
    print(f'  Material removal rate: {Q.to("in^3 / min"):.2f} {Q.to("cm^3 / min"):.2f}')
    print(f'  Minimal machining time: {op_time:.2f}')

    print('\n')

    # m.plot_torque_speed_curve(highlight_power=P, highlight_rpm=spindle_rpm)
    tool.plot_thrust(stock_material, highlight=m.max_feed_force)


def fusion_tests():
    # m = pm.MachinePM25MV_DMMServo()
    m = pm.MachinePM25MV_HS()

    # What are the Fusion 360 settings for...

    # Drill 1/4" hole into aluminum 1/2" deep:
    # drill_op(m, 'aluminum', Q_(.25, 'inch'), Q_(.5, 'inch'))
    drill_op(m, 'aluminum', Q_(6.7, 'mm'), Q_(.5, 'inch'))
    # drill_op(m, 'aluminum', Q_(.5, 'inch'), Q_(.5, 'inch'))


def main():
    # raw_tests()
    fusion_tests()


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
