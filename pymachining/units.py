import pint

# Units defined in Pint are browsable at
# https://github.com/hgrecco/pint/blob/master/pint/default_en.txt

ureg = pint.UnitRegistry(auto_reduce_dimensions=True)

# ureg.rpm is already defined as [revolution/minute] = [2Pi turn/minute]
# To avoid error prone scaling by 2Pi, define [tpm] = [1 turn/minute]

ureg.define('tpm = turn / minute')
ureg.define('tps = turn / second')
Q_ = ureg.Quantity

# But turn is also defined in terms of radians
# From default_en.txt:
#   radian = [] = rad
#   turn = 2 * π * radian = _ = revolution = cycle = circle
#   revolutions_per_minute = revolution / minute = rpm
#
# Defining turn and revolution without radians eliminates the 2Pi constant.
#   ureg.define('turn = [] = revolution')
#   ureg.define('revolutions_per_minute = revolution / minute = rpm')
# However, this complicates conversions, including power calculations that
# could be 2Pi smaller than expected. I'll try to explain why.
# Torque and Joule have dimensions Nm, but torque is an angular force while
# Joule measures energy. Torque (T) and Energy (E) are related by
#   Energy = Torque x Distance
# and Power is energy over time.
#   P = E / t
# Expansion:
#   θ [rad] = angular distance = 2π x (number of turns)
#   ω [rad] / [s] = angular velocity = θ [rad] / t [s]
#   E [J] = T [Nm] * θ [rad]
#   P [W] = T [Nm] * ω [rad] / [s]
#   P [W] = E [J] / t [s]
#
# Common equations are:
#   Power [kW] = Torque [Nm] x Speed [RPM] / 9.5493
#
# Derivation:
#   ω [rad] / [s] = angular velocity
#                 = (RPM [rev] / [min]) * (1 [min] / 60 [s]) * (2π ([rad] / [rev]))
#                 = (RPM [rev] / [min]) * (1 [min] / 9.5493 [s]) * (1 ([rad] / [rev]))
#                 = RPM * ([rad] / 9.5493 [s])
#   P = T * ω
#   P = T * RPM * ([rad] / 9.5493 [s])
#   P = T * RPM / 9.5493
