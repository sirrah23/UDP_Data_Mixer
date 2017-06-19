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

    def update(self, **kwargs):
        print("Update gui")
        with self._lock:
            self._arr = kwargs['arr']
            self._rows = kwargs['rows']
            self._cols = kwargs['cols']

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
                print(event)
                if event.type in (pygame.QUIT, pygame.KEYDOWN):
                    pygame.quit()
                    return
            with self._lock:
                arr, rows, cols = self._arr, self._rows, self._cols
            if arr:
                self.draw_grid(screen, arr, rows, cols)
            pygame.display.update()
            pygame.time.delay(100)
            pygame.event.pump()
