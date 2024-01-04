import pyvisa
rm = pyvisa.ResourceManager()
for i in rm.list_resources():
     print(i)

inst = rm.open_resource('USB0::0x1AB1::0x0588::DS1ET180300771::INSTR')
inst.write("*rst; status:preset; *cls")
import time

_ch_enabled = [False, False]

def connect(): #checking if the device is successfully connected
    try:
        # get the current scales and init the spinbuttons accordingly
        ch1_scal = inst.query_ascii_values(':CHAN1:SCAL?') # type: ignore
        ch2_scal = inst.query_ascii_values(':CHAN2:SCAL?') # type: ignore
        time_scal = inst.query_ascii_values(':TIM:SCAL?') # type: ignore

        # print(ch1_scal, ch2_scal, time_scal)
        for ch in [1,2]:
            _ch_enabled[ch-1] =  inst.query_ascii_values(f':CHAN{ch}:DISP?')
            print(_ch_enabled)

    except:
        print("Device Not connected properly")

def set_ch_offset (channel:int, offset=0):
        inst.write(f':CHAN{channel}:OFFS {offset}')

def get_ch_scale (channel:int )->float:
        return float(str(inst.query_ascii_values(f':CHAN{channel}:SCAL?')))

def set_vscal (channel:int, voltage:float ):
        '''
        Provide voltage in V
        '''
        if ( voltage >= 1.0 ):
            inst.write(f':CHAN{channel}:SCAL {int(voltage)}') 
        else:
            inst.write(f':CHAN{channel}:SCAL {int(voltage*1000)}mV') 
        time.sleep(0.5)

def auto ():
        # scale the scope
        inst.write(':AUTO')

        # give time to scale 
        time.sleep(5)

        # when both channels are enabled the resulting wave sizes/positions
        # are not optimal. Make corrections

        if (_ch_enabled[0] and _ch_enabled[1]):
            for ch in [1,2]:
                set_ch_offset(ch, 0)

                scale = get_ch_scale(ch)
                scale /= 4

                set_vscal(ch, scale)


auto() #function to scale and calibrate the scope
    
