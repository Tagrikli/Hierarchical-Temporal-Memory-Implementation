from numpy import e
from visualize_vis import *
import time

while True:

    app.create()
    app.process_events()

    pos= np.random.uniform(-100,100,(10000,3))
    markers.set_data(pos=pos)
    canvas.update()

    time.sleep(0.1)


