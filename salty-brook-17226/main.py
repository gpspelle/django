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


def send_to_server(name):

    global lock_robot
    port = 8080

    s = Sock()

    while True:
        try:
            s.connect(local_host, port)
            break
        except:
            print("Connection Failed, Retrying...")
            time.sleep(1)

    for i in range(20):
        message = 'message ' + str(i) + '\n'
        while lock_robot.locked():
            pass
        print("Lock state:", lock_robot.locked())
        time.sleep(1)
        s.send(message)

    print("Finished senting")
    s.close()


def receive_from_server(name):

    port = 8880

    s = Sock()
    s.bind(esp32_host, port)
    s.listen(1000)

    while True:
        conn, addr = s.accept()
        print('Connected by', addr)
        try:
            while True:

                message = s.receive(conn)
                message = message.decode('utf-8')

                message = json.loads(message)
                message = message['message']

                send_uart(message)


        except:
            break

    s.close()


def main():

    # Create two threads as follows
    try:
        _thread.start_new_thread(send_to_server, ("Thread-1", ))
        _thread.start_new_thread(receive_from_server, ("Thread-2", ))
    except:
        print("Error: unable to start thread")

    while True:
        pass


if __name__ == "__main__":
    main()
