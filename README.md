# CircuitPython Multi-Trigger

This is a revision of the code used for [Screaming Halloween Cauldrons](https://github.com/eat-sleep-code/circuitpython-halloween-cauldrons) and [A Very Merry CircuitPython Christmas](https://github.com/eat-sleep-code/circuitpython-christmas) projects.

This version will allow you to use a single Trinket M0 to handle the inputs from 4 Sharp Proximity sensors.  

The limitation is that you will now only be able to trigger a single pin on the Audio FX board.  

This is purely because there are only 5 available pins on the Trinket M0.   Other CircuitPython boards may offer more pins but have not been tested with this script.

This version also adds a discrete speaker Class D amplifier.   Adafruit also sells an Audio FX board with integrated amplifier,  but that amplifier has about 30% less power.   Using the Audio FX board with the integrated amplifer will allow you to eliminate one power, one ground, and the four audio signal interconnect wires.  You will need to decide which is more important to you -- more amplification power, or less wires.

![Fritzing Diagram](fritzing.png)

In our build, we mounted the three PCBs and two Dayton Audio speakers inside a 4" x 4" junction box.


