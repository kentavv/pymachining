#!/usr/bin/env python3.8

import numpy as np
import pymachining as pm

Q_ = pm.getQ()


def drill_assistant(m, material_name, drill_diam, depth, generate_graphs=False):
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
    print(
        f'  Plunge feedrate{ts_} ({t_:.1f}%): {plunge_feedrate.to("inch / minute"):.2f} {plunge_feedrate.to("mm / minute"):.2f} (calculated by f360 using feed/rev and spindle rpm)')

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

    if generate_graphs:
        m.plot_torque_speed_curve(highlight_power=P, highlight_rpm=spindle_rpm)
        tool.plot_thrust(stock_material, highlight=m.max_feed_force)


def test_assistants():
    # m = pm.MachinePM25MV_DMMServo()
    m = pm.MachinePM25MV_HS()

    # Drill 1/4" hole into aluminum 1/2" deep:
    gen_graphs = True
    # drill_assistant(m, 'aluminum', Q_(.25, 'inch'), Q_(.5, 'inch'), gen_graphs)
    drill_assistant(m, 'aluminum', Q_(6.7, 'mm'), Q_(.5, 'inch'), gen_graphs)
    # drill_assistant(m, 'aluminum', Q_(.5, 'inch'), Q_(.5, 'inch'), gen_graphs)


def main():
    # What are the Fusion 360 settings for...
    print('Content-Type: text/html')
    print()
    test_assistants()


if __name__ == "__main__":
    main()
