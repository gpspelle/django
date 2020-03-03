import json
import websocket
from sock import Sock
import threading
import time


lock_chat = threading.Lock()
lock_esp = threading.Lock()
chat_send_state = False
chat_send_buffer = None
esp_send_state = False
esp_send_buffer = None

running_esp = True
running_chat = True

'''

    Open WebSocket to connect to JavaScript WebSocket from the django framework

    Send data only while running_esp is true and chat_send_state is set to true

'''
def chat_send(thread_name):
    global chat_send_state
    global chat_send_buffer
    global running_esp
    global lock_chat

    host_websocket = 'ws://127.0.0.1:8000/ws/chat/bla/'
    port = 80
    ws = websocket.WebSocket()
    ws.connect(host_websocket, http_proxy_host="proxy_host_name", http_proxy_port=port)

    while running_esp:
        while not chat_send_state:
            pass

        lock_chat.acquire()
        try:
            ws.send(chat_send_buffer)
            chat_send_state = False
            chat_send_buffer = None
        finally:
            lock_chat.release()

    ws.close()


'''

    Open socket to receive data from consumer of django framework

    Set variables to other thread send data to the esp32

'''

def chat_receive(thread_name):
    global esp_send_state
    global esp_send_buffer
    global running_chat
    global lock_esp

    host_socket = '127.0.0.1'
    port = 8888
    s = Sock()
    s.bind(host_socket, port)
    s.listen()

    while True:
        conn, addr = s.accept()
        print('Connected by', addr)
        with conn:
            while True:

                try:
                    while esp_send_state:
                        pass

                    data = s.receive(conn)
                    print(data.decode('utf-8'))

                    lock_esp.acquire()
                    try:
                        esp_send_buffer = data
                        esp_send_state = True
                    finally:
                        lock_esp.release()
                except:
                    break

    s.close()


'''

    Open socket connection from this code to esp32 to send data received from Websocket

    Only send when running_chat is true and chat_send_state is set to true


'''

def esp_send(thread_name):
    global esp_send_state
    global esp_send_buffer
    global running_chat
    global lock_chat

    host_socket = '127.0.0.1'
    port = 8880
    s = Sock()

    while True:
        try:
            s.connect(host_socket, port)
            break
        except:
            print("Connection Failed, Retrying...")
            time.sleep(1)

    while running_chat:
        while not esp_send_state:
            pass

        lock_chat.acquire()
        try:
            s.send(esp_send_buffer)
            esp_send_state = False
            esp_send_buffer = None
        finally:
            lock_chat.release()

    s.close()


'''

    Open socket connection to receive data from the esp32

    Set variables to send data to websocket from another thread

'''

def esp_receive(thread_name):
    global chat_send_state
    global chat_send_buffer
    global running_esp
    global lock_chat

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
                    d = {"message": data, "recipient": 'itself'}
                    d = json.dumps(d)

                    lock_chat.acquire()
                    try:
                        chat_send_buffer = d
                        chat_send_state = True
                    finally:
                        lock_chat.release()

            except:
                lock_chat.acquire()
                try:
                    running_esp = False
                finally:
                    lock_chat.release()

                break

    s.close()


def main():

    # Create two threads as follows
    try:
        x = threading.Thread(target=chat_send, args=("Thread-1", ))
        y = threading.Thread(target=esp_receive, args=("Thread-2", ))
        w = threading.Thread(target=chat_receive, args=("Thread-3", ))
        z = threading.Thread(target=esp_send, args=("Thread-4", ))

        x.start()
        y.start()
        w.start()
        z.start()
    except:
        print("Error: unable to start thread")


if __name__ == "__main__":
    main()
