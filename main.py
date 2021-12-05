from Model import Model
from PlayerWindow import PlayerWindow
from helpers import *
from Settings import *

def main():
    window = PlayerWindow (config = pyglet.gl.Config(sample_buffers=1, samples=16), width=WIDTH, height=HEIGHT, caption='Pyglet', resizable=True)
    # Hide the mouse cursor and prevent the mouse from leaving the window.
    window.set_exclusive_mouse (True)
    setup()
    pyglet.app.run()

if __name__ == '__main__':
    main()
