import socket
import threading

MIX = "mix_command"
FRAME = "frame_data"

class Mixer(object):

    def __int__(self):
        pass

    def mix(self, data):
        """Aggregate all of the nested matrices via summing all the numbers"""
        return sum([sum(map(sum, mat)) for mat in data])

class ClientStore(object):

    def __init__(self, addr):
        self._address = addr[0]
        self._port = addr[1]
        self._framebuffer = []
        self._seqnum = -1
        self._rcvdata = False

    def new_frame(self, data):
        if data["seq_num"] > self._seqnum:
            self._seqnum = data["seq_num"]
            self._framebuffer.append(data["data"])
            self._rcvdata = True

    #TODO: Implement
    def get_frame_for_agg(self):
        pass


#TODO: Unit tests for this class
class ProxyServerReqHandler(object):

    def __init__(self, Mixer):
        self._client_list = {}
        self._lock = threading.RLock()
        self._mixer = Mixer()
        self._packets = []

    def handle(self, data, addr):
        #TODO: Write mix_handle and frame_handle functions...
        with self._lock:
            if data["request_type"] == FRAME:
                cstore = self.get_client(addr)
                if not cstore:
                    cstore = self.insert_client(addr)
                cstore.new_frame(data)
            elif data["request_type"] == MIX:
                frames_to_agg = []
                for k, v in self._client_list:
                    frames_to_agg.append(v.get_frame_for_agg())
                frames_to_agg = self.normalize_frames(frames_to_agg)
                #TODO: Filter empty frames...
                packet = self._mixer.mix(frames_to_agg)
                self._packets.append(packet)

    #TODO: Implement this
    def normalize_frames(self):
        pass

    def get_client(self, addr):
        return self._client_list.get(addr, None)

    def insert_client(self, addr):
        self._client_list[addr] = ClientStore(addr)
        return self._client_list[addr]


class ProxyServer(object):

    def __init__(self, address, port, Mixer):
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.address = address
        self.port = port
        self.reqhandler = ProxyServerReqHandler(Mixer)

    def run(self):
        self._sock.bind((self.address, self.port))
        while True:
            data, addr = self._sock.recvfrom(1024)
            threading.Thread(target=self.reqhandler.handle, args=(data, addr)).start()


if __name__ == "__main__":
    ps = ProxyServer("127.0.0.1", 5005, Mixer)
    ps.run()
