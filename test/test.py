import unittest
import time
from src.client import Client
from .utils import FakeServer

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
        time.sleep(0.5) # Give thread time to start
        self.client.send_msg_to_proxy(self.client.generate_msg())
        time.sleep(0.5) # Give message time to be sent and processed
        server.stop()
        time.sleep(0.5)
        self.assertEqual(len(server.received_data), 1) 
        self.assertEqual(server.received_data[0]['seq_num'], 0)
        self.assertEqual(server.received_data[0]['data'], self.client.grid)

    def test_drop_packet(self):
        self.assertEqual(0, self.client.seq_num)
        self.client.drop_packet()
        self.assertEqual(1, self.client.seq_num)
        self.assertEqual(False, self.client.transmit_this_packet)

    def test_drop_packet_twice(self):
        self.assertEqual(0, self.client.seq_num)
        self.client.drop_packet()
        self.assertEqual(1, self.client.seq_num)
        self.assertEqual(False, self.client.transmit_this_packet)
        self.client.drop_packet()
        self.assertEqual(1, self.client.seq_num)
        self.assertEqual(False, self.client.transmit_this_packet)

    def test_send_frame(self):
        server = FakeServer(ADDRESS, PORT)
        server.run()
        time.sleep(0.5)
        self.client.send_frame(self.client.generate_msg())
        time.sleep(0.5)
        server.stop()
        time.sleep(0.5)
        self.assertEqual(len(server.received_data), 1) 
        self.assertEqual(server.received_data[0]['seq_num'], 0)
        self.assertEqual(server.received_data[0]['data'], self.client.grid)

    def test_drop_send_frame(self):
        server = FakeServer(ADDRESS, PORT)
        server.run()
        time.sleep(0.5)
        self.client.drop_packet()
        self.client.send_frame(self.client.generate_msg())
        time.sleep(0.5)
        server.stop()
        time.sleep(0.5)
        self.assertEqual(len(server.received_data), 0) 

    def tearDown(self):
        self.client.stop_client()
