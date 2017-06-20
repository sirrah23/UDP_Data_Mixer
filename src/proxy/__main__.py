from proxy import ProxyServer
from proxy import Mixer
from proxy import mix_interval
import argparse

def main():
    # Get command line arguments
    parser = argparse.ArgumentParser(description="Start a proxy-server")
    parser.add_argument('ip', type=str, help="ip of the proxy server")
    parser.add_argument('port', type=int, help="port of the proxy server")
    args = vars(parser.parse_args())

    # Run the server
    ps = ProxyServer(args["ip"], args["port"], Mixer())
    mix_interval(ps, 3)
    ps.run()

main()