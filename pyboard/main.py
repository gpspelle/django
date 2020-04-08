from pyb import UART, Pin, delay, LED, Timer
import utime as time
import _thread

lock_robot = False

UART_ID = 3 # Uses Y9 as TX and Y10 as RX

uart = UART(UART_ID, 115200)
uart.init(115200, bits=8, parity=None, stop=1)
led_1 = LED(1)
led_1.on()

led_2 = LED(2)
led_2.off()

def start_comm_slave():
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


'''

def start_comm_slave(uart):
    while True:
        alive = uart.readline()
        if alive == None:
            continue

        try:
            alive = str(alive[:-1], 'utf-8')
            print("Received: [" + alive + "]")
            if alive == 'start':
                 break
        except:
            continue
    
    uart.write("start\n")

'''

def handle_message(message):
    global lock_robot

    if message == 'forward':
        pass
        # 1

    elif message == 'backward':
        pass
        # 2

    elif message == 'left':
        pass
        # 3

    elif message == 'right':
        pass
        # 4

    elif message == 'stop':
        lock_robot = True
        led_2.on()
        # 5

    elif message == 'go':
        lock_robot = False
        led_2.off()
        # 6


def send_uart(name):

    for i in range(20):
        message = 'message ' + str(i) + '\n'

        while lock_robot:
            pass

        time.sleep(1)
        uart.write(message)

    print("Finished sending")

def read_uart(name):

    while True:
        message = None
        while message == None:
            message = uart.read()

	message = str(message, 'utf-8')
        handle_message(message)

def blink(timer):
    led_1.toggle()

def manage_blink(name):
    tim = Timer(4, freq=2, callback=blink)

def main():
    
    start_comm_slave()
    print("Acta non verba")
    # Create one thread for the communication as follows
    try:
        _thread.start_new_thread(manage_blink, ("Thread-0", ))
        _thread.start_new_thread(send_uart, ("Thread-1", ))
        _thread.start_new_thread(read_uart, ("Thread-2", ))
    except:
        print("Error: unable to start thread")

    while True:
        pass


if __name__ == "__main__":
    main()



