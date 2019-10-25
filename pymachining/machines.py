from pymachining.units import *


class MachineType:
    def __init__(self):
        self.max_rpm = float('inf')
        self.min_rpm = float('inf')
        self.gear_ratio = 1
        self.name = 'Unknown'
        self.description = 'Unknown'
        self.torque_intermittent_define = False

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
        return (t * rpm).to('watt')

    def power_intermittent(self, rpm):
        if not isinstance(rpm, ureg.Quantity) or rpm.dimensionless:
            rpm *= ureg.tpm

        t = self.torque_intermittent(rpm)
        # return t * rpm
        # return t * rpm / 9.5488)
        return (t * rpm).to('watt')

    def plot_torque_speed_curve(self, highlight_power=None, highlight_torque=None, highlight_rpm=None):
        import pylab
        import numpy as np

        x = np.linspace(self.min_rpm, self.max_rpm / self.gear_ratio, 100) * ureg.tpm

        # y1 = np.vectorize(m.torque_continuous)(x)
        # y2 = np.vectorize(m.torque_intermittent)(x)
        # y1 = [m.torque_continuous(x_) for x_ in x]
        # y2 = [m.torque_intermittent(x_) for x_ in x]
        y1 = np.array([self.torque_continuous(x_).magnitude for x_ in x]) * (ureg.newton * ureg.meter)
        y2 = np.array([self.torque_intermittent(x_).magnitude for x_ in x]) * (ureg.newton * ureg.meter)

        fig, ax1 = pylab.subplots()

        ax1.set_title(self.name + " Torque, Power vs. Speed", fontsize=16.)

        ax1.set_xlabel("Speed [RPM]", fontsize=12)
        ax1.set_ylabel("Torque [N m]", fontsize=12)
        ax1.set_xlim([x[0].magnitude, x[-1].magnitude])

        ax2 = ax1.twinx()
        ax2.set_ylabel("Power [W]", fontsize=12)

        colors = ['#ff0000ee', '#773300ee', '#00ff00ee', '#005533ee',
                  '#555533ee', '#22ff22ee', '#ff5533ee']

        lns = []

        lns += ax1.plot(x, y1, color=colors[0], label='Continuous T')
        lns += ax2.plot(x, y1 * x / 9.5488, color=colors[1], label='Continuous P')

        if self.torque_intermittent_define:
            lns += ax1.plot(x, y2, color=colors[2], label='Intermittent T')
            lns += ax2.plot(x, y2 * x / 9.5488, color=colors[3], label='Intermittent P')

        if highlight_power is not None:
            lns += [ax2.axhline(highlight_power.to('watt').magnitude, color=colors[4], label='Requested P')]

        if highlight_torque is not None:
            lns += [ax2.axhline(highlight_rpm.magnitude, color=colors[5], label='Requested T')]

        if highlight_rpm is not None:
            lns += [ax2.axvline(highlight_rpm.magnitude, color=colors[6], label='Requested RPM')]

        ax1.set_ylim(bottom=0)
        ax2.set_ylim(bottom=0)

        labs = [l.get_label() for l in lns]
        ax1.legend(lns, labs, loc='upper left')

        fig.tight_layout()
        pylab.show()


class MachinePM25MV(MachineType):
    def __init__(self):
        MachineType.__init__(self)
        self.max_rpm = 2500 * (ureg.turn / ureg.min)
        self.min_rpm = 0 * (ureg.turn / ureg.min)
        self.name = 'PM25MV'
        self.description = 'PM25MV milling machine'

    # I have no information on the actual torque-speed curve; these are guesses.

    def _torque_continuous(self, abs_rpm):
        x1, y1 = 0 * ureg.tpm, 0 * (ureg.newton * ureg.meter)
        x2, y2 = 2500 * ureg.tpm / self.gear_ratio, 2.85 * (ureg.newton * ureg.meter) * self.gear_ratio
        dx = x1 - x2
        dy = y1 - y2
        m = dy / dx
        b = y1 - m * x1

        if self.min_rpm / self.gear_ratio <= abs_rpm <= self.max_rpm / self.gear_ratio:
            T = m * abs_rpm + b
        else:
            T = 0 * (ureg.newton * ureg.meter)

        return T

    def _torque_intermittent(self, rpm):
        return self._torque_continuous(rpm)


class MachinePM25MV_DMMServo(MachineType):
    def __init__(self):
        MachineType.__init__(self)
        self.max_rpm = 5000 * (ureg.turn / ureg.min)
        self.min_rpm = 0 * (ureg.turn / ureg.min)
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
        x1, y1 = 2994.910941 * ureg.tpm, 2.592785028 * (ureg.newton * ureg.meter)
        x2, y2 = 4969.465649 * ureg.tpm, 1.494459493 * (ureg.newton * ureg.meter)
        dx = x1 - x2
        dy = y1 - y2
        m = dy / dx
        b = y1 - m * x1

        if 0 * ureg.tpm <= abs_rpm <= 3000 * ureg.tpm:
            T = 2.6 * (ureg.newton * ureg.meter)
        elif 3000 * ureg.tpm < abs_rpm < 5000 * ureg.tpm:
            T = m * abs_rpm + b
        elif abs_rpm == 5000 * ureg.tpm:
            T = 1.5 * (ureg.newton * ureg.meter)
        else:
            T = 0 * (ureg.newton * ureg.meter)

        return T

    def _torque_intermittent(self, abs_rpm):
        x1, y1 = 3137.40458 * ureg.tpm, 7.160182221 * (ureg.newton * ureg.meter)
        x2, y2 = 4979.643766 * ureg.tpm, 3.168628417 * (ureg.newton * ureg.meter)
        dx = x1 - x2
        dy = y1 - y2
        m = dy / dx
        b = y1 - m * x1

        if 0 * ureg.tpm <= abs_rpm <= 3100 * ureg.tpm:
            T = 7.2 * (ureg.newton * ureg.meter)
        elif 3100 * ureg.tpm < abs_rpm < 5000 * ureg.tpm:
            T = m * abs_rpm + b
        elif abs_rpm == 5000 * ureg.tpm:
            T = 3.2 * (ureg.newton * ureg.meter)
        else:
            T = 0

        return T
