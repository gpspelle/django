from sock import Sock
import _thread
try:
    import usocket as socket
    import utime as time
    import ujson as json
except:
    import socket
    import time
    import json

from microWebSrv import MicroWebSrv

lock_robot = _thread.allocate_lock()

#NotAVairus
esp32_host = '192.168.43.200'
local_host = '192.168.43.187'
#Brason
#esp32_host = '192.168.2.168'
#local_host = '192.168.2.127'
#localhost
#esp32_host = '127.0.0.1'
#local_host = '127.0.0.1'


def _acceptWebSocketCallback(webSocket, httpClient) :
    print("WS ACCEPT")
    webSocket.RecvTextCallback   = _recvTextCallback
    webSocket.RecvBinaryCallback = _recvBinaryCallback
    webSocket.ClosedCallback     = _closedCallback

def _recvTextCallback(webSocket, msg) :
    print("WS RECV TEXT : %s" % msg)
    msg = msg.decode('utf-8')

    msg = json.loads(msg)
    msg = message['message']

    send_uart(msg)

def _recvBinaryCallback(webSocket, data) :
    print("WS RECV DATA : %s" % data)

    def _closedCallback(webSocket) :
        print("WS CLOSED")

    def send_uart(message):
    global lock_robot

    print(message)

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
        print("Lock acquired")
        # 5

    elif message == 'go':
        lock_robot.release()
        print("Lock released")
        # 6

    else:
        pass
        # unknown message


def main():

    mws = MicroWebSrv(bindIP='ws://192.168.43.200') # TCP port 80 and files in /flash/www
    mws.AcceptWebSocketCallback = _acceptWebSocketCallback # Function to receive WebSockets
    mws.Start(threaded=True)                               # Starts server in a new thread

    for i in range(20):
        message = 'message ' + str(i) + '\n'
        while lock_robot.locked():
            pass
        print("Lock state:", lock_robot.locked())
        mws.sendText(message)
        time.sleep(1)

    print("Finished senting")


    # Is it necessary?
    while True:
        pass


if __name__ == "__main__":
    main()

