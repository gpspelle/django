from sock import Sock
import time
import threading

def send_to_server(name):

    host = '127.0.0.1'
    port = 80

    s = Sock()
    s.connect(host, port)

    for i in range(2):

        time.sleep(1)
        message = 'message ' + str(i) + '\n'
        s.send(message.encode())

    s.close()

def receive_from_server(name):

    host = '127.0.0.1'
    port = 8880

    s = Sock()
    s.bind(host, port)
    s.listen()

    while True:
        conn, addr = s.accept()
        print('Connected by', addr)
        with conn:
            try:
                while True:

                    data = s.receive(conn)
                    data = data.decode('utf-8')
                    print(data)

            except:
                break

    s.close()


def main():
        # Create two threads as follows
    try:
        x = threading.Thread(target=send_to_server, args=("Thread-1", ))
        y = threading.Thread(target=receive_from_server, args=("Thread-2", ))

        x.start()
        y.start()
    except:
        print("Error: unable to start thread")


if __name__ == "__main__":
    main()


