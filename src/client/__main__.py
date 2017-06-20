from client import Client
from view import GridScreen
from controller import Controller
import threading
import argparse

def main():
        # Get command line arguments
        parser = argparse.ArgumentParser(description="Start a matrix-client")
        parser.add_argument('rows', type=int, help="the number of rows in the client matrix")
        parser.add_argument('columns', type=int, help="the number of columns in the client matrix")
        parser.add_argument('ip', type=str, help="ip of the proxy server")
        parser.add_argument('port', type=int, help="port of the proxy server")
        args = vars(parser.parse_args())

	# Initialize objects
        client = Client(args['rows'], args['columns'], args['ip'], args['port'])
        gs = GridScreen()
        controller = Controller()

        # Establish relationships
        # View <--> Controller <--> Client
        client.subscribe(controller)
        controller.subscribe(client)
        gs.subscribe(controller)
        controller.subscribe(gs)

        # Fire it up
        client_thread = threading.Thread(target=client.start)
        client_thread.start()
        gs.show()
        client.stop()

main()