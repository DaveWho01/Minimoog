import PySimpleGUI as sg


class GuiLayout:
    

    _font = ("Brain", 22)
    _font2 = ("Brain", 18)
    _font3 = ("", 9)

    def __init__(self, layout = []):

        power = sg.Column([
            #[sg.Frame('', layout =[[sg.Button("POWER", key='-POWER-')]])]
            [sg.Frame('POWER', layout = [[sg.Slider(range = (0,1),  size = (3,20), enable_events=True, default_value = 0, key='-POWER-')]])]
        ])

        oscillatorBank_modifiers = sg.Column(  [
            [sg.Text(' '*41 + 'O S C I L L A T O R   B A N K', font=self._font)],
            [sg.Text(' '*66 + 'OSCILLATOR - 1', font=self._font2)],
            [sg.Text('', size=(10,1), key='-OUT1-', justification='right'),
            sg.Frame('RANGE', layout = [[sg.Slider(range = (6,1),enable_events=True, disable_number_display=True, orientation='h', size = (12,20), default_value = 4, key='-RANGE1-')]]),
            #sg.Text('\t\t\t     '),
            sg.Text('  0: Triangular\n  1: Tri-sawUp (sawDown in osc3)\n  2: Sawtooth up\n  3/4/5: Square', font= ("Helvetica", 10)),
            sg.Frame('WAVEFORM', layout = [[sg.Slider(range = (0,5), enable_events=True, orientation='h', key='-WAVE1-' )]])],

            [sg.Text(' '*66 + 'OSCILLATOR - 2', font=self._font2)],
            [sg.Text('', size=(10,1), key='-OUT2-', justification='right'),
            sg.Frame('RANGE', layout = [[sg.Slider(range = (6,1), enable_events=True, disable_number_display=True, orientation='h', size = (12,20), default_value = 4, key='-RANGE2-')]]),
            sg.Frame('FREQUENCY', layout = [[sg.Slider(range = (-8,8), enable_events=True, resolution=.1, orientation='h', key='-FREQ2-', default_value = 0 )]]),
            sg.Frame('WAVEFORM', layout = [[sg.Slider(range = (0,5), enable_events=True, orientation='h', key='-WAVE2-' )]])],

            [sg.Text(' '*66 + 'OSCILLATOR - 3', font=self._font2)],
            [sg.Text('', size=(10,1), key='-OUT3-', justification='right'),
            sg.Frame('RANGE', layout = [[sg.Slider(range = (6,1), enable_events=True, disable_number_display=True, orientation='h', size = (12,20), default_value = 4, key='-RANGE3-')]]),
            sg.Frame('FREQUENCY', layout = [[sg.Slider(range = (-8,8), enable_events=True,orientation='h', resolution=.1, key='-FREQ3-', default_value = 0 )]]),
            sg.Frame('WAVEFORM', layout = [[sg.Slider(range = (0,5), enable_events=True, orientation='h', key='-WAVE3-' )]])],


            [sg.Text('\n\n' + ' '*59 +  'M O D I F I E R S', font=self._font)],
            [sg.Text(' '*83 +'FILTER', font=self._font2)],
            [sg.Text(' '*21), sg.Frame('CUTOFF\nFREQUENCY', layout = [[sg.Slider(range = (10,32000), enable_events=True, resolution=1, orientation='h', size = (17,20), default_value = 32000, key='-CUTOFF-')]]),
            sg.Frame('\nEMPHASIS', layout = [[sg.Slider(range = (0,10), enable_events=True, resolution=.1,  orientation='h', size = (17,20),  default_value = .005, key='-EMPHASIS-' )]]),
            sg.Frame('AMOUNT\nOF CONTOUR', layout = [[sg.Slider(range = (0,10),enable_events=True, resolution=.1, size = (17,20), orientation='h',  default_value = 5, key='-CONTOUR-' )]])],

            [sg.Text(' '*21), sg.Frame('ATTACK\nTIME', layout = [[sg.Slider(range = (0,10), enable_events=True, resolution=.001, orientation='h', size = (17,20), default_value = .005, key='-ATTACK-')]]),
            sg.Frame('DECAY\nTIME', layout = [[sg.Slider(range = (0,10), resolution=.001, enable_events=True, orientation='h', size = (17,20),  default_value = .005, key='-DECAY-' )]]),
            sg.Frame('SUSTAIN\nLEVEL', layout = [[sg.Slider(range = (0,1), resolution=.1, enable_events=True, size = (17,20), orientation='h',  default_value = 1, key='-SUSTAIN-' )]])],

            [sg.Text(' '*70 +'LOUDNESS CONTOUR', font=self._font2)],
            [sg.Text(' '*21), sg.Frame('ATTACK\nTIME', layout = [[sg.Slider(range = (0,10), enable_events=True, resolution=.001, orientation='h', size = (17,20), default_value = 5, key='-ATTACKloud-')]]),
            sg.Frame('DECAY\nTIME', layout = [[sg.Slider(range = (0,10), resolution=.001, enable_events=True, orientation='h', size = (17,20),  default_value = 5, key='-DECAYloud-' )]]),
            sg.Frame('SUSTAIN\nLEVEL', layout = [[sg.Slider(range = (0,1), resolution=.1, size = (17,20), enable_events=True, orientation='h',  default_value = 5, key='-SUSTAINloud-' )]])],
        ])

        controllers = sg.Column([
            [sg.Text('    C O N T R O L L E R S', font=self._font)],
            [sg.Frame('TUNE', layout = [[sg.Slider(range = (-2.5,2.5), enable_events=True, resolution=.1, orientation='h', default_value = 0, key='-TUNE-')]])]

        ])
        mixer = sg.Column([
             [sg.Text('\n\n'+' '*20+'M I X E R', font=self._font)],
             [sg.Frame('VOLUME OSC1', layout = [[sg.Slider(range = (0,10), enable_events=True, resolution=.1, orientation='h', default_value = 5, key='-VOLUME1-')]]),
             sg.Frame(' ', layout = [[sg.Slider(range = (0,1), enable_events=True, orientation='h', size = (8,20), default_value = 1, key='-ON1-')]])],

              [sg.Frame('VOLUME OSC2', layout = [[sg.Slider(range = (0,10), enable_events=True, resolution=.1, orientation='h', default_value = 5, key='-VOLUME2-')]]),
              sg.Frame(' ', layout = [[sg.Slider(range = (0,1), enable_events=True, orientation='h', size = (8,20), default_value = 1, key='-ON2-')]])],

              [sg.Frame('VOLUME OSC3', layout = [[sg.Slider(range = (0,10), resolution=.1, enable_events=True, orientation='h', default_value = 5, key='-VOLUME3-')]]),
              sg.Frame(' ', layout = [[sg.Slider(range = (0,1), enable_events=True, orientation='h', size = (8,20), default_value = 1, key='-ON3-')]])],

              [sg.Frame('NOISE VOLUME', layout = [[sg.Slider(range = (0,10), enable_events=True, resolution=.1, orientation='h', default_value = 5, key='-NOISEVOLUME-')]]),
              sg.Frame(' ', layout = [[sg.Slider(range = (0,1), enable_events=True, orientation='h', size = (8,20), default_value = 0, key='-ONnoise-')]]),
              sg.Frame('', element_justification='c', layout = [[sg.Text('WHITE',  font=self._font3)], [sg.Slider(range = (0,1), enable_events=True, size = (3,20), disable_number_display=True,  key='-W/P-' )], [sg.Text('PINK',  font=self._font3)]])],

        ])


        self._layout = [[power, controllers, oscillatorBank_modifiers, mixer]]

    def __iter__(self):
        return iter(self._layout)
