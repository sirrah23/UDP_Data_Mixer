import unittest
import pickle
from src.proxy.proxy import ClientStore, Mixer, ProxyServerReqHandler

ADDRESS = "127.0.0.1"
PORT = 1234

def gen_data(seq_num, data):
    return {"request_type": "frame_data", "seq_num": seq_num, "data": data}

def gen_server_data(seq_num, data):
    return pickle.dumps(gen_data(seq_num, data))

def gen_mix_request():
    return pickle.dumps({"request_type": "mix_command"})

def gen_mix_frame(staleness, data):
    return {"stale": staleness, "data": data}

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

    def test_get_agg_frame(self):
        frame = gen_data(1, [[1,0],[0,1]])
        self.cs.new_frame(frame)
        aggframe = self.cs.get_frame_for_agg()
        self.assertEqual(aggframe['stale'], False)
        self.assertEqual(aggframe['data'], [[1, 0],[0, 1]])

    def test_get_agg_frame_stale(self):
        frame = gen_data(1, [[1,0],[0,1]])
        self.cs.new_frame(frame)
        self.cs.get_frame_for_agg()
        aggframe = self.cs.get_frame_for_agg()
        self.assertEqual(aggframe['stale'], True)
        self.assertEqual(aggframe['data'], [[1, 0],[0, 1]])

    def test_get_agg_frame_second(self):
        frame = gen_data(1, [[1,0],[0,1]])
        self.cs.new_frame(frame)
        self.cs.get_frame_for_agg()
        frame = gen_data(2, [[1,1],[1,1]])
        self.cs.new_frame(frame)
        aggframe = self.cs.get_frame_for_agg()
        self.assertEqual(aggframe['stale'], False)
        self.assertEqual(aggframe['data'], [[1, 1],[1, 1]])


class TestMixer(unittest.TestCase):

    def setUp(self):
        self.mixer = Mixer()

    def test_mix_mat(self):
        data = [[[0, 1, 1, 0, 1], [0, 1, 1, 1, 1]]]
        self.assertEqual(self.mixer.mix_matrices(data), 7)

    def test_mix_two_mats(self):
        data = [[[0, 1],[0, 1]],[[1, 1],[1, 1]]]
        self.assertEqual(self.mixer.mix_matrices(data), 6)

    def test_mix_no_stale(self):
        f1 = gen_mix_frame(False, [[1, 1, 1],[1, 1, 1]])
        f2 = gen_mix_frame(False, [[1, 0, 0, 1],[0, 1, 0, 1]])
        f3 = gen_mix_frame(False, [[1, 0],[0, 1]])
        self.assertEqual(self.mixer.mix([f1, f2, f3]), 12)

    def test_mix_just_stale(self):
        f1 = gen_mix_frame(True, [[1, 1, 1],[1, 1, 1]])
        f2 = gen_mix_frame(True, [[1, 0, 1, 1],[0, 1, 0, 1]])
        f3 = gen_mix_frame(True, [[1, 0],[0, 1]])
        self.assertEqual(self.mixer.mix([f1, f2, f3]), 6.5)

    def test_mix_stale_and_no_stale(self):
        f1 = gen_mix_frame(True, [[1, 1, 1],[1, 1, 1]])
        f2 = gen_mix_frame(False, [[1, 0, 1, 1],[0, 1, 0, 1]])
        f3 = gen_mix_frame(False, [[1, 0],[0, 1]])
        self.assertEqual(self.mixer.mix([f1, f2, f3]), 10)


class TestProxyServerRequestHandler(unittest.TestCase):

    def setUp(self):
        self.psrhandler = ProxyServerReqHandler(Mixer())

    def test_frame_data_rq(self):
        frame = gen_server_data(0, [[1,0],[0,1]])
        self.psrhandler.handle(frame, (ADDRESS, PORT))
        self.assertEqual(len(self.psrhandler._clients), 1)

    def test_mix_command_rq(self):
        """Mix two client frames together"""
        client_1 = ("127.0.0.1", 5005)
        client_2 = ("127.0.0.1", 5006)
        frame1 = gen_server_data(0, [[1,0],[0,1]])
        frame2 = gen_server_data(0, [[1,1],[1,1]])
        mix_cmd = gen_mix_request()
        self.psrhandler.handle(frame1, client_1)
        self.psrhandler.handle(frame2, client_2)
        self.psrhandler.handle(mix_cmd, None)
        self.assertEqual(len(self.psrhandler._clients), 2)
        self.assertEqual(len(self.psrhandler._packets), 1)
        self.assertEqual(self.psrhandler._packets[0], 6)
