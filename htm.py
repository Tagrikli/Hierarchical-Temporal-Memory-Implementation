import numpy as np
import matplotlib.pyplot as plt
import random





class Cell:
    Inactive = 0
    Active = 1
    Predicting = 2

    def __init__(self) -> None:
        self.__curr_state = Cell.Inactive
        self.__prev_state = Cell.Inactive
        self.overlap_count = 0

    @property
    def state(self):
        return self.__curr_state

    @state.setter
    def state(self, new_state):
        self.__prev_state = self.__curr_state
        self.__curr_state = new_state

    def wasPredicting(self):
        return self.__prev_state == Cell.Predicting



class Column:
    def __init__(self, *, id, height, min_overlap, boost, connected_perm) -> None:
        self.id = id
        self.height = height
        self.cells = [Cell() for _ in range(height)]
        self.active = False

        self.input_indices = []
        self.permenance_values = []

        self.overlap_count = 0
        self.min_overlap = min_overlap
        self.boost = boost
        self.connected_perm = connected_perm

        self.perm_inc = 0.01
        self.perm_dec = 0.01


    def deactivate(self):
        pass

    def activate(self):
        has_predicted = False
        for cell in self.cells:
            if cell.wasPredicting():
                cell.state = Cell.Active
                has_predicted = True

        if not has_predicted:
            for cell in self.cells:
                cell.state = Cell.Active

    def setInputs(self, input_indices):
        self.input_indices = input_indices
        self.permenance_values = [random.random()
                                  for _ in range(len(input_indices))]

    def modifyConnections(self, input):
        for ind, index in enumerate(self.input_indices):
            cur_perm = self.permenance_values[ind]
            if input[index]:
                self.permenance_values[ind] = max(
                    cur_perm + self.perm_inc, 1.0)
            else:
                self.permenance_values[ind] = max(
                    cur_perm - self.perm_dec, 0.0)

    def countOverlap(self, input):
        self.overlap_count = 0

        for ind, index in enumerate(self.input_indices):
            self.overlap_count += input[index] if self.permenance_values[ind] > self.connected_perm else 0

        if self.overlap_count < self.min_overlap:
            self.overlap_count = 0
        else:
            self.overlap_count *= self.boost


class Layer:
    def __init__(self, *,
                 col_count,
                 col_height,
                 input_size,
                 input_ratio,
                 inhibition_radius,
                 desired_local_activity) -> None:

        self.col_count = col_count
        self.col_height = col_height
        self.input_size = input_size
        self.input_ratio = input_ratio
        self.inhibition_radius = inhibition_radius
        self.desired_local_activity = desired_local_activity
        self.columns = []
        self.active_columns = []

        self.cell_connections = []

    def initMiniColumns(self):
        self.columns = [Column(
            id=i,
            height=self.col_height,
            min_overlap=10,
            boost=1,
            connected_perm=0.2) for i in range(self.col_count)]

    

    def initConnections(self):
        for column in self.columns:
            indices = np.random.randint(0, self.input_size, int(
                self.input_size * self.input_ratio))
            column.setInputs(indices)

    def initCellConnections(self):
        self.cell_connections = [[[] for i in range(self.col_count)] for k in range(self.col_height)]
        #For every Column
        for i in range(self.col_count):
            #For every Cell
            for j in range(self.col_height):

                for k in range(5):
                    #Select Column
                    col_ind = random.randint(0,self.col_count)
                    #Select Cell
                    cel_ind = random.randint(0,self.col_height)
                    self.cell_connections[j][i].append([col_ind,cel_ind])

        for col in self.cell_connections:
            print(col)

    def spatialStep(self, input):
        self.active_columns = []

        # Overlap
        for column in self.columns:
            column.countOverlap(input)

        # Inhibition
        for index, column in enumerate(self.columns):

            n_start = max(0, index - self.inhibition_radius)
            n_end = min(self.col_count, index + self.inhibition_radius)

            neighbors = self.columns[n_start:n_end]
            neighbor_overlaps = [neig.overlap_count for neig in neighbors]

            neighbor_overlaps.sort(reverse=True)
            min_local_activity = neighbor_overlaps[min(
                self.desired_local_activity, len(neighbor_overlaps)-1)]

            if column.overlap_count > 0 and column.overlap_count >= min_local_activity:
                self.active_columns.append(column)

        # Learning
        for column in self.active_columns:
            column.modifyConnections(input)

    def temporalStep(self):
        for column in self.active_columns:
            column.activate()

    def listColumns(self):
        temp = [[c.state for c in col.cells] for col in self.columns]
        return np.array(temp).T.tolist()

    def listColumnOverlaps(self):
        return [col.overlap_count for col in self.columns]

    def listActiveColumnOverlaps(self):
        return [col.overlap_count if col in self.active_columns else 0 for col in self.columns]


layer = Layer(
    col_count=100,
    col_height=4,
    input_size=100,
    input_ratio=0.99,
    inhibition_radius=80,
    desired_local_activity=2)

layer.initMiniColumns()
layer.initConnections()
layer.initCellConnections()

samp_inp = [0 for _ in range(100)]
for i in range(5, 15):
    samp_inp[i] = 1

layer.spatialStep(samp_inp)
layer.temporalStep()

all_columns = [column.overlap_count for column in layer.columns]
act_columns = [
    1 if column in layer.active_columns else 0 for column in layer.columns]

print(f'SRD: {sum(act_columns) / layer.col_count}')


f, ax = plt.subplots(4, 1)

ax[0].imshow([samp_inp], cmap='gray')
ax[0].set_title('Input')

ax[1].imshow([layer.listColumnOverlaps()], cmap='gray')
ax[1].set_title('All Columns')

ax[2].imshow([layer.listActiveColumnOverlaps()], cmap='gray')
ax[2].set_title('Active Columns')

ax[3].imshow(layer.listColumns(), cmap='gray')
ax[3].set_title('Columns')

plt.show()
