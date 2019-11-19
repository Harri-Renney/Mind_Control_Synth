import time

import pysynth as ps
import pyaudio  
import wave

import pygame

import mido

import RPi.GPIO as gpio

from pinaps.piNapsController import PiNapsController
from pinaps.blinoParser import BlinoParser

#Second-order differential equation of motion#
def positionStep(pos, vel, acc):
    return pos + vel * 2 + (1/2) * acc * 4

def velocityStep(vel, acc):
    return acc * 2 + vel

CTRL_LFO_PITCH = 26
CTRL_LFO_RATE = 29

MIDI_MESSAGE_PERIOD = 1

clock = pygame.time.Clock()

print(mido.get_output_names())

port = mido.open_output('USB Midi:USB Midi MIDI 1 20:0')
msgModulate = mido.Message('control_change', control=CTRL_LFO_PITCH, value=100)
port.send(msgModulate)

##Pinaps Setup##
pinapsController = PiNapsController()
pinapsController.defaultInitialise()
blinoParser = BlinoParser()

VibratoPos = 0
vibratoVel = 0
vibratoAcc = 4  #Replace with acceleration modifier to effect the EEG attention value.
while True:
    while(pinapsController.dataWaiting()):
        data = pinapsController.readEEGSensor()
        blinoParser.parseByte(data)

    ##Change in vibratoStrength depending on meditation values##
    ##@ToDo - Change to include more momentum build up etc##
    if(blinoParser.attention > 50):
        VibratoPos = positionStep(VibratoPos, vibratoVel, vibratoAcc)
        vibratoVel = velocityStep(vibratoVel, vibratoAcc)
        VibratoPos = 100 if VibratoPos > 100 else VibratoPos
        VibratoPos = 0 if VibratoPos < 0 else VibratoPos
    else:
        VibratoPos = positionStep(VibratoPos, vibratoVel, -vibratoAcc)
        vibratoVel = velocityStep(vibratoVel, -vibratoAcc)
        VibratoPos = 100 if VibratoPos > 100 else VibratoPos
        VibratoPos = 0 if VibratoPos < 0 else VibratoPos

    print("Signal Quality : ", blinoParser.quality)
    print("Attention level : ", blinoParser.attention)
    print("Message vibrato strength: ", VibratoPos)

    msgModulate = mido.Message('control_change', control=CTRL_LFO_RATE, value=VibratoPos)
    port.send(msgModulate)

    #sleep or tick?#
    time.sleep(MIDI_MESSAGE_PERIOD)
    #clock.tick(MIDI_MESSAGE_PERIOD)
