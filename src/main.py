from config import CELL_STATE, INPUT_SIZE
from spatial import OnlySpatial
import numpy as np
from visualize_vis import *

a = OnlySpatial(100)
a.initSpatial()

htm.initConnections(a.spatial_connections)

def update(event):
    samp = np.zeros(INPUT_SIZE,dtype=np.int32)
    samp[np.random.randint(0,INPUT_SIZE,(15))] = CELL_STATE.ACTIVE
    #samp[20:30] = CELL_STATE.ACTIVE

    winner_columns = a.spatialStep(samp)

    
    htm.updateWinners(winner_columns)



    htm.canvas.update()


timer = app.Timer(0.4,update)
timer.start()
app.run()