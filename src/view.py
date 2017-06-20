import pygame, sys, threading, time

pygame.init()
pygame.font.init()
myfont = pygame.font.SysFont('monospace', 30)

class GridScreen(object):

    def __init__(self):
        self._arr = None
        self._rows = None
        self._cols = None
        self._lock = threading.RLock()
        self._listeners = []

    def draw_grid(self, screen, arr, rows, cols):
        rect_height = 800 // rows
        rect_width = 800 // cols
        for row in range(rows):
            for col in range(cols):
                textsurface = myfont.render(str(arr[row][col]), False, (0, 0, 0))
                left, top = col*rect_width ,row*rect_height
                r = pygame.Rect(left, top, rect_width, rect_height)
                pygame.draw.rect(screen, (255, 255, 255), r)
                screen.blit(textsurface,(left + rect_width//2, top + rect_height//2))

    def show(self):
        screen = pygame.display.set_mode((800, 800))
        while 1:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.KEYDOWN:
                    if pygame.key.get_pressed()[pygame.K_d] != 0:
                        self.notify(type="command", command_type="drop")
                    elif pygame.key.get_pressed()[pygame.K_s] != 0: 
                        self.notify(type="command", command_type="skip")
                    elif pygame.key.get_pressed()[pygame.K_r] != 0: 
                        self.notify(type="command", command_type="reverse")
            with self._lock:
                arr, rows, cols = self._arr, self._rows, self._cols
            if arr:
                self.draw_grid(screen, arr, rows, cols)
            pygame.display.update()
            pygame.time.delay(100)
            pygame.event.pump()

    def subscribe(self, listener):
        self._listeners.append(listener)

    def unsubscribe(self, listener):
        for idx, val in enumerate(self.listeners):
            if listener == val:
                del self.listeners[idx]
                break

    def notify(self, **kwargs):
        if kwargs.get('type', None) == 'client_grid':
            with self.lock:
                for listener in self._listeners:
                    listener.update(type="client_grid", arr = self.grid)
        if kwargs.get('type', None) == 'command':
                for listener in self._listeners:
                    listener.update(type="command", command_type = kwargs['command_type'])

    def update(self, **kwargs):
        if kwargs.get('type', None) == 'update_view':
            with self._lock:
                self._arr = kwargs['arr']
                self._rows = kwargs['rows']
                self._cols = kwargs['cols']
