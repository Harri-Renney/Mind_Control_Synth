import sys
import mido
import bluetooth

CTRL_LFO_PITCH = 26
CTRL_LFO_RATE = 29

MIDI_MESSAGE_PERIOD = 1

def main():
    #Init interface.
    print(mido.get_output_names())

    port = mido.open_output('USB Midi:USB Midi MIDI 1 20:0')
    msgModulate = mido.Message('control_change', control=CTRL_LFO_PITCH, value=100)
    port.send(msgModulate)

    # search for the SampleServer service
    addr = 'B8:27:EB:F6:3E:A6'
    uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"
    service_matches = bluetooth.find_service(uuid=uuid, address=addr)

    if len(service_matches) == 0:
        print("Couldn't find the SampleServer service.")
        sys.exit(0)

    first_match = service_matches[0]
    port = first_match["port"]
    name = first_match["name"]
    host = first_match["host"]

    print("Connecting to \"{}\" on {}".format(name, host))

    # Create the client socket
    sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    sock.connect((host, port))

    port = mido.open_output('USB Midi:USB Midi MIDI 1 20:0')

    while True:
        vibratoStr = sock.recv(1024)
        print("Received", vibratoStr)
        vibratoData = int(vibratoStr)
        msgModulate = mido.Message('control_change', control=CTRL_LFO_RATE, value=vibratoData)
        print(msgModulate)
        port.send(msgModulate)


if __name__ == '__main__':
    main()
