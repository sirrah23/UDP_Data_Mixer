class Controller(object):

    def __init__(self, view):
        self._view = view
        self.listeners = []

    def update(self, **kwargs):
        arr = kwargs[arr]
        rows = len(arr)
        cols = len(arr[0])
        self._view.update(arr=arr, rows=row, cols=col)

    def subscribe(self, listener):
        self.listeners.append(listener)

    def unsubscribe(self, listener):
        for idx, val in enumerate(self.listeners):
            if listener == val:
                del self.listeners[idx]
                break

    def notify(self):
        for listener in self.listeners:
            listener.update
