import numpy as np
from config import *


# Init temporal connections
temporal_connections_columns = np.random.randint(
    0, COLUMN_COUNT, (COLUMN_COUNT, COLUMN_HEIGHT, TEMPORAL_CONNECTION_COUNT))
temporal_connections_cells = np.random.randint(
    0, COLUMN_HEIGHT, (COLUMN_COUNT, COLUMN_HEIGHT, TEMPORAL_CONNECTION_COUNT))
temporal_connections = np.stack(
    (temporal_connections_columns, temporal_connections_cells), 3)

# Init permenance values
permenance_values = np.random.random(
    (COLUMN_COUNT, COLUMN_HEIGHT, TEMPORAL_CONNECTION_COUNT))

# Init cells status for active and predicting
active_cells = np.zeros((COLUMN_COUNT, COLUMN_HEIGHT), dtype=np.int32)
predicting_cells = np.zeros((COLUMN_COUNT, COLUMN_HEIGHT), dtype=np.int32)

cell_states = np.zeros((COLUMN_COUNT, COLUMN_HEIGHT), dtype=np.int32)
##SAMPLE INPUT####################
active_cells[:, :2] = 1
predicting_cells[0, 2] = 1

cell_states[:, :2] = 1
cell_states[0, 2] = 2
##SAMPLE INPUT####################


active_connections = np.equal(cell_states[temporal_connections[:,
                                                               :, :, 0], temporal_connections[:, :, :, 1]], CELL_STATE.ACTIVE)

predicting_connections = np.equal(cell_states[temporal_connections[:,
                                                                   :, :, 0], temporal_connections[:, :, :, 1]], CELL_STATE.PREDICTING)


connected_active_conns = np.logical_and(
    active_connections, permenance_values >= PERMENANCE_THRESHOLD
)

connected_predic_conns = np.logical_and(
    predicting_connections, permenance_values >= PERMENANCE_THRESHOLD
)

connected_active_conns_overlap = np.sum(connected_active_conns, axis=2)
connected_predic_conns_overlap = np.sum(connected_predic_conns, axis=2)
