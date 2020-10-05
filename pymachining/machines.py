from .base import *
from .units import *
import math
import pylab
import numpy as np


class MachineType(PyMachiningBase):
    def __init__(self):
        PyMachiningBase.__init__(self)
        self.max_rpm = float('inf')
        self.min_rpm = float('inf')
        self.gear_ratio = 1.
        self.name = 'Unknown'
        self.description = 'Unknown'
        self.torque_intermittent_define = False
        self.idle_power = Q_(0., 'watt')  # tare power
        self.efficiency = 1.
        self.max_feed_force = Q_(0, 'lbs')

    def set_gear_ratio(self, gear_ratio):
        self.gear_ratio = gear_ratio

    def _torque_continuous(self, rpm):
        return float('inf')

    def _torque_intermittent(self, rpm):
        return float('inf')

    def torque_continuous(self, rpm):
        if not isinstance(rpm, ureg.Quantity) or rpm.dimensionless:
            rpm *= ureg.tpm

        abs_rpm = abs(rpm)

        T = self._torque_continuous(abs_rpm)
        # T = math.copysign(T, rpm)
        if rpm < 0:
            T *= -1

        # T *= self.gear_ratio
        return T

    def torque_intermittent(self, rpm):
        if not isinstance(rpm, ureg.Quantity) or rpm.dimensionless:
            rpm *= ureg.tpm

        abs_rpm = abs(rpm)

        T = self._torque_intermittent(abs_rpm)
        # T = math.copysign(T, rpm)
        if rpm < 0:
            T *= -1

        # T *= self.gear_ratio
        return T

    # In the power methods, if not using Pint.to('watt'), the return value must be converted by dividing by 9.5488
    # Power (W) = Torque (N.m) x Speed (RPM) / 9.5488

    def power_continuous(self, rpm):
        if not isinstance(rpm, ureg.Quantity) or rpm.dimensionless:
            rpm *= ureg.tpm

        t = self.torque_continuous(rpm)
        # return t * rpm
        # return t * rpm / 9.5488)
        return (t * rpm / self.efficiency).to('watt') + self.idle_power

    def power_intermittent(self, rpm):
        if not isinstance(rpm, ureg.Quantity) or rpm.dimensionless:
            rpm *= ureg.tpm

        t = self.torque_intermittent(rpm)
        # return t * rpm
        # return t * rpm / 9.5488)
        return (t * rpm / self.efficiency).to('watt') + self.idle_power

    def plot_torque_speed_curve(self, highlight_power=None, highlight_torque=None, highlight_rpm=None, embed=False, full_title=True):
        x = np.linspace(self.min_rpm, self.max_rpm / self.gear_ratio, 100)  # * ureg.tpm
        # y1 = np.vectorize(m.torque_continuous)(x)
        # y2 = np.vectorize(m.torque_intermittent)(x)
        # y1 = [m.torque_continuous(x_) for x_ in x]
        # y2 = [m.torque_intermittent(x_) for x_ in x]
        y1 = np.array([self.torque_continuous(x_).to(ureg.newton * ureg.meter).magnitude for x_ in x]) * (ureg.newton * ureg.meter)
        y2 = np.array([self.torque_intermittent(x_).to(ureg.newton * ureg.meter).magnitude for x_ in x]) * (ureg.newton * ureg.meter)

        fig, ax1 = pylab.subplots()

        if full_title:
            ax1.set_title(self.name + " Torque, Power vs. Speed", fontsize=16.)
        else:
            ax1.set_title("Torque, Power vs. Speed", fontsize=16.)

        ax1.set_xlabel("Speed [RPM]", fontsize=12)
        ax1.set_ylabel("Torque [N m]", fontsize=12)
        xmin = x[0].magnitude
        xmax = x[-1].magnitude
        if highlight_rpm is not None:
            xmin = min(xmin, highlight_rpm.m * 0.9)
        if highlight_rpm is not None:
            xmax = max(xmax, highlight_rpm.m * 1.1)
        ax1.set_xlim([xmin, xmax])

        ax2 = ax1.twinx()
        ax2.set_ylabel("Power [W]", fontsize=12)

        colors = ['#aa0000ee', '#00aa00ee', '#ff0000ee', '#00ff00ee',
                  '#aaaa00ee', '#aa00aaee', '#00aaaaee']

        lns = []

        lns += ax1.plot(x.magnitude, y1.magnitude, color=colors[0], label='Continuous T')
        lns += ax2.plot(x.magnitude, (y1 * x / 9.5488).magnitude, color=colors[1], label='Continuous P')

        if self.torque_intermittent_define:
            lns += ax1.plot(x.magnitude, y2.magnitude, color=colors[2], label='Intermittent T')
            lns += ax2.plot(x.magnitude, (y2 * x / 9.5488).magnitude, color=colors[3], label='Intermittent P')

        #if highlight_power is not None:
        #    lns += [ax2.axhline(highlight_power.to('watt').magnitude, color=colors[4], label='Requested P')]
#
#        if highlight_torque is not None:
#            lns += [ax2.axhline(highlight_rpm.magnitude, color=colors[5], label='Requested T')]
#
#        if highlight_rpm is not None:
#            lns += [ax2.axvline(highlight_rpm.magnitude, color=colors[6], label='Requested RPM')]

        if highlight_rpm is not None and highlight_power is not None:
            ax2.scatter([highlight_rpm.magnitude], [highlight_power.to('watt').magnitude], label='Requested RPM,P')
            ax2.scatter([highlight_rpm.magnitude*.90], [highlight_power.to('watt').magnitude*.90], label='90% Requested RPM,P')
            ax2.scatter([highlight_rpm.magnitude*1.10], [highlight_power.to('watt').magnitude*1.10], label='110% Requested RPM,P')

        ax1.set_ylim(bottom=0)
        ax2.set_ylim(bottom=0)

        labs = [l.get_label() for l in lns]
        ax1.legend(lns, labs, loc='upper left')
        ax2.legend(loc='upper right')

        fig.tight_layout()
        if not embed:
            pylab.show()
            pylab.close()
            return None
        else:
            import io
            pylab.show()
            imgdata = io.BytesIO()
            pylab.savefig(imgdata, format='png', bbox_inches='tight')
            imgdata.seek(0)
            img_str = imgdata.getvalue()
            pylab.close()
            return img_str

    def clamp_speed(self, rpm):
        adjusted = False
        if rpm < self.min_rpm:
            rpm = self.min_rpm
            adjusted = True
        elif rpm > self.max_rpm:
            rpm = self.max_rpm
            adjusted = True
        return rpm, adjusted

    def clamp_thrust(self, thrust):
        adjusted = False
        if thrust < 0:
            thrust = 0
            adjusted = True
        elif thrust > self.max_feed_force:
            thrust = self.max_feed_force
            adjusted = True
        return thrust, adjusted


class LatheMachine(MachineType):
    def __init__(self):
        MachineType.__init__(self)
        self.efficiency_motor = 1.
        self.efficiency_belt = 1.
        self.efficiency_front_bearing = 1.
        self.efficiency_rear_bearing = 1.
        self.efficiency = (self.efficiency_motor * self.efficiency_belt *
                           self.efficiency_front_bearing * self.efficiency_rear_bearing)


class MillingMachine(MachineType):
    def __init__(self):
        MachineType.__init__(self)
        self.max_feed_force = 0 * ureg.lbs
        self.max_z_rate = Q_(0, 'inch / min')
        self.max_x_rate = Q_(0, 'inch / min')
        self.max_y_rate = Q_(0, 'inch / min')


class VerticalMillingMachine(MillingMachine):
    def __init__(self):
        MillingMachine.__init__(self)


class MachinePM25MV_LeadshineAxes(VerticalMillingMachine):
    def __init__(self):
        VerticalMillingMachine.__init__(self)
        self.name = 'PM25MV Leadshine'
        self.description = 'PM25MV milling machine Leadshine'
        # 300 lbs is the measured force, but the scale limit may have been exceeded.
        # The speed-torque curve of the Leadshine ES-32320-S Easy Servo Motor shows
        # the motor produces 1.8 Nm up to 360 RPM (with default holding current percentage
        # of 40%; increasing this percentage improves torque at higher RPMs).
        # David Clements' PM25-CNC kit uses 5mm pitch (5.08 TPI) ballscrews.
        # Converting the torque to a linear force:
        # F = T * 2Pi * (gear ratio) * (%eff) / (lead pitch)
        #
        # >>> Q_(1.8, 'newton meter') * 2 * math.pi * 1 * .95 / Q_(5, 'mm')
        # 2148.8493750554185 <Unit('newton')>
        # >>> (Q_(1.8, 'newton meter') * 2 * math.pi * 1 * .95 / Q_(5, 'mm')).to('lbf')
        # 483.080556886682 <Unit('force_pound')>
        #
        # Measured using a Taylor 5559 BIA scale. Could not find a manual for specifications,
        # but Amazon description says "Accurate to 300 lbs" and "330 lb capacity reading to the 0.2 lb."
        self.max_feed_force = 300 * ureg.lbs
        self.max_z_rate = Q_(100, 'inch / min')
        self.max_x_rate = Q_(100, 'inch / min')
        self.max_y_rate = Q_(100, 'inch / min')


class MachinePM25MV(MachinePM25MV_LeadshineAxes):
    def __init__(self):
        MachinePM25MV_LeadshineAxes.__init__(self)
        self.max_rpm = Q_(2500, 'turn / min')
        self.min_rpm = Q_(100, 'turn / min')
        self.name = 'PM25MV'
        self.description = 'PM25MV milling machine'

    # I have no information on the actual torque-speed curve; these are guesses.

    def _torque_continuous(self, abs_rpm):
        x1, y1 = Q_(0, 'tpm'), Q_(0., 'newton meter')
        x2, y2 = Q_(2500, 'tpm') / self.gear_ratio, Q_(2.85, 'newton meter') * self.gear_ratio
        dx = x1 - x2
        dy = y1 - y2
        m = dy / dx
        b = y1 - m * x1

        if self.min_rpm / self.gear_ratio <= abs_rpm <= self.max_rpm / self.gear_ratio:
            T = m * abs_rpm + b
        else:
            T = Q_(0, 'newton meter')

        return T

    def _torque_intermittent(self, rpm):
        return self._torque_continuous(rpm)

    def torque_range(self):
        return [Q_(0, 'newton meter'), Q_(2.85, 'newton meter')]


class MachinePM25MV_DMMServo(MachinePM25MV_LeadshineAxes):
    def __init__(self):
        MachinePM25MV_LeadshineAxes.__init__(self)
        self.max_rpm = Q_(5000, 'turn / min')
        self.min_rpm = Q_(10, 'turn / min')
        self.name = 'PM25MV_DMMServo'
        self.description = 'PM25MV milling machine with DMM 86M Servo'
        self.torque_intermittent_define = True

    # A - Continuous duty		B - Intermittent duty
    # Y	X	Y	X
    # Torque [N m]	Motor speed [min^-1]	Torque [N m]	Motor speed [min^-1]
    # 2.599975376	22.90076336	7.167741935	12.72264631
    # 2.592785028	2994.910941	7.160182221	3137.40458
    # 1.494459493	4969.465649	3.168628417	4979.643766
    # 0.275055405	4989.821883	0.26540261	4979.643766

    def _torque_continuous(self, abs_rpm):
        x1, y1 = Q_(2994.910941, 'tpm'), Q_(2.592785028, 'newton meter')
        x2, y2 = Q_(4969.465649, 'tpm'), Q_(1.494459493, 'newton meter')
        dx = x1 - x2
        dy = y1 - y2
        m = dy / dx
        b = y1 - m * x1

        if Q_(0, 'tpm') <= abs_rpm <= Q_(3000, 'tpm'):
            T = 2.6 * (ureg.newton * ureg.meter)
        elif Q_(3000, 'tpm') < abs_rpm < Q_(5000, 'tpm'):
            T = m * abs_rpm + b
        elif abs_rpm == Q_(5000, 'tpm'):
            T = Q_(1.5, 'newton meter')
        else:
            T = Q_(0, 'newton meter')

        return T

    def _torque_intermittent(self, abs_rpm):
        x1, y1 = Q_(3137.40458, 'tpm'), Q_(7.160182221, 'newton meter')
        x2, y2 = Q_(4979.643766, 'tpm'), Q_(3.168628417, 'newton meter')
        dx = x1 - x2
        dy = y1 - y2
        m = dy / dx
        b = y1 - m * x1

        if Q_(0, 'tpm') <= abs_rpm <= Q_(3100, 'tpm'):
            T = 7.2 * (ureg.newton * ureg.meter)
        elif Q_(3100, 'tpm') < abs_rpm < Q_(5000, 'tpm'):
            T = m * abs_rpm + b
        elif abs_rpm == Q_(5000, 'tpm'):
            T = Q_(3.2, 'newton meter')
        else:
            T = Q_(0, 'newton meter')

        return T

    def torque_range(self):
        return [Q_(2.6, 'newton meter'), Q_(7.2, 'newton meter')]


class MachinePM25MV_HS(MachinePM25MV_LeadshineAxes):
    def __init__(self):
        MachinePM25MV_LeadshineAxes.__init__(self)
        self.max_rpm = Q_(24000, 'turn / min')
        self.min_rpm = Q_(9000, 'turn / min')
        self.name = 'PM25MV_2.2kW24kRPM'
        self.description = 'PM25MV milling machine with 2.2kW24kRPM'
        self.torque_intermittent_define = True
        self._torque_x = [17985.882352941175, 20992.941176470587, 22983.529411764703, 23999.999999999996]
        self._torque_y = [1.0622589531680442, 0.9107438016528927, 0.8308539944903582, 0.7977961432506888]

    def _torque_both(self, abs_rpm):
        # Data sampled from the torque-speed curve of a similar spindle
        # https://www.damencnc.com/en/electrospindel-c41-47-c-db-p-er25-hy-2-2kw-18-000-24-000rpm/a14?c=32#gallery-3
        # using
        # https://apps.automeris.io/wpd/
        coeffs = np.polyfit(self._torque_x, self._torque_y, 2)

        if Q_(0, 'tpm') <= abs_rpm <= Q_(18000, 'tpm'):
            T = self._torque_y[0] * (ureg.newton * ureg.meter)
        elif Q_(18000, 'tpm') < abs_rpm < Q_(24000, 'tpm'):
            x_ = abs_rpm.to('turn / minute').magnitude
            T = coeffs.dot([x_ ** 2, x_, 1]) * (ureg.newton * ureg.meter)
        elif abs_rpm == Q_(24000, 'tpm'):
            T = Q_(self._torque_y[-1], 'newton meter')
        else:
            T = Q_(0, 'newton meter')

        return T

    def _torque_continuous(self, abs_rpm):
        return self._torque_both(abs_rpm)

    def _torque_intermittent(self, abs_rpm):
        # The VFD can increase torque, briefly, up to seemingly 200%, depending
        # on VFD settings, but lets conservatively estimate 120%.
        return self._torque_both(abs_rpm) * 1.2

    def torque_range(self):
        return [Q_(np.min(self._torque_y), 'newton meter'), Q_(np.max(self._torque_y), 'newton meter')]
