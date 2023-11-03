from pyo import *

#-------------------------SERVER INITILIZATION---------------------------

def init():
    s = Server(nchnls=1)
    s.setMidiInputDevice(99)
    s.boot()
    s.start()
    return s


#-------------------------IMPORT WAVEFORMS---------------------------

def import_waves():
    from pathlib import Path
    import os
    wdir = Path(__file__).absolute().parent
    waves = {}
    for r, d, f in os.walk(wdir):
        for file in f:
            if file.endswith(".txt"):
                f = open((os.path.join(r, file)))
                content = f.read()
                wavetable = list(float(x) for x in content.split(","))
                waves[(str(f.name)).split("\\")[-1][:-4]] = DataTable(size=len(wavetable),init=wavetable)

    #waveform list for osc1 and osc2
    wavelist_12 = [waves["triangle"],waves["trisaw"],waves["sawup"],waves["stdsquare"],waves["square2"],waves["square3"]]
    # waveform list for osc3
    wavelist_3 = [waves["triangle"],waves["sawdown"],waves["sawup"],waves["stdsquare"],waves["square2"],waves["square3"]]

    return wavelist_12, wavelist_3


#-------------------------ADSR (for initialization)---------------------------

def setInitialAdsr(velocity):
    amps1 = MidiAdsr(velocity, attack=0.5, decay=0, sustain=1, release=0.2, mul=1)
    amps2 = MidiAdsr(velocity, attack=0.5, decay=0, sustain=1, release=0.2, mul=1)
    amps3 = MidiAdsr(velocity, attack=0.5, decay=0, sustain=1, release=0.2, mul=1)
    ampsWN = MidiAdsr(velocity, attack=0.5, decay=0, sustain=1, release=0.2, mul=1)
    ampsPN = MidiAdsr(velocity, attack=0.5, decay=0, sustain=1, release=0.2, mul=1)
    ampsLP = MidiAdsr(velocity, attack=0.5, decay=0, sustain=1, release=0.2, mul=1)

    return amps1, amps2, amps3, ampsWN, ampsPN, ampsLP


#-------------------------RANGE (OCTAVE)---------------------------

def updateOctave(window, values):
    window.Element('-OUT1-').Update(2**int(values['-RANGE1-']))
    window.Element('-OUT2-').Update(2**int(values['-RANGE2-']))
    window.Element('-OUT3-').Update(2**int(values['-RANGE3-']))

def setRange(osc, values, default):

    if values != default :
        osc.setFreq(osc.getFreq()*(2**(default-values)))
        default = values
    return default


#-------------------------GLIDE---------------------------

def setGlide(l, values):
    for osc in l:
        osc.setRiseTime(values)
        osc.setFallTime(values)


#-------------------------PITCH---------------------------

def setPitch(l, values, tmp):

    if values != tmp:
        for osc in l:
            if values > tmp:
                osc.setFreq(osc.getFreq()/(2**-(values-tmp)))
            else:
                osc.setFreq(osc.getFreq()*(2**(values-tmp)))
    tmp = values
    return tmp


#-------------------------TUNE---------------------------

def setTune(l, values, tmp):

    if values != tmp:
        for osc in l:
            if values <= tmp:
                osc.setFreq(osc.getFreq()/(1.059**-(values-tmp)))
            else:
                osc.setFreq(osc.getFreq()*(1.059**(values-tmp)))
    tmp = values

    return tmp


#-------------------------FREQUENCY---------------------------

def setFrequency(osc, values, tmp):

    if values != tmp:
        if values <= tmp:
            osc.setFreq(osc.getFreq()/(1.059**-(values-tmp)))
        else:
            osc.setFreq(osc.getFreq()*(1.059**(values-tmp)))
    tmp = values

    return tmp

#-------------------------VOLUME---------------------------

def setVolume(amps, on, values, n):
    if on==1: amps.setMul(values/n)
    else: amps.setMul(0)



#-------------------------ADSR loudness---------------------------

def setADSR(l, attack, decay, sustain):
    for amps in l:
        amps.setAttack(attack);
        amps.setDecay(decay);
        amps.setSustain(sustain)


#-------------------------FIX OSC3 (after modulation) ---------------------------

def fixOsc3(LPfilt, ampsLP, modOsc3, osc3, freq3, Glide3):

    modOsc3.stop(0)
    modOsc3zero=True
    osc3.setFreq(Glide3*1.059**(freq3))
    LPfilt.setMul(ampsLP)

    return modOsc3zero
