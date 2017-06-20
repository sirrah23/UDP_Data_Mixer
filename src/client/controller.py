class Controller(object):

    def __init__(self):
        self._listeners = []

    def update(self, **kwargs):
        if kwargs.get('type', None) == 'client_grid':
            arr = kwargs['arr']
            rows = len(arr)
            cols = len(arr[0])
            for listener in self._listeners:
                listener.update(type="update_view", arr=arr, rows=rows, cols=cols)
        if kwargs.get('type', None) == 'command':
            for listener in self._listeners:
                listener.update(type="command", command_type = kwargs["command_type"])

    def subscribe(self, listener):
        self._listeners.append(listener)

    def unsubscribe(self, listener):
        for idx, val in enumerate(self.listeners):
            if listener == val:
                del self._listeners[idx]
                break

    def notify(self):
        for listener in self._listeners:
            listener.update
