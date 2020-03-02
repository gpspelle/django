from sock import Sock

host = '127.0.0.1'
port = 80

s = Sock()
s.connect(host, port)
s.send(b'bosta 0\n')
s.send(b'bosta 1\n')
s.send(b'bosta 2\n')
s.send(b'bosta 3\n')
s.send(b'bosta 4\n')
s.close()
