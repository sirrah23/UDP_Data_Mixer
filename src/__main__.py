from client import Client
from view import GridScreen
from controller import Controller
import threading

def main():
        client = Client(5, 5, "127.0.0.1", 5005)
        gs = GridScreen()
        controller = Controller(gs)
        client.subscribe(controller)
        client_thread = threading.Thread(target=client.start)
        client_thread.start()
        gs.show()
        client.stop()

main()
