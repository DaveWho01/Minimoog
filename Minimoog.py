import functions
from pyo import *
import PySimpleGUI as sg
from classes.guiClass import GuiLayout
from classes.oscClass import ModOsc
from classes.modMoogLP import MMoogLP
import warnings

warnings.filterwarnings('ignore')

 # server initialization
s = functions.init()

# import waveforms
wavelist_12, wavelist_3 = functions.import_waves()

# variables initialization
modOsc3zero=False
check=0; checkPower=0

defosc1 = 4; defosc2 = 4; defosc3 = 4               # 2**4=16, cioè il range di default all'accensione
tmptune = 0; tmpf2 = 0; tmpf3 = 0; tmpPitch=0

# GUI
sg.theme('LightGray1') #DarkPurple6 #DarkGray3
layout = GuiLayout()
window = sg.Window("minimoog", layout)

# MIDI
notes = Notein(poly=1,scale=1)
notes.setStealing(True)         # MONO
notes.setCentralKey(6)

# OSCILLATOR'S ADSR for initialization
amps1, amps2, amps3, ampsWN, ampsPN, ampsLP = functions.setInitialAdsr(notes["velocity"])

# OSCILLATORS
t = DataTable(1000)
Glide1 = Port(notes['pitch'],0,0)
Glide2 = Port(notes['pitch'],0,0)
Glide3 = Port(notes['pitch'],0,0)
osc1 = ModOsc(table=t, freq=Glide1, mul=amps1)
osc2 = ModOsc(table=t, freq=Glide2, mul=amps2)
osc3 = ModOsc(table=t, freq=Glide3, mul=amps3)

# NOISE GENERATOR
whiteN = Noise(mul=ampsWN)
pinkN = PinkNoise(mul=ampsPN)

# MIXes
mix2filter = Mix(input=[osc1,osc2,osc3,whiteN,pinkN])
modOsc3Mix = Mix(input=[osc1,osc2])
modNoiseMix = Mix(input=[osc1,osc2, osc3])

# FILTERS
LPfilt = MMoogLP(input=mix2filter,mul=1)
modOsc3Filt = MMoogLP(input=mix2filter,mul=ampsLP)
modPinkFilt = MMoogLP(input=modNoiseMix*3,mul=ampsLP)
modWhiteFilt = MMoogLP(input=modNoiseMix*3,mul=ampsLP)

# OSC3 MODULATION
modOsc3 = modOsc3Filt*osc3
modWhiteN= modWhiteFilt*whiteN
modPinkN = modPinkFilt*pinkN

# LFO for left-hand
lfo = LFO(freq=0.6, type=3)
LPfiltLFO=LPfilt*lfo


#-----------------------------------------------------------------------------
# ------------------------------MAIN CYCLE------------------------------------
#-----------------------------------------------------------------------------

while True:

    event, values = window.read()
    if event == sg.WIN_CLOSED :
        break

    if values['-POWER-']==1:                # Fisrt of all check if power is on
        checkPower=1

        functions.updateOctave(window, values)


    # ---------------------- LEFT HAND / CONTROLLERS ------------------------------
        #### GLIDE ####
        if values['-GLIDEleft-']==1:
            functions.setGlide([Glide1, Glide2, Glide3], values['-GLIDE-'])
        else:
            functions.setGlide([Glide1, Glide2, Glide3], 0)

        #### PITCH ####
        tmpPitch = functions.setPitch([osc1,osc2,osc3], values['-PITCH-'], tmpPitch)

        if event=="Double Click Reset":                     # reset pitch to default=0
            if values['-PITCH-'] != 0:
                window['-PITCH-'].update(value = 0)
                window.refresh()


    #-----------------------OSCILLATOR BANK / CONTROLLERS  ----------------------------
        # -----OSC1-----
        defosc1 = functions.setRange(osc1, values['-RANGE1-'], defosc1)                 # RANGE osc1
        tmptune = functions.setTune([osc1, osc2, osc3], values['-TUNE-'], tmptune)      # TUNE (all oscillators)
        osc1.setTable(wavelist_12[int(values['-WAVE1-'])])                              # WAVEFORM osc1

        # -----OSC2-----
        defosc2 = functions.setRange(osc2, values['-RANGE2-'], defosc2)                 # RANGE osc2
        tmpf2 = functions.setFrequency(osc2, values['-FREQ2-'], tmpf2)                  # FREQUENCY osc2
        osc2.setTable(wavelist_12[int(values['-WAVE2-'])])                              # WAVEFORM osc2

        # -----OSC3-----
        defosc3 = functions.setRange(osc3, values['-RANGE3-'], defosc3)                 # RANGE osc3
        tmpf3 = functions.setFrequency(osc3, values['-FREQ3-'], tmpf3)                  # FREQUENCY osc3
        osc3.setTable(wavelist_3[int(values['-WAVE3-'])])                               # WAVEFORM osc3


    # ---------------------- MIXER ------------------------------

        # OSCs Volume
        functions.setVolume(amps1, values['-ON1-'], values['-VOLUME1-'], 30)
        functions.setVolume(amps2, values['-ON2-'], values['-VOLUME2-'], 30)
        functions.setVolume(amps3, values['-ON3-'], values['-VOLUME3-'], 30)


        # Noise Volume
        if values['-ONnoise-']==1:
            if values['-W/P-']==0:
                ampsWN.setMul(0)
                ampsPN.setMul(values['-NOISEVOLUME-']/100)
            if values['-W/P-']==1:
                ampsPN.setMul(0)
                ampsWN.setMul(values['-NOISEVOLUME-']/100)
        else:
            ampsPN.setMul(0)
            ampsWN.setMul(0)



    # ----------------- MODULATION (left-hand, osc3, filter, noise, lfo) -------------------------------

        LPfiltStop=0                                        # check for stopping/starting LPfilt.out(). Stop if LPFiltStop==1, play if LPfiltStop==0

    ########### NOISE / LFO AS MODULATION ###########

        if values['-MODULATION-']==2:
            if values['-NOISE/LFO-']==0:                    #  LFO AS MODULATION
                check=1
                lfo.setFreq(values["-LFORATE-"])
                LPfiltLFO.out()

            else:                                           #  NOISE AS MODULATION
                LPfilt.stop(0)
                LPfiltStop=1
                functions.setVolume(amps1, values['-ON1-'], values['-VOLUME1-'], 5)     #fix volumes
                functions.setVolume(amps2, values['-ON2-'], values['-VOLUME2-'], 5)
                functions.setVolume(amps3, values['-ON3-'], values['-VOLUME3-'], 5)

                if values['-W/P-']==0:      # pink noise
                    modWhiteN.stop()
                    modPinkN.out()
                elif values['-W/P-']==1:    # white noise
                    modPinkN.stop()
                    modWhiteN.out()


    ########### OSC3 / FILTER EG AS MODULATION ###########

        if values['-MODULATION-']==0:

            if values['-OSC3/EG-']==1:                      #  OSC3 AS MODULATION
                LPfiltStop=1
                LPfilt.stop(0)

                osc3.setFreq(values['-FREQ3-']*10)

                ### fix volumes
                functions.setVolume(amps1, values['-ON1-'], values['-VOLUME1-'], 10)
                functions.setVolume(amps2, values['-ON2-'], values['-VOLUME2-'], 10)
                functions.setVolume(amps3, values['-ON3-'], values['-VOLUME3-'], 10)

                if modOsc3zero==True: modOsc3=modOsc3Filt*osc3; modOsc3zero=False
                modOsc3.out()
                check=1

            elif values['-OSC3/EG-']==0 :                   #  FILTER EG AS MODULATION
                LPfilt.setFreq(values['-CUTOFF-']*ampsLP)                                                   # cutoff ADSR
                functions.setADSR([ampsLP], values['-ATTACK-'], values['-DECAY-'], values['-SUSTAIN-'])     # set filter adsr
                modOsc3zero=functions.fixOsc3(LPfilt, ampsLP, modOsc3, osc3, values['-FREQ3-'], Glide3)     # fix osc3
                defosc3 = functions.setRange(osc3, values['-RANGE3-'], defosc3)
                check=1


    ########### NO MORE MODULATION, restore "normal" values ###########

        elif values['-MODULATION-']==1 and check==1:
            check=0

            ### fix osc3
            modOsc3zero=functions.fixOsc3(LPfilt, ampsLP, modOsc3, osc3, values['-FREQ3-'], Glide3)

            ### fix filterEG
            LPfilt.setFreq(values['-CUTOFF-'])              # sistemo filter EG
            functions.setADSR([ampsLP], values['-ATTACKloud-'], values['-DECAYloud-'], values['-SUSTAINloud-'])

            ### fix LFO
            LPfiltLFO.stop(0)

            ### fix noise
            modWhiteN.stop(0); modPinkN.stop(0)


    # ---------------------- MODIFIERS ------------------------------

        # Filter
        LPfilt.setRes(values['-EMPHASIS-'])
        LPfilt.setFreq(values['-CUTOFF-'])

        # Loudness Contour
        functions.setADSR([amps1, amps2, amps3, ampsWN, ampsPN], values['-ATTACKloud-'], values['-DECAYloud-'], values['-SUSTAINloud-'])


        # OUTs
        if LPfiltStop==0: LPfilt.out()


# ---------------------- POWER OFF ------------------------------

    elif values['-POWER-']==0 and checkPower==1:
        break

#-----------------------------------------------------------------------------
# ------------------------------END MAIN CYCLE------------------------------------
#-----------------------------------------------------------------------------


window.close()
