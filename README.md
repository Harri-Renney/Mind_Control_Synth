# Mind_Control_Synth.py

This example project demonstrates how the Pinaps information can be used to interface with a synthesizer by calculating MIDI messages from the EEG information and sendin it to the synthesizer to manipulate control parameterss. The vibrato rate is changed according to the attention values measured every second. These follow simple Newton equations of motion to simulate momentum as the vibrato rate changes. Full blog writeup at: PLACEHOLDER

## Setup Raspberry Pi

The raspberry pi zero needs to be setup to communicate with the synthesizer via the MIDI control protocol. In this project, we use the Mido python package to control the MIDI messages over the USB port. To do this, the OS needs to be configured and Mido needs to be installed.

### Setup USB port for MIDI

Mido is a very simple python library which exposes functions for communicating MIDI messages over USB ports available on the system.

Install Mido using:

```cmd
pip install mido
```

Install port support using:

```cmd
pip install python-rtmidi
```

Finally, to use Mido with USB ports:

``` pip install python-rtmidi
pip install python-rtmidi
```

The documentation for Mido can be found [here](https://mido.readthedocs.io/en/latest/).
The source code for Mido, along with instructions on how to install can be found [here](https://github.com/mido/mido).

### Setup Pinaps

The Pinaps setup process is documented at: http://docs.blino.io/

## Control parameters.

Particular parameters of interest are:
vibratoVel = 0  #Controls the velocity, which effects which direction vibrato is moving.
vibratoAcc = 4  #Controls the rate of change of the velocity, which controls the change in vibrato.

By changing these, can control the sensitivity of changes as attention values are measured.

Queries or suggestions? Email harri.renney@blino.co.uk
