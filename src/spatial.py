import numpy as np
from config import *


class OnlySpatial:

    def __init__(self, input_size) -> None:

        self.input_size = input_size
        self.columns = np.zeros(COLUMN_COUNT)
        self.spatial_connections = np.empty(
            (COLUMN_COUNT, SPATIAL_CONNECTION_COUNT), dtype=np.int32)


        self.spatial_boosts = np.empty(COLUMN_COUNT, dtype=np.int32)
        self.permenance_values = np.empty(
            (COLUMN_COUNT, SPATIAL_CONNECTION_COUNT), dtype=np.float64)
        self.neighbor_indices = self.__getNeighborIndices()

        self.__configCheck()

    def spatialStep(self, input_data):

        # Find connected cells and mask input data
        connected_cells = self.permenance_values >= PERMENANCE_THRESHOLD
        connected_input_data = input_data[self.spatial_connections] * \
            connected_cells

        # Total overlaps per column
        spatial_overlaps = np.sum(connected_input_data, axis=1)

        # Total overlaps multiplied by boost per column
        spatial_overlaps_boosted = np.multiply(
            spatial_overlaps, self.spatial_boosts)

        # Take overlaps from indices
        neighbor_overlaps = np.take(
            spatial_overlaps_boosted, self.neighbor_indices)

        # NTH_SCORE of the every neighbor
        nty_scores_per_inhibition_area = np.partition(
            neighbor_overlaps, -KTH_SCORE, axis=1)[:, -KTH_SCORE][:, np.newaxis]

        # Overlaps greater than or equal to NTH_SCORE of the neighborhood
        loser_neighbors = np.less(
            neighbor_overlaps, nty_scores_per_inhibition_area)

        # Mask neighbor indices with overlap mask
        winner_neighbors = np.ma.array(
            self.neighbor_indices, mask=loser_neighbors)

        # Compress the array and get unique values
        winner_columns = np.unique(
            winner_neighbors.compressed())

        # Increase and decrease permenance values accordingly
        if LEARNING:
            input_data_of_winner_columns = input_data[self.spatial_connections[winner_columns]]

            active_winner_connections = np.equal(
                input_data_of_winner_columns, CELL_STATE.ACTIVE)
            inactive_winner_connections = np.equal(
                input_data_of_winner_columns, CELL_STATE.INACTIVE)

            temp = self.permenance_values[winner_columns].copy()
            temp[active_winner_connections] += PERMENCANCE_INCREMENT
            temp[inactive_winner_connections] -= PERMENCANCE_DECREAMENT
            self.permenance_values[winner_columns] = temp

            np.clip(self.permenance_values, 0., 1.)

        # Reset Columns
        self.columns.fill(0)

        # Set active indices to 1
        self.columns[winner_columns] = 1

        return winner_columns

    def initSpatial(self):
        '''
        Initialize spatial connections and boost values
        '''
        # self.spatial_connections = np.random.randint(
        #     0, self.input_size, (COLUMN_COUNT, SPATIAL_CONNECTION_COUNT))

        self.permenance_values = np.random.uniform(PERMENANCE_THRESHOLD - INIT_PERMENANCE_RADIUS,
                                                   PERMENANCE_THRESHOLD + INIT_PERMENANCE_RADIUS,
                                                   (COLUMN_COUNT, SPATIAL_CONNECTION_COUNT))

        self.spatial_connections = np.zeros(
            (COLUMN_COUNT, SPATIAL_CONNECTION_COUNT), dtype=np.int32)
        for index in range(self.spatial_connections.shape[0]):
            self.spatial_connections[index] = np.random.choice(
                self.__neighborRanges(index), SPATIAL_CONNECTION_COUNT, replace=False)

        self.spatial_boosts = np.ones(COLUMN_COUNT, dtype=np.int32)

    def __neighborRanges(self, index):

        FIRST_IND = 0
        LAST_IND = COLUMN_COUNT - 1

        if not FIRST_IND <= index <= LAST_IND:
            raise Exception('Index value must be in range [0,COLUMN_COUNT -1]')

        range = []

        start_edge = index - int(INHIBITION_RADIUS/2)
        stop_edge = index + int(INHIBITION_RADIUS/2)

        if start_edge < 0 and stop_edge >= 0:
            r1 = np.arange(start_edge % COLUMN_COUNT, LAST_IND + 1)
            r2 = np.arange(FIRST_IND, stop_edge + 1)
            range = (*r1, *r2)

        elif stop_edge > LAST_IND and start_edge < LAST_IND:
            r1 = np.arange(0, (stop_edge % COLUMN_COUNT) + 1)
            r2 = np.arange(start_edge, LAST_IND + 1)
            range = (*r1, *r2)

        elif start_edge >= FIRST_IND and stop_edge <= LAST_IND:
            range = (*np.arange(start_edge, stop_edge + 1),)

        return np.array(range, dtype=np.int32)

    def __getNeighborIndices(self):
        '''
        Creates an array filled with neighbor columns indices per column
        '''
        arr = []
        for i in range(COLUMN_COUNT):
            item = []
            for j in range(-int(INHIBITION_RADIUS/2), int(INHIBITION_RADIUS/2)+1):
                index = i + j

                if index < 0 or index >= COLUMN_COUNT:
                    index %= COLUMN_COUNT

                item.append(index)
            arr.append(item)

        return np.array(arr, dtype=np.int32)

    def __configCheck(self):
        if INHIBITION_RADIUS > COLUMN_COUNT:
            raise Exception(
                'INHIBITION_RADIUS cannot be greater than COLUMN_COUNT')

        if INHIBITION_RADIUS < SPATIAL_CONNECTION_COUNT:
            raise Exception(
                'INHIBITION_RADIUS cannot be lesser than SPATIAL_CONNECTION_COUNT')

        if not INHIBITION_RADIUS % 2:
            raise Exception('INHIBITION_RADIUS cannot be an even number')


if __name__ == '__main__':
    pass
    