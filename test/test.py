import unittest
import time
from src.client import Client
from .test_utils import FakeServer

# Address and Port where server will listen and
# client will send data...
ADDRESS = "127.0.0.1"
PORT = 5005

class TestClient(unittest.TestCase):

    def setUp(self):
        self.client = Client(rows=3, cols=4,proxy_address=ADDRESS, proxy_port=PORT)
    
    def test_grid_dimensions(self):
        self.assertEqual(self.client.rows, 3)
        self.assertEqual(self.client.cols, 4)
        self.assertEqual(len(self.client.grid), 3)
        for col in self.client.grid:
            self.assertEqual(len(col), 4)

    def test_grid_content(self):
        for row in self.client.grid:
            for col in row:
                self.assertTrue(col in (0, 1))

    def test_data_send(self):
        server = FakeServer(ADDRESS, PORT)
        server.run()
        time.sleep(1) # Give thread time to start
        self.client.send_msg_to_proxy(self.client.generate_msg())
        time.sleep(1) # Give message time to be sent and processed
        self.assertEqual(len(server.received_data), 1) 
        self.assertEqual(server.received_data[0]['seq_num'], 0)
        self.assertEqual(server.received_data[0]['data'], self.client.grid)

    def tearDown(self):
        pass
