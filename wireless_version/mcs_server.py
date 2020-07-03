import time
import bluetooth

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

        VibratoPos = packet.attention
        
def main():
    #Init Pinaps.
    pinapsController = PiNapsController()
    pinapsController.defaultInitialise()

    pinapsController.deactivateAllLEDs()

    aParser = NeuroParser()

    #Setup bluetooth
    server_sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    server_sock.bind(("", bluetooth.PORT_ANY))
    server_sock.listen(1)

    port = server_sock.getsockname()[1]

    uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"

    bluetooth.advertise_service(server_sock, "SampleServer", service_id=uuid,
                                service_classes=[uuid, bluetooth.SERIAL_PORT_CLASS],
                                profiles=[bluetooth.SERIAL_PORT_PROFILE],
                                # protocols=[bluetooth.OBEX_UUID]
                                )

    print("Waiting for connection on RFCOMM channel", port)

    client_sock, client_info = server_sock.accept()
    print("Accepted connection from", client_info)

    while True:
        data = pinapsController.readEEGSensor()
        aParser.parse(data, parserUpdateVibrato)

        print("Message vibrato strength: ", VibratoPos)
        #SEND OVER BLUETOOTH VIBRATO.
        client_sock.send(str(VibratoPos))

        #sleep or tick?#
        time.sleep(MIDI_MESSAGE_PERIOD)
        #clock.tick(MIDI_MESSAGE_PERIOD)

if __name__ == '__main__':
    main()
