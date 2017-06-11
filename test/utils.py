import threading
import socket
import pickle

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
            data = pickle.loads(data)
            self.received_data.append(data)
            sock.close()
            return
        
        self.server_thread = threading.Thread(target=fake_server)
        self.server_thread.start()