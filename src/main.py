from spatial import OnlySpatial
import matplotlib.pyplot as plt
import numpy as np


##### SAMPLE INPUT ######
input_size = 100
input = np.zeros(input_size, dtype=np.int32)
input[:10] = 1
##### SAMPLE INPUT ######


fig, ax = plt.subplots(ncols=2)

layer = OnlySpatial(input_size)
layer.initSpatial()

a1 = layer.spatialStep(input)
