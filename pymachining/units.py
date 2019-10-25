import pint

ureg = pint.UnitRegistry(auto_reduce_dimensions=True)
# ureg.rpm is already defined as [revolution/minute] = [2Pi turn/minute]
# To avoid a lot of error prone scaling by 2Pi, define ureg.tpm as [1 turn/minute]
ureg.tpm = ureg.turn / ureg.min
