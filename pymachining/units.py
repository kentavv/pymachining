import pint

# Units defined in Pint are browsable at
# https://github.com/hgrecco/pint/blob/master/pint/default_en.txt

ureg = pint.UnitRegistry(auto_reduce_dimensions=True)

# ureg.rpm is already defined as [revolution/minute] = [2Pi turn/minute]
# To avoid error prone scaling by 2Pi, define [tpm] = [1 turn/minute]

ureg.define('tpm = turn / minute')
ureg.define('tps = turn / second')

# But turn is also defined in terms of radians
# From default_en.txt:
# radian = [] = rad
# turn = 2 * π * radian = _ = revolution = cycle = circle
# revolutions_per_minute = revolution / minute = rpm
#
# Defining turn and revolution without radians eliminates the 2Pi constant,
# however, other complications occur. Most noticeable is power calculations
# will be 2Pi smaller than expected. Torque is defined as Nm or J/radian and
# [Watt] = [J]/[s]. [P] = [T] * [RPM], and if RPM is not 2Pi radians / minute,
# power will be 2PI smaller than expected when expressed as watts.
# ureg.define('turn = [] = revolution')
# ureg.define('revolutions_per_minute = revolution / minute = rpm')
