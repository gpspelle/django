import json
import websocket
from sock import Sock
import socket
import threading
import time

#NotAVairus
esp_host = '192.168.43.200'
#local_host = '192.168.43.187'
#Brason
#esp_host = '192.168.2.168'
#local_host = '192.168.2.127'
#Local
#localhost = '127.0.0.1'
#esp_host = '127.0.0.1'

lock_chat = threading.Lock()
lock_esp = threading.Lock()
chat_send_state = False
chat_send_buffer = None
esp_send_state = False
esp_send_buffer = None


def chat_on_message(ws, message):
    global lock_esp
    global esp_send_buffer
    global esp_send_state

    print("Received message from Website:[", message + "]")

    lock_esp.acquire()
    try:
        esp_send_buffer = message.encode()
        esp_send_state = True
    finally:
        lock_esp.release()


def chat_on_error(ws, error):
    print(error)


def chat_on_close(ws):
    print("### closed ###")


def chat_on_open(ws):
    def run(ws):
        global chat_send_state
        global chat_send_buffer
        global lock_chat

        while True:
            while not chat_send_state:
                pass

            lock_chat.acquire()
            try:
                ws.send(chat_send_buffer)
                chat_send_state = False
                chat_send_buffer = None
            finally:
                lock_chat.release()

        # dumb don't know if I am doing it right
        ws.close()

    x = threading.Thread(target=run, args=(ws, ))
    x.start()

def esp_on_message(ws, message):
    global lock_chat
    global chat_send_buffer
    global chat_send_state

    print("Received message from ESP:[", message + "]")

    lock_chat.acquire()
    try:
        chat_send_buffer = message.encode()
        chat_send_state = True
    finally:
        lock_chat.release()


def esp_on_error(ws, error):
    print(error)


def esp_on_close(ws):
    print("### closed ###")


def esp_on_open(ws):
    def run(ws):
        global esp_send_state
        global esp_send_buffer
        global lock_esp

        while True:
            while not esp_send_state:
                pass

            lock_esp.acquire()
            try:
                ws.send(esp_send_buffer)
                esp_send_state = False
                esp_send_buffer = None
            finally:
                lock_esp.release()


        # dumb don't know if I am doing it right
        ws.close()


    x = threading.Thread(target=run, args=(ws, ))
    x.start()


'''

    Open WebSocket to connect to JavaScript WebSocket from the django framework

    Send data only while running_esp is true and chat_send_state is set to true

'''

def chat_manager(thread_name):
    host_websocket = 'ws://gpspelle.com/ws/chat/ble/'
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp(host_websocket, on_message = chat_on_message, on_error = chat_on_error, on_close = chat_on_close)
    ws.on_open = chat_on_open

    ws.run_forever()

'''

    Open WebSocket to connect to MicroPython WebSocket

    Only send when running_chat is true and chat_send_state is set to true

    Set variables to send data to websocket from another thread

'''

def esp_manager(thread_name):
    host_websocket = 'ws://' + esp_host
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp(host_websocket, on_message = esp_on_message, on_error = esp_on_error, on_close = esp_on_close)
    ws.on_open = esp_on_open

    ws.run_forever()


def main():


    # Create two threads as follows
    try:
        x = threading.Thread(target=chat_manager, args=("Thread-1", ))
        y = threading.Thread(target=esp_manager, args=("Thread-2", ))

        x.start()
        y.start()
    except:
        print("Error: unable to start thread")


if __name__ == "__main__":
    main()
