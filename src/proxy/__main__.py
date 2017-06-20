from proxy import ProxyServer
from proxy import Mixer
from proxy import mix_interval

def main():
    ps = ProxyServer("127.0.0.1", 5005, Mixer())
    mix_interval(ps, 3)
    ps.run()

main()