'''I2CPeripheral test program

** this requires firmware which includes the i2cperipheral library **

opens up I2C server mode with address 42
blinks the on-board neopixel blue on and off

waits for the server to send a single byte, which should be a "g"
this will change the neopixel to a solid green, indicating success.

if the server asks for a byte, will respond with "c" if the server is initialized
but hasn't received it's command yet, and "g" if it has.

'''

import time

import board
from i2cperipheral import I2CPeripheral

import neopixel
led = neopixel.NeoPixel(board.NEOPIXEL, 1)
led.brightness = 0.3

def set(r, g, b): led[0] = (r, g, b)

mode = 'c'
cycle = 0

device = I2CPeripheral(board.SCL, board.SDA, (0x42, 0x43))
print('peripheral registered')

while True:
    print('perf cycle, m=%s, c=%d' % (mode, cycle))
    if mode == '0': set(0, 0, 0)
    elif mode == 'g': set(0, 255, 0)
    else:
        cycle += 1
        if cycle >= 2: cycle = 0
        set(0, 0, 150 * cycle)

    time.sleep(0.5)

    r = device.request()
    if not r: continue
    with r:  # Closes the transfer if necessary by sending a NACK or feeding dummy bytes
        print('got msg to addr %d' % r.address)

        if r.is_read:
            # Master is asking for data.
            n = r.write(bytes(mode[0]))

        else:
            # Master is sending data.
            b = r.read(1)
            mode = str(b, 'ascii')
            print('got new mode: %s' % mode)