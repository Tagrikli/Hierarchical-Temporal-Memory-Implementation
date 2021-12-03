import numpy as np
from config import *


connections_x = np.random.randint(
    0, COL_COUNT, (COL_COUNT, COL_HEIGH, CON_COUNT))
connections_y = np.random.randint(
    0, COL_HEIGH, (COL_COUNT, COL_HEIGH, CON_COUNT))
connections = np.stack((connections_x, connections_y), 3)

permen = np.random.random((COL_COUNT, COL_HEIGH, CON_COUNT))

active_cells = np.zeros((COL_COUNT, COL_HEIGH), dtype=np.int32)
predic_cells = np.zeros((COL_COUNT, COL_HEIGH), dtype=np.int32)

active_cells[:, :2] = 1
predic_cells[0, 2] = 1

active_conns = active_cells[connections[:, :, :, 0], connections[:, :, :, 1]]
predic_conns = predic_cells[connections[:, :, :, 0], connections[:, :, :, 1]]

connected_active_conns = np.ma.array(
    active_conns, mask=(permen < PER_THRES)).filled(fill_value=0)

connected_predic_conns = np.ma.array(
    predic_conns, mask=(permen < PER_THRES)).filled(fill_value=0)

connected_active_conns_overlap = np.sum(connected_active_conns, axis=2)
connected_predic_conns_overlap = np.sum(connected_predic_conns, axis=2)

print(connected_active_conns_overlap)
print(connected_predic_conns_overlap)

