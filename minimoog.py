from pathlib import Path
import os

def import_waves():
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



def updateOctave(window, values):
    window.Element('-OUT1-').Update(2**int(values['-RANGE1-']))
    window.Element('-OUT2-').Update(2**int(values['-RANGE2-']))
    window.Element('-OUT3-').Update(2**int(values['-RANGE3-']))



#######################################################################################################################################


from pyo import *
import PySimpleGUI as sg
from guiClass import GuiLayout
from oscClass import ModOsc


s = Server(nchnls=1)
s.setMidiInputDevice(99)
s.boot()
s.start()

wavelist_12, wavelist_3 = import_waves()

# GUI
sg.theme('DarkPurple6')
layout = GuiLayout()
window = sg.Window("minimoog", layout)

#variables
checkPower=0
notes = Notein(scale=1)
notes.setCentralKey(6)
amps1 = MidiAdsr(notes["velocity"], attack=0.5, decay=0, sustain=1, release=0.2, mul=1)
amps2 = MidiAdsr(notes["velocity"], attack=0.5, decay=0, sustain=1, release=0.2, mul=1)
amps3 = MidiAdsr(notes["velocity"], attack=0.5, decay=0, sustain=1, release=0.2, mul=1)
ampsWN = MidiAdsr(notes["velocity"], attack=0.5, decay=0, sustain=1, release=0.2, mul=1)
ampsPN = MidiAdsr(notes["velocity"], attack=0.5, decay=0, sustain=1, release=0.2, mul=1)
ampsLP = MidiAdsr(notes["velocity"], attack=0.5, decay=0, sustain=1, release=0.2, mul=1)


defosc1 = 4; defosc2 = 4; defosc3 = 4
tmptune = 0; tmpf2 = 0; tmpf3 = 0
# OSCILLATORS
t = DataTable(1000)
a1 = notes['pitch']
a2 = notes['pitch']
a3 = notes['pitch']
Glide1 = Port(a1,1,1)
Glide2 = Port(a2,1,1)
Glide3 = Port(a3,1,1)
osc1 = ModOsc(table=t, freq=Glide1, mul=amps1)
osc2 = ModOsc(table=t, freq=Glide2, mul=amps2)
osc3 = ModOsc(table=t, freq=Glide3, mul=amps3)
# NOISE GENERATOR
whiteN = Noise(mul=ampsWN)
pinkN = PinkNoise(mul=ampsPN)
# MIXes
mix2filter = Mix(input=[osc1,osc2,osc3,whiteN,pinkN])
# FILTER
LPfilt = MoogLP(input=mix2filter,mul=ampsLP)


# MAIN CYCLE
while True:

    event, values = window.read()
    #print (event, values)
    if event == sg.WIN_CLOSED :
        break

    if values['-POWER-']==1:
        checkPower=1
        updateOctave(window, values)


        # ---------------------- OSCILLATORS ------------------------------

        # OSC1
        #       Range
        if values['-RANGE1-'] != defosc1 :
            osc1.setFreq(osc1.getFreq()*(2**(defosc1-values['-RANGE1-'])))
            defosc1 = values['-RANGE1-']
        #       Tune
        if values['-TUNE-'] != tmptune:
            if values['-TUNE-'] <= tmptune:
                osc1.setFreq(osc1.getFreq()/(1.059**-(values['-TUNE-']-tmptune)))
                osc2.setFreq(osc2.getFreq()/(1.059**-(values['-TUNE-']-tmptune)))
                osc3.setFreq(osc3.getFreq()/(1.059**-(values['-TUNE-']-tmptune)))
            else:
                osc1.setFreq(osc1.getFreq()*(1.059**(values['-TUNE-']-tmptune)))
                osc2.setFreq(osc2.getFreq()*(1.059**(values['-TUNE-']-tmptune)))
                osc3.setFreq(osc3.getFreq()*(1.059**(values['-TUNE-']-tmptune)))
            tmptune = values['-TUNE-']

        #       Waveform
        osc1.setTable(wavelist_12[int(values['-WAVE1-'])])


        # OSC2
        #       Range
        if values['-RANGE2-'] != defosc2 :
            osc2.setFreq(osc2.getFreq()*(2**(defosc2-values['-RANGE2-'])))
            defosc2 = values['-RANGE2-']

        #       Frequency
        if values['-FREQ2-'] != tmpf2:
            if values['-FREQ2-'] < tmpf2:
                osc2.setFreq(osc2.getFreq()/(1.059**-(values['-FREQ2-'] - tmpf2)))
            elif values['-FREQ2-'] > tmpf2:
                osc2.setFreq(osc2.getFreq()*(1.059**(values['-FREQ2-'] - tmpf2)))
            tmpf2 = values['-FREQ2-']

        #       Waveform
        osc2.setTable(wavelist_12[int(values['-WAVE2-'])])


        # OSC3
        #       Range
        if values['-RANGE3-'] != defosc3 :
            osc3.setFreq(osc3.getFreq()*(2**(defosc3-values['-RANGE3-'])))
            defosc3 = values['-RANGE3-']

        #       Frequency
        if values['-FREQ3-'] != tmpf3:
            if values['-FREQ3-'] < tmpf3:
                osc3.setFreq(osc3.getFreq()/(1.059**-(values['-FREQ3-'] - tmpf3)))
            elif values['-FREQ3-'] > tmpf3:
                osc3.setFreq(osc3.getFreq()*(1.059**(values['-FREQ3-'] - tmpf3)))
            tmpf3 = values['-FREQ3-']

        #       Waveform
        osc3.setTable(wavelist_3[int(values['-WAVE3-'])])


        # ---------------------- MIXER ------------------------------

        # OSCs Volume
        if values['-ON1-']==1: amps1.setMul(values['-VOLUME1-']/30)
        else: amps1.setMul(0)

        if values['-ON2-']: amps2.setMul(values['-VOLUME2-']/30)
        else: amps2.setMul(0)

        if values['-ON3-']: amps3.setMul(values['-VOLUME3-']/30)
        else: amps3.setMul(0)
        
        # Noise Volume
        if values['-ONnoise-']==1:
            if values['-W/P-']==0:
                ampsWN.setMul(0)
                ampsPN.setMul(values['-NOISEVOLUME-']/30)
            if values['-W/P-']==1:
                ampsPN.setMul(0)
                ampsWN.setMul(values['-NOISEVOLUME-']/30)
        else:
            ampsPN.setMul(0)
            ampsWN.setMul(0)

        # Filter
        LPfilt.setFreq(values['-CUTOFF-'])
        LPfilt.setRes(values['-EMPHASIS-'])

        ampsLP.setAttack(values['-ATTACK-'])
        ampsLP.setDecay(values['-DECAY-'])
        ampsLP.setSustain(values['-SUSTAIN-'])

        # Loudness Contour

        amps1.setAttack(values['-ATTACKloud-']); amps1.setDecay(values['-DECAYloud-']); amps1.setSustain(values['-SUSTAINloud-'])
        amps2.setAttack(values['-ATTACKloud-']); amps2.setDecay(values['-DECAYloud-']); amps2.setSustain(values['-SUSTAINloud-'])
        amps3.setAttack(values['-ATTACKloud-']); amps3.setDecay(values['-DECAYloud-']); amps3.setSustain(values['-SUSTAINloud-'])
        ampsWN.setAttack(values['-ATTACKloud-']); ampsWN.setDecay(values['-DECAYloud-']); ampsWN.setSustain(values['-SUSTAINloud-'])
        ampsPN.setAttack(values['-ATTACKloud-']); ampsPN.setDecay(values['-DECAYloud-']); ampsPN.setSustain(values['-SUSTAINloud-'])

        # OUTs

        a1 = osc1.getFreq()
        a2 = osc1.getFreq()
        a3 = osc1.getFreq()
        LPfilt.out()

        


    elif values['-POWER-']==0 and checkPower==1:
        break



window.close()
