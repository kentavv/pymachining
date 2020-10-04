#!/usr/bin/env python

import sys
import urllib.parse
import io
import cgi
import numpy as np
import pymachining as pm

Q_ = pm.getQ()


def drill_assistant_header():
    print('''
  <form action="/pymachining/assistant_cgi.py" method="post">
    <label for="machine">Machine:</label>
    <select id="machine" name="machine">
      <option value="PM25MV">PM25MV</option>
      <option value="PM25MV_DMMServo">PM25MV DMMServo</option>
      <option value="PM25MV_HS">PM25MV HS</option>
    </select>
    <br>

    <label for="operation">Operation:</label>
    <select id="operation" name="operation">
      <option value="drilling">Drilling</option>
    </select>
    <br>


    <label for="stock_mat">Stock material:</label>
    <select id="stock_mat" name="stock_mat">
      <option value="aluminum">Aluminum</option>
      <option value="6061">Aluminum - 6061</option>
      <option value="steel">Steel</option>
      <option value="steel-mild">Steel mild</option>
      <option value="12l14">12L14</option>
      <option value="steel-medium">Steel medium</option>
      <option value="steel-high">Steel high</option>
    </select>
    <br>

    <label for="tool_mat">Tool material:</label>
    <select id="tool_mat" name="tool_mat">
      <option value="hss">HSS</option>
      <option value="carbide">Carbide</option>
    </select>
    <br>

    <label for="input_units">Input units:</label>
    <select id="input_units" name="input_units">
      <option value="metric">Metric</option>
      <option value="imperial">Imperial</option>
    </select>
    <br>

    <label for="output_units">Output units:</label>
    <select id="output_units" name="output_units">
      <option value="metric">Metric</option>
      <option value="imperial">Imperial</option>
    </select>
    <br>

    <label for="drill_diam">Drill diam:</label>
    <input type="text" id="drill_diam" name="drill_diam" value="0.25">
    <br>

    <label for="hole_depth">Hole depth:</label>
    <input type="text" id="hole_depth" name="hole_depth" value="0.5">
    <br>

    <input type="submit" value="Submit">
  </form>
''')


def drill_assistant(m, material_name, drill_diam, depth, output_units, generate_graphs=False):
    stock_material = pm.Material(material_name)
    tool = pm.DrillHSSStub(drill_diam)
    op = pm.DrillOp(tool, stock_material)

    sfm = stock_material.sfm(tool.tool_material)
    material_sfm = sfm

    print('<h1>Drilling operation</h1>')
    print(stock_material)
    print('  SFM:', material_sfm, '<br>')
    print(tool)
    print(op)

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

    print('<h2>Machining parameters</h2>')
    print(' Supplied to F360<br>')
    if spindle_limited:
        print(f'  Spindle RPM (limited): {spindle_rpm:.2f}<br>')
    else:
        t_ = (sfm / material_sfm).m_as('') * 100
        print(f'  Surface speed ({t_:.1f}%): {sfm:.2f}<br>')
    print(f'  Feed per revolution: {feed_per_revolution.to("inch / turn"):.4f} {feed_per_revolution.to("mm / turn"):.4f}<br>')
    print(' Calculated by F360:<br>')
    if spindle_limited:
        t_ = (sfm / material_sfm).m_as('') * 100
        print(f'  Surface speed ({t_:.1f}%): {sfm:.2f} (limited by maximum spindle speed)<br>')
    else:
        t_ = (spindle_rpm / max_spindle_rpm).m_as('') * 100
        ts_ = per_warning2(t_)
        print(f'  Spindle RPM{ts_}: {spindle_rpm:.2f} (calculated by f360 using tool diam and sfm)<br>')
    t_ = (plunge_feedrate / max_plunge_feedrate).m_as('') * 100
    ts_ = per_warning(t_)
    print(
        f'  Plunge feedrate{ts_} ({t_:.1f}%): {plunge_feedrate.to("inch / minute"):.2f} {plunge_feedrate.to("mm / minute"):.2f} (calculated by f360 using feed/rev and spindle rpm)<br>')

    print('<h2>Operation analysis</h2>')
    t_ = (depth / drill_diam).m_as('')
    print(f' Cycle type:<br>')
    print(f'  D / diam: {t_:.2f}<br>')
    if t_ < 4:
        print()
        print('  Standard drilling may be fine.<br>')
        print('  Peck drilling may still be preferred to break chips.<br>')
        print('  One retraction before final breakthrough may be preferred to allow coolant to hole bottom.<br>')
        # Before the final breakthrough, there is minimal material remaining and the heat carrying capacity
        # of the stock is low.

    print('\n Limited by:<br>')
    if sfm > material_sfm:
        print(f'  Warning: SFM ({sfm:.1f}) exceeds material SFM ({material_sfm:.1f})<br>')
    t_ = False
    if spindle_limited:
        print(f'  Limited by spindle RPM: requested spindle rpm {requested_spindle_rpm:.2f} changed to {spindle_rpm:.2f}<br>')
        t_ = True
    if torque_limited:
        print('  Limited by spindle torque<br>')
        t_ = True
    if thrust_limited:
        print('  Limited by thrust<br>')
        t_ = True
    if plunge_limited:
        print('  Limited by plunge feedrate<br>')
        t_ = True
    if not t_:
        print('  Not limited.<br>')

    print('<h2>Machine demands</h2>')
    t_ = (thrust1 / max_thrust).m_as('') * 100
    ts_ = per_warning(t_)
    print(f'  Thrust1{ts_}: {t_:.1f}% ({thrust1.to("pound"):.2f} {thrust1.to("kg"):.2f})<br>')
    t_ = (thrust2 / max_thrust).m_as('') * 100
    ts_ = per_warning(t_)
    print(f'  Thrust2{ts_}: {t_:.1f}% ({thrust2.to("pound"):.2f} {thrust2.to("kg"):.2f})<br>')
    if spindle_limited:
        print(f'  Spindle RPM (limited): {spindle_rpm:.2f}<br>')
    else:
        t_ = (spindle_rpm / max_spindle_rpm).m_as('') * 100
        ts_ = per_warning2(t_)
        print(f'  Spindle RPM{ts_}: {spindle_rpm:.2f}<br>')
    t_ = (P / max_P).m_as('') * 100
    ts_ = per_warning(t_)
    print(f'  Power{ts_}: {t_:.1f}% ({P.to("watt"):.2f})<br>')
    t_ = (T / max_T).m_as('') * 100
    ts_ = per_warning(t_)
    print(f'  Torque{ts_}: {t_:.1f}% ({T.to("ft lbf"):.2f} {T.to("N m"):.2f})<br>')

    print('\n Efficiency:<br>')
    print(f'  Material removal rate: {Q.to("in^3 / min"):.2f} {Q.to("cm^3 / min"):.2f}<br>')
    print(f'  Minimal machining time: {op_time:.2f}<br>')

    if generate_graphs:
        m.plot_torque_speed_curve(highlight_power=P, highlight_rpm=spindle_rpm)
        tool.plot_thrust(stock_material, highlight=m.max_feed_force)


def main(env, form):
    print('Content-Type: text/html\n')

    # What are the Fusion 360 settings for...

    machine = env['machine'] if 'machine' in env else None
    operation = env['operation'] if 'operation' in env else None
    stock_mat = env['stock_mat'] if 'stock_mat' in env else None
    tool_mat = env['tool_mat'] if 'tool_mat' in env else None
    input_units = env['input_units'] if 'input_units' in env else None
    output_units = env['output_units'] if 'output_units' in env else None

    drill_diam = env['drill_diam'] if 'drill_diam' in env else None
    hole_depth = env['hole_depth'] if 'hole_depth' in env else None

    if machine not in ['PM25MV', 'PM25MV_DMMServo', 'PM25MV_HS']:
        machine = None

    if operation not in ['drilling']:
        operation = None

    if stock_mat not in ['aluminum', '6061', 'steel', 'steel-mild', '12l14', 'steel-medium', 'steel-high']:
        stock_mat = None

    if tool_mat not in ['carbide', 'hss']:
        tool_mat = None

    if input_units not in ['metric', 'imperial']:
        input_units = None

    if output_units not in ['metric', 'imperial']:
        output_units = None

    try:
        drill_diam = float(drill_diam)
    except (TypeError, ValueError):
        drill_diam = None

    try:
        hole_depth = float(hole_depth)
    except (TypeError, ValueError):
        hole_depth = None

    if machine is not None and stock_mat is not None and tool_mat is not None and input_units is not None and output_units is not None and operation is not None and drill_diam is not None and hole_depth is not None:
        print('<html>')
        drill_assistant_header()

        if machine == 'PM25MV':
            m = pm.MachinePM25MV()
        elif machine == 'PM25MV_DMMServo':
            m = pm.MachinePM25MV_DMMServo()
        elif machine == 'PM25MV_HS':
            m = pm.MachinePM25MV_HS()
        else:
            m = None
        if input_units == 'metric':
            tool = Q_(drill_diam, 'mm')
        else:
            tool = Q_(drill_diam, 'inch')
        if output_units == 'metric':
            depth = Q_(hole_depth, 'mm')
        else:
            depth = Q_(hole_depth, 'inch')
        gen_graphs = False
        drill_assistant(m, stock_mat, tool, depth, output_units, gen_graphs)
        print('</html>')
    else:
        print('<html>')
        drill_assistant_header()
        print('</html>')


def application(environ, start_response):
    status = '200 OK'

    saved_stdout = sys.stdout

    sys.stdout = io.StringIO()

    d = urllib.parse.parse_qs(environ['QUERY_STRING'])
    env = {k: v[0].strip() for k, v in d.items()}

    request_body = environ['wsgi.input'].read()
    d = urllib.parse.parse_qs(request_body)
    form = {k.decode('utf-8'): v[0].decode('utf-8').strip() for k, v in d.items()}

    main(env, form)
    html = sys.stdout.getvalue()

    sys.stdout = saved_stdout

    response_header = [('Content-type', 'text/html')]
    start_response(status, response_header)

    return [html.encode('utf-8')]


if __name__ == "__main__":
    if False:
        env = {'machine': 'PM25MV_DMMServo',
               'stock_mat': 'aluminum',
               'tool_mat': 'hss',
               'input_units': 'metric',
               'output_units': 'imperial'}
        form = {}
    elif 0:
        d = urllib.parse.parse_qs(environ['QUERY_STRING'])
        env = {k: v[0].strip() for k, v in d.items()}

        request_body = environ['wsgi.input'].read()
        d = urllib.parse.parse_qs(request_body)
        form = {k.decode('utf-8'): v[0].decode('utf-8').strip() for k, v in d.items()}
    else:
        form = cgi.FieldStorage()
        env = { 'machine': form.getvalue('machine'),
                'operation': form.getvalue('operation'),
                'stock_mat': form.getvalue('stock_mat'),
                'tool_mat': form.getvalue('tool_mat'),
                'input_units': form.getvalue('input_units'),
                'output_units': form.getvalue('output_units'),

                'drill_diam': form.getvalue('drill_diam'),
                'hole_depth': form.getvalue('hole_depth')}

        #form = {}

    main(env, form)
