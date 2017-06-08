import unittest

from client import Client

class TestClient(unittest.TestCase):

    def setUp(self):
        self.client = Client(rows=3, cols=4,proxy_address='127.0.0.1',proxy_port=5005)
    
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


if __name__ == '__main__':
    unittest.main()
