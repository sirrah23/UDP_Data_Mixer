import random

class Client(object):

    def __init__(self, rows, cols, proxy_address, proxy_port):
        self.rows = rows
        self.cols = cols
        self.proxy_address = proxy_address
        self.proxy_port = proxy_port
        self.seq_num = 0
        self.grid = self.generate_grid()

    def generate_grid(self):
        grid = []
        for row in range(self.rows):
            col = []
            for _ in range(self.cols):
                col.append(random.choice((0,1)))
            grid.append(col)
        return grid
