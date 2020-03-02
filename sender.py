import json
import websocket
from sock import Sock

try:
    import thread
except ImportError:
    import _thread as thread


def main():
    host_websocket = 'ws://127.0.0.1:8000/ws/chat/bla/'
    host_socket = '127.0.0.1'
    port = 80
    ws = websocket.WebSocket()
    ws.connect(host_websocket, http_proxy_host="proxy_host_name", http_proxy_port=port)

    s = Sock()
    s.bind(host_socket, port)
    s.listen()


    while True:
        conn, addr = s.accept()
        print('Connected by', addr)
        with conn:

            try:
                while True:
                    data = s.receive(conn)
                    data = data.decode('utf-8')
                    d = {"message": data }
                    d = json.dumps(d)
                    ws.send(d)
            except:
                break

    s.close()
    ws.close()


if __name__ == "__main__":
    main()
