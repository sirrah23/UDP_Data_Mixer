from client import Client
from view import GridScreen
from controller import Controller
import threading

def main():
		# Initialize objects
        client = Client(5, 5, "127.0.0.1", 5005)
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