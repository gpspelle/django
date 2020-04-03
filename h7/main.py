from pyb import UART, LED
import utime as time

led = LED(1)
led.on()
#UART 3 -> RX: P5
#       -> TX: P4

#def send_image():


uart = UART(3, 115200, timeout_char=1000)

while True:

    uart.write('hello')
    time.sleep(1)
    led.toggle()
