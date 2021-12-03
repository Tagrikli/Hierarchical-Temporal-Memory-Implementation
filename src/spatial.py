import numpy as np
from config import *

class OnlySpatial:

    def __init__(self, input_size) -> None:

        self.input_size = input_size
        self.columns = np.zeros(COLUMN_COUNT)
        self.spatial_connections = []
        self.spatial_boosts = []
        self.neighbor_indices = self.__getNeighborIndices()

    def spatialStep(self, input_data):
        # Total overlaps per column
        spatial_overlaps = np.sum(input_data[self.spatial_connections], axis=1)

        # Total overlaps multiplied by boost per column
        spatial_overlaps_boosted = np.multiply(
            spatial_overlaps, self.spatial_boosts)

        # Take overlaps from indices
        neighbor_overlaps = np.take(spatial_overlaps_boosted, self.neighbor_indices)

        # NTH_SCORE of the every neighbor
        nty_scores_per_inhibition_area = np.partition(
            neighbor_overlaps, -KTH_SCORE, axis=1)[:, -KTH_SCORE][:, np.newaxis]

        # Overlaps greater than or equal to NTH_SCORE of the neighborhood
        inhibited_mask = np.less(
            neighbor_overlaps, nty_scores_per_inhibition_area)

        # Mask neighbor indices with overlap mask
        inhibited_neighbor_indices = np.ma.array(
            self.neighbor_indices, mask=inhibited_mask)

        # Compress the array and get unique values
        inhibited_neighbor_indices = np.unique(
            inhibited_neighbor_indices.compressed())

        # Reset Columns
        self.columns.fill(0)

        # Set active indices to 1
        self.columns[inhibited_neighbor_indices] = 1

        return self.columns

    def initSpatial(self):
        '''
        Initialize spatial connections and boost values
        '''
        self.spatial_connections = np.random.randint(
            0, self.input_size, (COLUMN_COUNT, SPATIAL_CONNECTION_COUNT))

        self.spatial_boosts = np.ones(COLUMN_COUNT, dtype=np.int32)


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

        return arr