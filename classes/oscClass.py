from pyo import *

class ModOsc(Osc):
    def __init__(self, table, freq=1000, phase=0, interp=2, mul=1, add=0):
        return super().__init__(table, freq, phase, interp, mul, add)
    def getFreq(self):
        return self._freq

    def getMul(self):
        return self._mul
if __name__=="__main__":

    # TRY WITH A SIMPLE ModOsc

    s = Server().boot()
    s.start()
    t = DataTable(1000)
    o = ModOsc(t)
    print(o.getFreq())
