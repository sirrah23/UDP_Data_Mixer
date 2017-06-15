import unittest
from src.proxy import ClientStore, Mixer

ADDRESS = "127.0.0.1"
PORT = 1234

def gen_data(seq_num, data):
    return {"seq_num": seq_num, "data": data}

class TestClientStore(unittest.TestCase):

    def setUp(self):
        self.cs = ClientStore((ADDRESS,PORT))

    def test_new_frame_sent_successfully(self):
        frame = gen_data(1, [[1,0],[0,1]])
        self.cs.new_frame(frame)
        self.assertEqual(self.cs.seqnum, 1)
        self.assertEqual(len(self.cs.framebuffer), 1)

    def test_new_frame_ignore(self):
        frame = gen_data(-2, [[1,0],[0,1]])
        self.cs.new_frame(frame)
        self.assertEqual(self.cs.seqnum, -1)
        self.assertEqual(len(self.cs.framebuffer), 0)

class TestMixer(unittest.TestCase):

    def setUp(self):
        self.mixer = Mixer()

    def test_mix_mat(self):
        data = [[[0, 1, 1, 0, 1], [0, 1, 1, 1, 1]]]
        self.assertEqual(self.mixer.mix(data), 7)

    def test_mix_two_mats(self):
        data = [[[0, 1],[0, 1]],[[1, 1],[1, 1]]]
        self.assertEqual(self.mixer.mix(data), 6)
