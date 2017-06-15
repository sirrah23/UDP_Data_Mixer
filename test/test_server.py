import unittest
from src.proxy import ClientStore, Mixer, ProxyServerReqHandler

ADDRESS = "127.0.0.1"
PORT = 1234

def gen_data(seq_num, data):
    return {"request_type": "frame_data", "seq_num": seq_num, "data": data}

class TestClientStore(unittest.TestCase):

    def setUp(self):
        self.cs = ClientStore((ADDRESS,PORT))

    def test_new_frame_sent_successfully(self):
        frame = gen_data(1, [[1,0],[0,1]])
        self.cs.new_frame(frame)
        self.assertEqual(self.cs._seqnum, 1)
        self.assertEqual(len(self.cs._framebuffer), 1)
        self.assertEqual(self.cs._rcvdata, True)

    def test_new_frame_ignore(self):
        frame = gen_data(-2, [[1,0],[0,1]])
        self.cs.new_frame(frame)
        self.assertEqual(self.cs._seqnum, -1)
        self.assertEqual(len(self.cs._framebuffer), 0)
        self.assertEqual(self.cs._rcvdata, False)

    def get_agg_frame(self):
        frame = gen_data(1, [[1,0],[0,1]])
        self.cs.new_frame(frame)
        aggframe = self.cs.get_frame_for_agg()
        self.assertEqual(aggframe['stale'], False)
        self.assertEqual(aggframe['data'], [[1, 0],[0, 1]])

    def get_agg_frame_stale(self):
        frame = gen_data(1, [[1,0],[0,1]])
        self.cs.new_frame(frame)
        self.cs.get_frame_for_agg()
        aggframe = self.cs.get_frame_for_agg()
        self.assertEqual(aggframe['stale'], True)
        self.assertEqual(aggframe['data'], [[1, 0],[0, 1]])

    def get_agg_frame_second(self):
        frame = gen_data(1, [[1,0],[0,1]])
        self.cs.new_frame(frame)
        self.cs.get_frame_for_agg()
        frame = gen_data(1, [[1,1],[1,1]])
        self.cs.new_frame(frame)
        aggframe = self.cs.get_frame_for_agg()
        self.assertEqual(aggframe['stale'], False)
        self.assertEqual(aggframe['data'], [[1, 1],[1, 1]])


class TestMixer(unittest.TestCase):

    def setUp(self):
        self.mixer = Mixer()

    def test_mix_mat(self):
        data = [[[0, 1, 1, 0, 1], [0, 1, 1, 1, 1]]]
        self.assertEqual(self.mixer.mix(data), 7)

    def test_mix_two_mats(self):
        data = [[[0, 1],[0, 1]],[[1, 1],[1, 1]]]
        self.assertEqual(self.mixer.mix(data), 6)

class TestProxyServerRequestHandler(unittest.TestCase):

    def setUp(self):
        self.psrhandler = ProxyServerReqHandler(Mixer)

    def test_frame_data_rq(self):
        frame = gen_data(0, [[1,0],[0,1]])
        self.psrhandler.handle(frame, (ADDRESS, PORT))
        self.assertEqual(len(self.psrhandler._client_list), 1)

    def test_mix_command_rq(self):
        #TODO: Do this
        self.assertEqual(1, 2)
