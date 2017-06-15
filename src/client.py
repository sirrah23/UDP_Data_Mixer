import socket
import random
import pickle


#TODO: Should probably write some unit tests for this thing
class SequenceNumberMgr(object):

    def __init__(self):
        self.sequence_numbers = []
        self.gen = self.seq_num_gen()

    def seq_num_gen(self):
        n = 0
        while True:
            yield n
            n += 1

    def get_next_seq_num(self):
        if len(self.sequence_numbers) == 0:
            return next(self.gen)
        else:
            return self.sequence_numbers.pop(0)

    def skip_seq_num(self):
        if len(self.sequence_numbers) == 0:
            next(self.gen)
        else:
            self.sequence_numbers.pop(0)

    def reverse_seq_nums(self):
        while len(self.sequence_numbers) < 2:
            self.sequence_numbers.append(next(self.gen))
        self.sequence_numbers[0], self.sequence_numbers[1] = self.sequence_numbers[1], self.sequence_numbers[0]


class Client(object):

    def __init__(self, rows, cols, proxy_address, proxy_port):
        self.rows = rows
        self.cols = cols
        self.proxy_address = proxy_address
        self.proxy_port = proxy_port
        self.grid = self.generate_grid()
        self.socket = self.create_socket()
        self.transmit_this_packet = True
        self.sqnmanager = SequenceNumberMgr()

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
        else:
            self.transmit_this_packet = False

    def send_msg_to_proxy(self, data):
        msg = pickle.dumps(data)
        self.socket.sendto(msg, (self.proxy_address, self.proxy_port))

    def generate_msg(self):
        return {
                "request_type": "frame_data",
                "seq_num": self.sqnmanager.get_next_seq_num(),
                "data": self.grid
                }

    def stop_client(self):
        self.socket.close()

    def drop_packet(self):
        if self.transmit_this_packet:
            self.transmit_this_packet = False
            self.sqnmanager.skip_seq_num()

    def skip_packet(self):
        if self.transmit_this_packet:
            self.sqnmanager.skip_seq_num()

    def reverse_seq(self):
        self.sqnmanager.reverse_seq_nums()
