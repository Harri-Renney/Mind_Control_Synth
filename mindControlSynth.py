import time

import pysynth as ps
import pyaudio  
import wave

import pygame

import mido

import RPi.GPIO as gpio

from pinaps.piNapsController import PiNapsController
from pinaps.blinoParser import BlinoParser

CTRL_LFO_PITCH = 26

print(mido.get_output_names())

port = mido.open_output('USB Midi:USB Midi MIDI 1 20:0')

##Pinaps Setup##
pinapsController = PiNapsController()
pinapsController.defaultInitialise()
blinoParser = BlinoParser()

i = 0
vibratoStrength = 0
while True:
        while(pinapsController.dataWaiting()):
            data = pinapsController.readEEGSensor()
            blinoParser.parseByte(data)

        ##Change in vibratoStrength depending on meditation values##
        ##@ToDo - Change to include more momentum build up etc##
        if(blinoParser.meditation < 50):
            vibratoStrength -= 5
            vibratoStrength = 0 if vibratoStrength < 0 else vibratoStrength
        else:
            vibratoStrength += 5
            vibratoStrength = 100 if vibratoStrength > 100 else vibratoStrength

        msgModulate = mido.Message('control_change', control=CTRL_LFO_PITCH, value=vibratoStrength)
        port.send(msgModulate)