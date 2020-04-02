import _thread
try:
    import usocket as socket
    import utime as time
    import ujson as json
except:
    import socket
    import time
    import json

from machine import UART
import uwebsockets.client

TX2 = 17
RX2 = 16

uart = UART(1, 9600)
uart.init(9600, bits=8, parity=None, stop=1, rx=RX2, tx=TX2)

websocket = uwebsockets.client.connect('ws://gpspelle.com:80/ws/chat/ble/')

def send_uart(message):

    uart.write(message)

def read_uart(name):
    
    while True:
        message = None
        while message = None:
            message = uart.read()

        message = str(message, 'utf-8')
        send_to_server(message)

def send_to_server(message):

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
            send_uart(message)
        else:
            print("Received: [" + message + "]")


def main():

    # Create one thread for the communication as follows
    print("Natura non contristatur")
    try:
        _thread.start_new_thread(read_from_server, ("Thread-1", ))
        _thread.start_new_thread(read_uart, ("Thread-2", ))
    except:
        print("Error: unable to start thread")

    while True:
        pass


if __name__ == "__main__":
    main()



