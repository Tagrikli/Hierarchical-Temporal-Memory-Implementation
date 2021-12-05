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
column_input = np.zeros(COLUMN_COUNT)
column_input[np.random.randint(0, COLUMN_COUNT, int(
    0.2 * COLUMN_COUNT))] = CELL_STATE.ACTIVE
#column_input[0] = CELL_STATE.ACTIVE
print(column_input)

cell_states[:, :2] = CELL_STATE.ACTIVE
cell_states[0, 2] = CELL_STATE.PREDICTING

new_cell_states = np.zeros((COLUMN_COUNT, COLUMN_HEIGHT), dtype=np.int32)
##SAMPLE INPUT####################


bool_column_input = np.bool8(column_input)
bool_column_input_T = bool_column_input[:,np.newaxis]

#Column Active & Cells Predicting /STRENGHTEN
predicting_cells = np.equal(cell_states, CELL_STATE.PREDICTING)
active_predicting = np.bitwise_and(predicting_cells, bool_column_input_T)
active_predicting_indices = np.where(active_predicting)

#Column Active & Cells NotPredicting /BURST
not_predicting_cells = np.bitwise_not(predicting_cells)
not_predicting_columns = np.all(not_predicting_cells,axis=1)
columns_to_burst = np.bitwise_and(not_predicting_columns, bool_column_input)


#Column NotActive & Predicting
not_bool_column_input = np.bitwise_not(bool_column_input)
predicting_columns = np.any(predicting_cells,axis=1)
columns_has_wrong_prediction = np.bitwise_and(not_bool_column_input,predicting_columns)
columns_has_wrong_prediction_T = columns_has_wrong_prediction[:,np.newaxis]
cells_has_wrong_predictions = np.bitwise_and(predicting_cells, columns_has_wrong_prediction_T)
cells_has_wrong_prediction_indices = np.where(cells_has_wrong_predictions)



active_connections = np.equal(cell_states[temporal_connections[:,
                                                               :, :, 0], temporal_connections[:, :, :, 1]], CELL_STATE.ACTIVE)

predicting_connections = np.equal(cell_states[temporal_connections[:,
                                                                   :, :, 0], temporal_connections[:, :, :, 1]], CELL_STATE.PREDICTING)

permenance_values_mask = permenance_values >= PERMENANCE_THRESHOLD

connected_active_conns = np.logical_and(
    active_connections, permenance_values_mask)

connected_predic_conns = np.logical_and(
    predicting_connections, permenance_values_mask)


connected_active_conns_overlap = np.sum(connected_active_conns, axis=2)
connected_predic_conns_overlap = np.sum(connected_predic_conns, axis=2)
