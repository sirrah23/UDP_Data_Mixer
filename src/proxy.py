import socket
import threading

# TODO: Write unit tests...

class ClientStore(object):

    def __init__(self, addr):
        self._address = addr[0]
        self._port = addr[1]
        self._framebuffer = []
        self._seqnum = -1

    def new_frame(self, data):
        self._framebuffer.append(data)
        print(data)
        print(len(self._framebuffer))


class ProxyServerReqHandler(object):

    def __init__(self):
        self._client_list = {}
        self._lock = threading.RLock()

    def handle(self, data, addr):
        with self._lock:
            cstore = self.get_client(addr)
            if not cstore:
                cstore = self.insert_client(addr)
            cstore.new_frame(data)

    def get_client(self, addr):
        return self._client_list.get(addr, None)

    def insert_client(self, addr):
        self._client_list[addr] = ClientStore(addr)
        return self._client_list[addr]


class ProxyServer(object):

    def __init__(self, address, port):
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
        self.address = address
        self.port = port
        self.reqhandler = ProxyServerReqHandler()

    def run(self):
        self._sock.bind((self.address, self.port))
        while True:
            data, addr = self._sock.recvfrom(1024)
            threading.Thread(target=self.reqhandler.handle, args=(data, addr)).start()


if __name__ == "__main__":
    ps = ProxyServer("127.0.0.1", 5005)
    ps.run()

