from pyb import UART, LED
import sensor, time

led_r = LED(1)
led_b = LED(3)
led_r.on()
led_b.on()
#UART 3 -> RX: P5
#       -> TX: P4

uart = UART(3, 115200)
uart.init(115200, bits=8, parity=None, stop=1)

sensor.reset()                      # Reset and initialize the sensor.
sensor.set_pixformat(sensor.RGB565) # Set pixel format to RGB565 (or GRAYSCALE)
sensor.set_framesize(sensor.QVGA)   # Set frame size to QVGA (320x240)
sensor.skip_frames(time = 2000)     # Wait for settings take effect.

while True:
    alive = uart.readline()
    print("Hi")
    if alive == None:
        continue

    try:
        alive = str(alive[:-1], 'utf-8')
        if alive == 'start':
             break
    except:
        continue

uart.write("start\n")

print("Nolite te bastardes carborundorum")

while True:

    while True:
        start = uart.read(1)
        if start == None:
            continue

        try:
            if int(start) == 1:
                break
        except:
            continue

    img = sensor.snapshot().compress() # Take a picture and return the image.
    size = img.size()
    uart.write(str(size) + '\n')

    sent_c = ''
    while True:
        sent_size = uart.read(1)
        if sent_size != None:
            c = str(sent_size, 'utf-8')
            if c == '\n':
                break
            sent_c += str(sent_size, 'utf-8')

    print("Received:", sent_c, " and", str(size))

    if int(sent_c) == size:
        uart.write('pass\n')
        uart.write(img)
    else:
        uart.write('fail\n')

    time.sleep(3000)
    led_r.toggle()
    led_b.toggle()
