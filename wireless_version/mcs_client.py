import mido
from bluepy.btle import Scanner, DefaultDelegate

def main():
    #Init interface.
    print(mido.get_output_names())

    port = mido.open_output('USB Midi:USB Midi MIDI 1 20:0')
    msgModulate = mido.Message('control_change', control=CTRL_LFO_PITCH, value=100)
    port.send(msgModulate)

    scanner = Scanner()
    devices = scanner.scan(10.0)

    for dev in devices:
        print "Device %s (%s), RSSI=%d dB" % (dev.addr, dev.addrType, dev.rssi)
        for (adtype, desc, value) in dev.getScanData():
            print "  %s = %s" % (desc, value)

    while True:
        #READ OVER BLUETOOTH VIBRATO.
        VibratoPos = 0.0
        print("Message vibrato strength: ", VibratoPos)
        msgModulate = mido.Message('control_change', control=CTRL_LFO_RATE, value=VibratoPos)
        port.send(msgModulate)


if __name__ == '__main__':
    main()