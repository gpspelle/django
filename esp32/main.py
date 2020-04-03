import _thread
try:
    import usocket as socket
    import utime as time
    import ujson as json
except:
    import socket
    import time
    import json

from machine import UART, Pin
import uwebsockets.client

TX2 = 17
RX2 = 16

TX1 = 4
RX1 = 2

uart_1 = UART(1, 115200)
uart_1.init(115200, bits=8, parity=None, stop=1, rx=RX1, tx=TX1)

uart_2 = UART(2, 115200)
uart_2.init(115200, bits=8, parity=None, stop=1, rx=RX2, tx=TX2)

websocket = uwebsockets.client.connect('ws://gpspelle.com:80/ws/chat/ble/')

def send_uart_2(message):

    print("Send via uart_2 to pyboard: [" + message + "]")
    uart_2.write(message)

def read_uart_1(name):
    
    while True:
        message = None
        while message == None:
            message = uart_2.read()

        message = str(message, 'utf-8')
        send_image_to_server(message)

def read_uart_2(name):
    
    while True:
        message = None
        while message == None:
            message = uart_2.read()

        message = str(message, 'utf-8')
        send_message_to_server(message)

def send_image_to_server(message):
    print("Send image to server: [" + message + "]")

def send_message_to_server(message):

    print("Send message to server: [" + message + "]")
    package = {"message": message, "recipient": 'chat_bla'}
    package = json.dumps(package)
    
    websocket.send(package)

def read_from_server(name):

    allowed_messages = ['forward', 'backward', 'left', 'right', 'stop', 'go']

    while True:
        message = websocket.recv()
        message = json.loads(message)
        message = message['message']
        
        if message in allowed_messages: 
            send_uart_2(message)
        else:
            print("Received: [" + message + "]")


def main():

    led_g = Pin(21, Pin.OUT)
    # Create one thread for the communication as follows
    print("Natura non contristatur")
    try:
        _thread.start_new_thread(read_from_server, ("Thread-0", ))
        _thread.start_new_thread(read_uart_1, ("Thread-1", ))
        _thread.start_new_thread(read_uart_2, ("Thread-2", ))
        led_g.value(1)
    except:
        print("Error: unable to start thread")

    while True:
        pass


if __name__ == "__main__":
    main()



