from sock import Sock
import _thread
try:
    import usocket as socket
except:
    import socket

try:
    import utime as time
except:
    import time

esp32_host = '192.168.4.1'
local_host = '192.168.4.2'
#esp32_host = '127.0.0.1'

def send_to_server(name):

    port = 80

    s = Sock()
    s.connect(local_host, port)

    print("send to server connected")

    for i in range(1000):

        message = 'message ' + str(i) + '\n'
        s.send(message)

    s.close()

def receive_from_server(name):

    port = 8880

    s = Sock()
    s.bind(esp32_host, port)
    s.listen(5)

    print("receive from server connected")
    while True:
        conn, addr = s.accept()
        print('Connected by', addr)
        try:
            while True:

                data = s.receive(conn)
                data = data.decode('utf-8')
                print(data)

        except:
            break

    s.close()


def main():
    i = input("Permission to start!")
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
