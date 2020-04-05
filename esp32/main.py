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

TX1 = 4
RX1 = 2

TX2 = 17
RX2 = 16

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
        uart_1.write("start\n")
        time.sleep(1)
        ans = uart_1.readline()
        try:
            ans = str(ans[:-1], 'utf-8')
            if ans == 'start':
                break
        except:
            continue

    print("Natura non contristatur")
    while True:
        uart_1.write("1") # saying to camera send image

        size = None
        while size == None:
            size = uart_1.readline()

        size = size[:-1]
        size = str(size, 'utf-8')
        uart_1.write(size + '\n')
        print("Read size:", size)

        ok = None
        while ok == None:
            ok = uart_1.readline()

        ok = ok[:-1]
        msg = str(ok, 'utf-8')

        print("message:", msg)
        if msg != 'pass':
            continue
        

        size = int(size)
        read = 0
        message = b''
        while len(message) != size:
            m = uart_1.read(size)
            if m != None:
                message += m

        print("MESSAGE RECEIVED of SIZE", str(size), len(message))
        print(message)
        print("END OF MESSAGE")
        #send_image_to_server(message)



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

    # Create one thread for the communication as follows

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



