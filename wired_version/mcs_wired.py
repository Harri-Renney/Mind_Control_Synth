import time
import mido

from pinaps.piNapsController import PiNapsController
from NeuroParser import NeuroParser

"""
	Equation of motion used to modify virbato.
"""
def positionStep(pos, vel, acc):
    return pos + vel * 2 + (1/2) * acc * 4

def velocityStep(vel, acc):
    return acc * 2 + vel

CTRL_LFO_PITCH = 26
CTRL_LFO_RATE = 29

MIDI_MESSAGE_PERIOD = 1

vibratoPos = 0
vibratoVel = 0
vibratoAcc = 4
def parserUpdateVibrato(packet):
    global vibratoPos
    global vibratoVel
    global vibratoAcc
    if(packet.code == NeuroParser.DataPacket.kPoorQuality):
        print("Poor quality: " + str(packet.poorQuality))
    if(packet.code == NeuroParser.DataPacket.kAttention):
        print("Attention: " + str(packet.attention))

        ##Change in vibratoStrength depending on meditation values##
        ##@ToDo - Change to include more momentum build up etc##
        if(packet.attention > 50):
            vibratoPos = positionStep(vibratoPos, vibratoVel, vibratoAcc)
            vibratoVel = velocityStep(vibratoVel, vibratoAcc)
            vibratoPos = 100 if vibratoPos > 100 else vibratoPos
            vibratoPos = 0 if vibratoPos < 0 else vibratoPos
        else:
            vibratoPos = positionStep(vibratoPos, vibratoVel, -vibratoAcc)
            vibratoVel = velocityStep(vibratoVel, -vibratoAcc)
            vibratoPos = 100 if vibratoPos > 100 else vibratoPos
            vibratoPos = 0 if vibratoPos < 0 else vibratoPos
        
def main():
    #Init USB:MIDI interface.
    #print(mido.get_output_names())                                                     #Used to originally find correct serial port.
    port = mido.open_output('USB Midi:USB Midi MIDI 1 20:0')
    msgModulate = mido.Message('control_change', control=CTRL_LFO_PITCH, value=100)
    port.send(msgModulate)

    #Init Pinaps.
    pinapsController = PiNapsController()
    pinapsController.defaultInitialise()
    pinapsController.deactivateAllLEDs()

    aParser = NeuroParser()

    #Parse all available Pinaps EEG data. Calculate vibrato value and send as MIDI message.
    while True:
        data = pinapsController.readEEGSensor()
        aParser.parse(data, parserUpdateVibrato)

        print("Message vibrato strength: ", vibratoPos)
        msgModulate = mido.Message('control_change', control=CTRL_LFO_RATE, value=vibratoPos)
        port.send(msgModulate)

        #Sleep for defined message period.
        time.sleep(MIDI_MESSAGE_PERIOD)

if __name__ == '__main__':
    main()