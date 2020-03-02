try:
    import usocket as socket
except:
    import socket

MSGLEN = 1024

class Sock:
    """demonstration class only
      - coded for clarity, not efficiency
    """

    def __init__(self, sock=None):
        if sock is None:
            self.sock = socket.socket(
                            socket.AF_INET, socket.SOCK_STREAM)
        else:
            self.sock = sock

    def connect(self, host, port):
        self.sock.connect((host, port))

    def send(self, msg):
        totalsent = 0
        if len(msg) <= 1024:
            msg = msg.ljust(1024)

        while totalsent < MSGLEN:
            sent = self.sock.send(msg[totalsent:])
            if sent == 0:
                raise RuntimeError("socket connection broken")
            totalsent = totalsent + sent

    def receive(self, sock):
        chunks = []
        bytes_recd = 0
        while bytes_recd < MSGLEN:
            chunk = sock.recv(min(MSGLEN - bytes_recd, MSGLEN))
            if chunk == b'':
                raise RuntimeError("socket connection broken")
            chunks.append(chunk)
            bytes_recd = bytes_recd + len(chunk)

        st = b''.join(chunks)
        st = st.decode()
        st = st.strip()
        return st.encode()

    def bind(self, host, port):
        self.sock.bind((host, port))

    def listen(self):
        self.sock.listen()

    def close(self):
        self.sock.close()

    def accept(self):
        return self.sock.accept()
