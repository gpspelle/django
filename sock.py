try:
    import usocket as socket
except:
    import socket

MSGLEN = 128

def ljust(msg, size):
    return msg + ' ' * max(0, size - len(msg))

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
        msg = ljust(msg, MSGLEN)
        msg = msg.encode()

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

    def listen(self, n):
        self.sock.listen(n)

    def close(self):
        self.sock.close()

    def accept(self):
        return self.sock.accept()
