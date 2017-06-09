import threading
import socket
import cPickle

class FakeServer(object):

    def __init__(self, address, port):
        self.address = address
        self.port = port
        self.received_data = []
        self.server_thread = None

    def run(self):

        def fake_server():
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
            sock.bind((self.address, self.port))
            data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
            data = cPickle.loads(data)
            self.received_data.append(data)
            return
        
        self.server_thread = threading.Thread(target=fake_server)
        self.server_thread.start()