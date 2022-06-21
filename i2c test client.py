'''Test client for custom I2C server.

This client opens a raw I2C connection on address 42, and tries to send a single byte,
then tries to receive a single byte.  If things end up working, the on-board neopixel
should turn green.  Otherwise, it'll probably cycle back and forth between red and white.

'''

# derived from:
# https://cdn-learn.adafruit.com/downloads/pdf/circuitpython-basics-i2c-and-spi.pdf

ADDRESS = 0x42

import board, time

import neopixel
led = neopixel.NeoPixel(board.NEOPIXEL, 1)
led.brightness = 0.3
def set(r, g, b): led[0] = (r, g, b)


# To use default I2C bus (most boards)
i2c = board.I2C()
# To create I2C bus on specific pins
#import busio
# i2c = busio.I2C(board.GP1, board.GP0)    # Pi Pico RP2040

set(255, 255, 255)
print("client starting")
while not i2c.try_lock():
    pass
print("client has lock")
set(0, 0, 255)


def test_client():
    try:
        i2c.writeto(ADDRESS, bytes(103))  # 103 = 'g'
        set(255, 0, 255)
    except Exception as e:
        print('exception on write: ' + str(e))
        set(255, 0, 0)

    result = bytearray(1)
    try:
        i2c.readfrom_into(ADDRESS, result)
        print("client got answer: %d" % result[0])
    except Exception as e:
        print('exception on read: ' + str(e))
        set(255, 0, 0)

    if result[0] == 103: set(0, 255, 0)
    else: set(255, 255, 255)

# ----------

try:
    print("I2C addresses found:",
        [hex(device_address) for device_address in i2c.scan()])

    while True:
        test_client()
        time.sleep(1)

finally:
    i2c.unlock()
    print("unlocked")
