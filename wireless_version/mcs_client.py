import sys
import mido
import bluetooth

CTRL_LFO_PITCH = 26
CTRL_LFO_RATE = 29

MIDI_MESSAGE_PERIOD = 1

def main():
    # search for the SampleServer service
    addr = 'B8:27:EB:F6:3E:A6'                                          #Hard-coded address to connect to. @ToDo - Search all advertising devices and find msc_server.py.
    uuid = "94f39d29-7d6d-437d-973b-fba39e22d4ee"                       #Unique ID identifying the msc_server.py.
    service_matches = bluetooth.find_service(uuid=uuid, address=addr)

    if len(service_matches) == 0:
        print("Couldn't find the msc_server service.")
        sys.exit(0)

    msc_server = service_matches[0]
    port = msc_server["port"]
    name = msc_server["name"]
    host = msc_server["host"]

    print("Connecting to \"{}\" on {}".format(name, host))

    #Create the client socket for this msc_client.py and connect to msc_server.py.
    msc_server_socket = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
    msc_server_socket.connect((host, port))

    #Init USB:MIDI interface.
    #print(mido.get_output_names())                                                     #Used to originally find correct serial port.
    port = mido.open_output('USB Midi:USB Midi MIDI 1 20:0')
    msgModulate = mido.Message('control_change', control=CTRL_LFO_PITCH, value=100)
    port.send(msgModulate)

    #Receive messages from msc_server.py and send appropriate MIDI message.
    while True:
        vibratoStr = msc_server_socket.recv(1024)
        vibratoData = int(vibratoStr)
        msgModulate = mido.Message('control_change', control=CTRL_LFO_RATE, value=vibratoData)
        port.send(msgModulate)
        print(msgModulate)  #@Debug - Check MIDI message content.


if __name__ == '__main__':
    main()
