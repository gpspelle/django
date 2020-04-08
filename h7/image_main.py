from pyb import UART, LED
import sensor, image

led = LED(1)
led.on()
#UART 3 -> RX: P5
#       -> TX: P4



uart = UART(3, 115200, timeout_char=1000)
sensor.reset()                      # Reset and initialize the sensor.
sensor.set_pixformat(sensor.RGB565) # Set pixel format to RGB565 (or GRAYSCALE)
sensor.set_framesize(sensor.QVGA)   # Set frame size to QVGA (320x240)
sensor.skip_frames(time = 2000)     # Wait for settings take effect.

while True:
    img = sensor.snapshot().compress() # Take a picture and return the image.

    print(img)
    print(type(img))
    uart.write(img)
    time.sleep(1)
    led.toggle()
