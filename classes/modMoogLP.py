from pyo import *

class MMoogLP(MoogLP):
    """
    A fourth-order resonant lowpass filter.

    Digital approximation of the Moog VCF, giving a decay of 24dB/oct.

    :Parent: :py:class:`PyoObject`

    :Args:

        input: PyoObject
            Input signal to process.
        freq: float or PyoObject, optional
            Cutoff frequency of the filter. Defaults to 1000.
        res: float or PyoObject, optional
            Amount of Resonance of the filter, usually between 0 (no resonance)
            and 1 (medium resonance). Self-oscillation occurs when the
            resonance is >= 1. Can go up to 10. Defaults to 0.

    >>> s = Server().boot()
    >>> s.start()
    >>> ph = Phasor(40)
    >>> sqr = Round(ph, add=-0.5)
    >>> lfo = Sine(freq=[.4, .5], mul=2000, add=2500)
    >>> fil = MoogLP(sqr, freq=lfo, res=1.25).out()

    """

    def __init__(self, input, freq=1000, res=0, mul=1, add=0):
        pyoArgsAssert(self, "oOOOO", input, freq, res, mul, add)
        PyoObject.__init__(self, mul, add)
        self._input = input
        self._freq = freq
        self._res = res
        self._in_fader = InputFader(input)
        in_fader, freq, res, mul, add, lmax = convertArgsToLists(self._in_fader, freq, res, mul, add)
        self._base_objs = [
            MoogLP_base(wrap(in_fader, i), wrap(freq, i), wrap(res, i), wrap(mul, i), wrap(add, i)) for i in range(lmax)
        ]
        self._init_play()



    def getMul(self):
        return self._mul

    def __repr__(self):
        return self._mul
