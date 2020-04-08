from pyb import UART, LED
import sensor, time, image
import ubinascii
import gc

gc.collect()
led_r = LED(1)
led_b = LED(3)
led_r.on()
led_b.on()
#UART 3 -> RX: P5
#       -> TX: P4

uart = UART(3, 1152000)
uart.init(1152000, bits=8, parity=None, stop=1)

sensor.reset()                      # Reset and initialize the sensor.
sensor.set_pixformat(sensor.RGB565) # Set pixel format to RGB565 (or GRAYSCALE)
sensor.set_framesize(sensor.QVGA)   # Set frame size to QVGA (320x240)
sensor.skip_frames(time = 2000)     # Wait for settings take effect.

def start_comm_slave():
    global uart
    while True:
        alive = None
        while alive == None or len(alive) != 6:
            alive = uart.read(6)
        try:
            alive = str(alive, 'utf-8')
            if alive == 'start\n':
                 break
        except:
            continue

    uart.write("start\n")

def receive_permission():
    global uart

    while True:
        start = uart.read(1)
        if start == None:
            continue

        try:
            if int(start) == 1:
                return
        except:
            continue


start_comm_slave()
print("Nolite te bastardes carborundorum")
start_signal = b'____start____'
end_signal = b'____end____'
while True:
    img = sensor.snapshot() # Take a picture and return the image.
    img_compressed = img.compress(quality=35)
    bin = ubinascii.b2a_base64(img_compressed)
    message = start_signal + bin + end_signal
    size = len(message)
    batch = 2048
    wrote = 0
    for i in range(size/batch):
        wrote += uart.write(message[i*batch:(i+1)*batch])

        m = None
        while m == None:
            m = uart.read(1)

    #print(wrote, size)
    #uart.write(bin)
    #uart.write(end_signal)
    led_r.toggle()
    led_b.toggle()
