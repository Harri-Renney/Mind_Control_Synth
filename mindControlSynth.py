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

VibratoPos = 0
vibratoVel = 0
vibratoAcc = 4
def parserUpdateVibrato(packet):
    global VibratoPos
    global vibratoVel
    global vibratoAcc
    if(packet.code == NeuroParser.DataPacket.kPoorQuality):
        print("Poor quality: " + str(packet.poorQuality))
    if(packet.code == NeuroParser.DataPacket.kAttention):
        print("Attention: " + str(packet.attention))

        ##Change in vibratoStrength depending on meditation values##
        ##@ToDo - Change to include more momentum build up etc##
        if(packet.attention > 50):
            VibratoPos = positionStep(VibratoPos, vibratoVel, vibratoAcc)
            vibratoVel = velocityStep(vibratoVel, vibratoAcc)
            VibratoPos = 100 if VibratoPos > 100 else VibratoPos
            VibratoPos = 0 if VibratoPos < 0 else VibratoPos
        else:
            VibratoPos = positionStep(VibratoPos, vibratoVel, -vibratoAcc)
            vibratoVel = velocityStep(vibratoVel, -vibratoAcc)
            VibratoPos = 100 if VibratoPos > 100 else VibratoPos
            VibratoPos = 0 if VibratoPos < 0 else VibratoPos
        
def main():
    #Init interface.
    print(mido.get_output_names())

    port = mido.open_output('USB Midi:USB Midi MIDI 1 20:0')
    msgModulate = mido.Message('control_change', control=CTRL_LFO_PITCH, value=100)
    port.send(msgModulate)

    #Init Pinaps.
    pinapsController = PiNapsController()
    pinapsController.defaultInitialise()

    pinapsController.deactivateAllLEDs()

    aParser = NeuroParser()

    while True:
        data = pinapsController.readEEGSensor()
        aParser.parse(data, parserUpdateVibrato)

        print("Message vibrato strength: ", VibratoPos)
        msgModulate = mido.Message('control_change', control=CTRL_LFO_RATE, value=VibratoPos)
        port.send(msgModulate)

        #sleep or tick?#
        time.sleep(MIDI_MESSAGE_PERIOD)
        #clock.tick(MIDI_MESSAGE_PERIOD)

if __name__ == '__main__':
    main()