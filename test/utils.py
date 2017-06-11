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
            while True:
                data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
                if data == b'STOP':
                    sock.close()
                    return
                else:
                    data = pickle.loads(data)
                    self.received_data.append(data)
            
        self.server_thread = threading.Thread(target=fake_server)
        self.server_thread.start()

    def stop(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto("STOP".encode(), (self.address, self.port))
        sock.close()
