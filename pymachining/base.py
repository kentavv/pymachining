class PyMachiningBase:
    def __init__(self):
        pass


class PyMachiningException(Exception):
    def __init__(self, s=''):
        Exception.__init__(self)
        self.description = s
