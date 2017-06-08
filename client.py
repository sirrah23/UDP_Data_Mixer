class Client(object):

    def __init__(self, rows, cols, proxy_address, proxy_port):
        self.rows = rows
        self.cols = cols
        self.grid = [] #TODO: initialize this
        self.proxy_address = proxy_address
        self.proxy_port = proxy_port
