import socket
import random
import pickle

class Client(object):

    def __init__(self, rows, cols, proxy_address, proxy_port):
        self.rows = rows
        self.cols = cols
        self.proxy_address = proxy_address
        self.proxy_port = proxy_port
        self.seq_num = 0
        self.grid = self.generate_grid()
        self.socket = self.create_socket()
        self.transmit_this_packet = True

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

    def send_frame(self):
        if self.transmit_this_packet:
            data = self.generate_msg()
            self.send_msg_to_proxy(data)
            self.seq_num += 1 # next frame!
        else:
            self.transmit_this_packet = False

    def send_msg_to_proxy(self, data):
        msg = pickle.dumps(data)
        self.socket.sendto(msg, (self.proxy_address, self.proxy_port))

    def generate_msg(self):
        return {
                "seq_num": self.seq_num,
                "data": self.grid
                }
    
    def stop_client(self):
        self.socket.close()

    def drop_packet(self):
        if self.transmit_this_packet:
            self.transmit_this_packet = False
            self.seq_num += 1

    def skip_packet(self):
        if self.transmit_this_packet:
            self.seq_num += 1

    def reverse_seq(self):
        pass
