import socket
import random
import cPickle

class Client(object):

    def __init__(self, rows, cols, proxy_address, proxy_port):
        self.rows = rows
        self.cols = cols
        self.proxy_address = proxy_address
        self.proxy_port = proxy_port
        self.seq_num = 0
        self.grid = self.generate_grid()
        self.socket = self.create_socket()

    def generate_grid(self):
        grid = []
        for row in range(self.rows):
            col = []
            for _ in range(self.cols):
                col.append(random.choice((0,1)))
            grid.append(col)
        return grid

    def create_socket(self):
        return socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    #TODO: Write tests for this
    def send_msg_to_proxy(self, data):
        msg = cPickle.dumps(data)
        self.socket.sendto(msg, (self.proxy_address, self.proxy_port))

    #TODO: Write tests for this
    def generate_msg(self):
        return {
                "seq_num": self.seq_num,
                "data": self.grid
                }

    def drop_packet(self):
        pass

    def skip_packet(self):
        pass

    def reverse_seq(self):
        pass
