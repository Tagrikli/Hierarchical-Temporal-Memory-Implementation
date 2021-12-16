import enum
from vpython import *
import numpy as np
from config import CELL_STATE, COLUMN_COUNT, COLUMN_HEIGHT, INPUT_SIZE, SPATIAL_CONNECTION_COUNT


scene = canvas(width=2400,height=1300)



class InputLayerVisual:
    def __init__(self, x_range, y_range) -> None:
        self.cell_size = 0
        self.poses = self.__initPoses(x_range, y_range)
        self.cells = self.__initCells()

        self.colors = [color.white, color.green, color.orange]

    def __initCells(self):
        boxes = []
        for pos in self.poses:
            boxes.append(
                box(pos=vector(pos[0], pos[1], 0),
                    height=self.cell_size,
                    length=self.cell_size,
                    width=self.cell_size
                    )
            )
        return boxes

    def updateInput(self, data):
        for index, value in enumerate(data):
            self.cells[index].color = self.colors[value]

    def __initPoses(self, x_range, y_range):

        self.cell_size = ((abs(x_range[0]) + abs(x_range[1]))/INPUT_SIZE) * 0.7

        poses = np.empty((INPUT_SIZE, 2), dtype=np.float32)
        poses[:, 0] = np.linspace(
            x_range[0], x_range[1], INPUT_SIZE, dtype=np.float32)
        poses[:, 1] = y_range[0]
        return poses

    def getPositions(self):
        return self.poses


class ColumnsVisual:
    def __init__(self, x_range, y_range) -> None:

        self.cell_size = 0
        self.cell_poses = self.__initPoses(x_range, y_range[0])
        self.columns = self.__initColumns()


    def __initColumns(self):
        columns = []
        for column in self.cell_poses:
            temp = []
            for cell in column:
                temp.append(
                    box(pos=vector(cell[0], cell[1], 0),
                        width=self.cell_size,
                        length=self.cell_size,
                        height=self.cell_size)
                )
            columns.append(temp)
        return columns

    def __initPoses(self, x_range, y_start):

        column_distance = (abs(x_range[0]) + abs(x_range[1])) / COLUMN_COUNT
        self.cell_size = (column_distance) * 0.7

        y_range = (y_start, y_start - (COLUMN_HEIGHT * column_distance))

        xs = np.linspace(x_range[0], x_range[1],
                         COLUMN_COUNT, dtype=np.float32)
        ys = np.linspace(y_range[0], y_range[1],
                         COLUMN_HEIGHT, dtype=np.float32)

        poses = np.array(np.meshgrid(xs, ys)).T.reshape(
            COLUMN_COUNT, COLUMN_HEIGHT, 2)


        return poses


class HTMVisual():
    def __init__(self) -> None:
        self.input_layer = InputLayerVisual((-100, 100), (0,))
        self.columns = ColumnsVisual((-100, 100), (30,))

        self.spatial_connections = []

    def updateConnections(self, connections,permenance):
        

        for col_ind in range(COLUMN_COUNT):

            for ind,con_ind in enumerate(connections[col_ind]):
                begin = vector(
                    self.columns.cell_poses[col_ind, -1][0], self.columns.cell_poses[col_ind, -1][1] - self.columns.cell_size/2, 0)
                end = vector(
                    self.input_layer.poses[con_ind][0], self.input_layer.poses[con_ind][1] + self.input_layer.cell_size/2, 0)
                curve(begin, end, radius=0.2, opacity=permenance[col_ind][ind]/10)



    def updateInput(self, data):
        self.input_layer.updateInput(data)

    def updatePermenance(self,data):

        self.spatial_connections[13][0].color = color.red


        # for col_data,col_cons in zip(data,self.connections):
        #     for perm_data, perm_curve in zip(col_data,col_cons):
        #         print(perm_curve)
        #         perm_curve.color = color.red
                


htm = HTMVisual()
