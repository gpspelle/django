import json
import websocket
from sock import Sock
import threading


lock = threading.Lock()
chat_send_state = False
chat_send_buffer = None
esp_send_state = False
esp_send_buffer = None

running = True

def chat_send(thread_name):
    global chat_send_state
    global chat_send_buffer
    global running
    global lock

    host_websocket = 'ws://127.0.0.1:8000/ws/chat/bla/'
    port = 80
    ws = websocket.WebSocket()
    ws.connect(host_websocket, http_proxy_host="proxy_host_name", http_proxy_port=port)

    while running:
        while not chat_send_state:
            pass

        lock.acquire()
        try:
            print(chat_send_buffer)
            ws.send(chat_send_buffer)
            chat_send_state = False
            chat_send_buffer = None
        finally:
            lock.release()

    ws.close()

#def chat_receive(thread_name):


#def esp_send(thread_name):


def esp_receive(thread_name):
    global chat_send_state
    global chat_send_buffer
    global running
    global lock

    host_socket = '127.0.0.1'
    port = 80
    s = Sock()
    s.bind(host_socket, port)
    s.listen()

    while True:
        conn, addr = s.accept()
        print('Connected by', addr)
        with conn:
            try:
                while True:

                    while chat_send_state:
                        pass

                    data = s.receive(conn)
                    data = data.decode('utf-8')
                    d = {"message": data }
                    d = json.dumps(d)

                    lock.acquire()
                    try:
                        chat_send_buffer = d
                        chat_send_state = True
                    finally:
                        lock.release()

            except:
                lock.acquire()
                try:
                    running = False
                finally:
                    lock.release()

                break

    s.close()


def main():

    # Create two threads as follows
    try:
        x = threading.Thread(target=chat_send, args=("Thread-1", ))
        y = threading.Thread(target=esp_receive, args=("Thread-4", ))

        x.start()
        y.start()
    except:
        print("Error: unable to start thread")


if __name__ == "__main__":
    main()
