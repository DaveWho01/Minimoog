import PySimpleGUI as sg


class GuiLayout:


    _font = ("Brain", 25)
    _font2 = ("Brain", 18)
    _font3 = ("", 9)

    def __init__(self, layout = []):

        power = sg.Column([
            [sg.Frame('', element_justification='c', layout = [[sg.Text('ON',  font=self._font2)], [sg.Slider(range = (0,1), enable_events=True, size = (3,20), disable_number_display=True,  key='-POWER-' )], [sg.Text('OFF',  font=self._font2)]]), sg.Text(' '*10)]
        ])

        left = sg.Column([
            [sg.Text('L E F T - H A N D', font=self._font)],
            [sg.Frame('LFO RATE', layout = [[sg.Slider(range = (0,50),  enable_events=True, resolution=.1, orientation='h', default_value = 5, key='-LFORATE-')]])],
            [sg.Frame('GLIDE', layout = [[sg.Slider(range = (0,1),  enable_events=True, size = (8.5,20), orientation='h', key='-GLIDEleft-' )]])],
            [sg.Frame('PITCH', element_justification='c', layout = [[sg.Slider(range = (-1,1),  enable_events=True, disable_number_display=True,  resolution=.1, default_value = 0, key='-PITCH-')]])],
            [sg.Button("Double Click Reset")]
        ], pad=(0,0), element_justification='c' )


        oscillatorBank_modifiers = sg.Column([
            [sg.Text('O S C I L L A T O R   B A N K', font=self._font)],
            [sg.Text('OSCILLATOR - 1', font=self._font2)],
            [sg.Text('', size=(10,1), key='-OUT1-', justification='right'),
            sg.Frame('RANGE', layout = [[sg.Slider(range = (6,1),enable_events=True, disable_number_display=True, orientation='h', size = (12,20), default_value = 4, key='-RANGE1-')]]),
            #sg.Text('\t\t\t     '),
            sg.Text('  0: Triangular\n  1: Tri-sawUp (sawDown in osc3)\n  2: Sawtooth up\n  3/4/5: Square', font= ("Helvetica", 10)),
            sg.Frame('WAVEFORM', layout = [[sg.Slider(range = (0,5), enable_events=True, orientation='h', key='-WAVE1-' )]])],

            [sg.Text('OSCILLATOR - 2', font=self._font2)],
            [sg.Text('', size=(10,1), key='-OUT2-', justification='right'),
            sg.Frame('RANGE', layout = [[sg.Slider(range = (6,1), enable_events=True, disable_number_display=True, orientation='h', size = (12,20), default_value = 4, key='-RANGE2-')]]),
            sg.Frame('FREQUENCY', layout = [[sg.Slider(range = (-8,8), enable_events=True, resolution=.1, orientation='h', key='-FREQ2-', default_value = 0 )]]),
            sg.Frame('WAVEFORM', layout = [[sg.Slider(range = (0,5), enable_events=True, orientation='h', key='-WAVE2-' )]])],

            [sg.Text('OSCILLATOR - 3', font=self._font2)],
            [sg.Text('', size=(10,1), key='-OUT3-', justification='right'),
            sg.Frame('RANGE', layout = [[sg.Slider(range = (6,1), enable_events=True, disable_number_display=True, orientation='h', size = (12,20), default_value = 4, key='-RANGE3-')]]),
            sg.Frame('FREQUENCY', layout = [[sg.Slider(range = (-8,8), enable_events=True,orientation='h', resolution=.01, key='-FREQ3-', default_value = 0 )]]),
            sg.Frame('WAVEFORM', layout = [[sg.Slider(range = (0,5), enable_events=True, orientation='h', key='-WAVE3-' )]])],



            [sg.Text('\n\nM O D I F I E R S', font=self._font)],
            [sg.Text('FILTER', font=self._font2)],
            [sg.Text(' '*18), sg.Frame('CUTOFF\nFREQUENCY', layout = [[sg.Slider(range = (10,32000), enable_events=True, resolution=1, orientation='h', size = (17,20), default_value = 32000, key='-CUTOFF-')]]),
            sg.Frame('\nEMPHASIS', layout = [[sg.Slider(range = (0,10), enable_events=True, resolution=.1,  orientation='h', size = (17,20),  default_value = .005, key='-EMPHASIS-' )]])],

            [sg.Text(' '*18), sg.Frame('ATTACK TIME', layout = [[sg.Slider(range = (0,10), enable_events=True, resolution=.001, orientation='h', size = (17,20), default_value = .005, key='-ATTACK-')]]),
            sg.Frame('DECAY TIME', layout = [[sg.Slider(range = (0,10), resolution=.001, enable_events=True, orientation='h', size = (17,20),  default_value = .005, key='-DECAY-' )]]),
            sg.Frame('SUSTAIN LEVEL', layout = [[sg.Slider(range = (0,1), resolution=.1, enable_events=True, size = (17,20), orientation='h',  default_value = 1, key='-SUSTAIN-' )]])],

            [sg.Text('\nLOUDNESS CONTOUR', font=self._font2)],
            [sg.Text(' '*18), sg.Frame('ATTACK TIME', layout = [[sg.Slider(range = (0,10), enable_events=True, resolution=.001, orientation='h', size = (17,20), default_value = .005, key='-ATTACKloud-')]]),
            sg.Frame('DECAY TIME', layout = [[sg.Slider(range = (0,10), resolution=.001, enable_events=True, orientation='h', size = (17,20),  default_value = .005, key='-DECAYloud-' )]]),
            sg.Frame('SUSTAIN LEVEL', layout = [[sg.Slider(range = (0,1), resolution=.1, size = (17,20), enable_events=True, orientation='h',  default_value = 1, key='-SUSTAINloud-' )]])],
        ], pad=(0,0), element_justification='c')

        controllers_mixer = sg.Column([
            [sg.Text('C O N T R O L L E R S', font=self._font)],
            [sg.Frame('TUNE', layout = [[sg.Slider(range = (-2.5,2.5), enable_events=True, resolution=.1, orientation='h', default_value = 0, key='-TUNE-')]])],
            [sg.Frame('GLIDE', layout = [[sg.Slider(range = (0,10),  enable_events=True, resolution=.01, orientation='h', default_value = .05, key='-GLIDE-')]])],
            [sg.Frame('MODULATION', layout = [[sg.Slider(range = (0,2), enable_events=True, size = (15,20), orientation='h', default_value = 1, disable_number_display=True, key='-MODULATION-')]])],
            [sg.Frame('', element_justification='c', layout = [[sg.Text('OSC 3',  font=self._font3)], [sg.Slider(range = (0,1),  enable_events=True, size = (3,20), disable_number_display=True,  key='-OSC3/EG-' )], [sg.Text('FILTER EG',  font=self._font3)]]),
             sg.Frame('', element_justification='c', layout = [[sg.Text('NOISE',  font=self._font3)], [sg.Slider(range = (0,1),  enable_events=True, size = (3,20), disable_number_display=True,  key='-NOISE/LFO-' )], [sg.Text('LFO',  font=self._font3)]]) ],



            [sg.Text('\nM I X E R', font=self._font)],
            [sg.Frame('VOLUME OSC1', layout = [[sg.Slider(range = (0,10), enable_events=True, resolution=.1, orientation='h', default_value = 5, key='-VOLUME1-')]]),
            sg.Frame(' ', layout = [[sg.Slider(range = (0,1), enable_events=True, orientation='h', size = (8,20), default_value = 1, key='-ON1-')]])],

            [sg.Frame('VOLUME OSC2', layout = [[sg.Slider(range = (0,10), enable_events=True, resolution=.1, orientation='h', default_value = 5, key='-VOLUME2-')]]),
            sg.Frame(' ', layout = [[sg.Slider(range = (0,1), enable_events=True, orientation='h', size = (8,20), default_value = 0, key='-ON2-')]])],

            [sg.Frame('VOLUME OSC3', layout = [[sg.Slider(range = (0,10), resolution=.1, enable_events=True, orientation='h', default_value = 5, key='-VOLUME3-')]]),
            sg.Frame(' ', layout = [[sg.Slider(range = (0,1), enable_events=True, orientation='h', size = (8,20), default_value = 0, key='-ON3-')]])],

            [sg.Frame('', element_justification='c', layout = [[sg.Text('WHITE',  font=self._font3)], [sg.Slider(range = (0,1), enable_events=True, size = (3,20), disable_number_display=True,  key='-W/P-' )], [sg.Text('PINK',  font=self._font3)]] ),
            sg.Frame('NOISE VOLUME', layout = [[sg.Slider(range = (0,10), enable_events=True, resolution=.1, orientation='h', default_value = 1, key='-NOISEVOLUME-')]]),
            sg.Frame(' ', layout = [[sg.Slider(range = (0,1), enable_events=True, orientation='h', size = (8,20), default_value = 0, key='-ONnoise-')]]),
            sg.Text(' '*13),
            ],

        ], pad=(0,0), element_justification='c')


        self._layout = [[power, left, controllers_mixer, oscillatorBank_modifiers]]

    def __iter__(self):
        return iter(self._layout)
