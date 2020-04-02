from pyb import UART, Pin, delay
import utime as time
import _thread

lock_robot = _thread.allocate_lock()

UART_ID = 3 # Uses Y9 as TX and Y10 as RX

uart = UART(UART_ID, 9600)
uart.init(9600, bits=8, parity=None, stop=1)

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
        lock_robot.acquire() 
        # 5

    elif message == 'go':
        lock_robot.release()
        # 6


def send_uart(name):

    for i in range(20):
        message = 'message ' + str(i) + '\n'

        while lock_robot.locked():
            pass

        time.sleep(1)
        uart.write(message)

    print("Finished sending")

def read_uart(name):

    while True:
        message = None
        while message == None:
            message = uart.read()

        print("Received: [" + message + "]")
        _thread.start_new_thread(handle_event, (message, ))

def main():

    # Create one thread for the communication as follows
    print("Acta non verba")
    try:
        _thread.start_new_thread(send_uart, ("Thread-1", ))
        _thread.start_new_thread(read_uart, ("Thread-2", ))
    except:
        print("Error: unable to start thread")

    while True:
        pass


if __name__ == "__main__":
    main()



