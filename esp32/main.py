import _thread
import ubinascii
import ujson as json
from utime import sleep, localtime
from machine import UART, Pin
from uwebsockets.client import connect
import gc

gc.enable()

#sock_lock = _thread.allocate_lock()

# https://forums.openmv.io/viewtopic.php?t=885
batch = 2048

TX1 = 4
RX1 = 2

TX2 = 17
RX2 = 16

uart_1 = UART(1, 115200)
uart_1.init(115200, bits=8, parity=None, stop=1, rx=RX1, tx=TX1)

uart_2 = UART(2, 1152000, rxbuf=batch)
uart_2.init(1152000, bits=8, parity=None, stop=1, rx=RX2, tx=TX2)

t1_websocket = connect('ws://gpspelle.com:80/ws/chat/chatesp32/')
t2_websocket = connect('ws://gpspelle.com:80/ws/chat/imageesp32/')

separator_start = b'____start____'
separator_end = b'____end____'

def start_comm_master(uart):
    while True:
        uart.write("start\n")
        sleep(1)
        ans = uart.readline()
        try:
            ans = str(ans[:-1], 'utf-8')
            if ans == 'start':
                return
        except:
            continue

def send_uart_1(message):

    print("Send via uart_1 to pyboard: [" + message + "]")
    uart_1.write(message)

def read_uart_2(name):

    send_message_to_server("Camera is not connected", name)
    start_comm_master(uart_2)
    send_message_to_server("Camera is connected", name)

    i = 0
    msgs = [b'', b'']
    while True:
        msgs = read_data(msgs[1])
        message = msgs[0]
        i += 1

        # so far, no need for the timestamp
        #ct = localtime()
        #ct_str = '{0}{1}{2}_{3}{4}{5}'.format(ct[0], ct[1], ct[2], ct[3], ct[4], ct[5])
        #print(ct_str)

        send_image_to_server(message)

'''

def read_uart_2(name):
    
    send_message_to_server("Camera is not connected", name)
    start_comm_master(uart_2)
    send_message_to_server("Camera is connected", name)

    print("Natura non contristatur - uart_2 read")
    while True:
        #uart_2.write("1") # saying to camera send image

        size = None
        while size == None:
            size = uart_2.readline()

        size = size[:-1]
        print("What is in size", size)
        size = str(size, 'utf-8')
        print("Read size:", size)

        size = int(size)
        message = b''
        len_ = 0
        while len_ != size:
            m = uart_2.read(size-len_)
            #increased = False
            if m != None:
            #    increased = True
                len_ += len(m)
                message += m
            
            #if increased:
            #    print(len_, "of", size)

        send_image_to_server(message)
        gc.collect()
        print(gc.mem_free())

'''

def read_uart_1(name):
    
    send_message_to_server("Leleco is not receiving commands", name)
    start_comm_master(uart_1)
    send_message_to_server("Leleco is receiving commands", name)
    print("Cogito ergo sum - uart_1 read")

    while True:
        message = None
        while message == None:
            message = uart_1.read()

        send_message_to_server(message, name)

def send_image_to_server(message):
    #print("Send image to server")
    # openMV camera is already doing it
    #message = ubinascii.b2a_base64(message)
    package = {"message": message, "recipient": 'chat_image'}
    package = json.dumps(package)
    
    #sock_lock.acquire()
    t2_websocket.send(package)
    #sock_lock.release()

def send_message_to_server(message, name):

    message = str(message, 'utf-8')
    print("Send message to server: [" + message + "]")
    package = {"message": message, "recipient": 'chat_chat'}
    package = json.dumps(package)
    
    if '1' in name:
        #sock_lock.acquire()
        t1_websocket.send(package)
    else:
        #sock_lock.acquire()
        t2_websocket.send(package)

    #sock_lock.release()

def read_from_server(name):

    allowed_messages = ['forward', 'backward', 'left', 'right', 'stop', 'go']

    while True:

        message = b''
        while message == None or len(message) == 0:
            message = t1_websocket.recv()

        print("Message received: [", message, "]")
        message = json.loads(message)
        message = message['message']
        
        if message in allowed_messages: 
            send_uart_1(message)
        else:
            print("Received: [" + message + "]")

def read_data(buf):
    # Read enough data for a message

    while not (separator_start in buf and separator_end in buf):
        m = None
        p = b''
        while len(p) < batch and separator_end not in p:
            m = uart_2.read(batch - len(p))
            if m != None:
                p += m

        uart_2.write("1")
        buf += p

    # Locate message separators
    start_pos = buf.find(separator_start)
    end_pos = buf.find(separator_end)

    # Save the beginning of the next message if any
    new_msg = buf[end_pos + len(separator_end):]

    # Extract the message
    msg = buf[start_pos+len(separator_start):end_pos]

    return [msg, new_msg]

def main():

    # Create one thread for the communication as follows

    try:
        _thread.start_new_thread(read_from_server, ("Thread-0", ))
        _thread.start_new_thread(read_uart_1, ("Thread-1", ))
        _thread.start_new_thread(read_uart_2, ("Thread-2", ))
        led_g.value(1)
    except:
        print("Error: unable to start thread")

    while True:
        pass


if __name__ == "__main__":
    main()
