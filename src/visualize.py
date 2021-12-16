from vpython import *
import numpy as np

from config import CELL_STATE, COLUMN_COUNT, COLUMN_HEIGHT, INPUT_SIZE, SPATIAL_CONNECTION_COUNT


scene = canvas(width=1920, height=1080)


class InputVisual:
    def __init__(self, pos_range) -> None:
        self.input_boxes = []
        self.input_poses = np.linspace(pos_range[0], pos_range[1], INPUT_SIZE)
        self.input_box_size = (
            (abs(pos_range[0]) + abs(pos_range[1]))/INPUT_SIZE) * 0.9
        self.colors = [color.white, color.green, color.orange]

    def initBoxes(self):
        for x in self.input_poses:
            self.input_boxes.append(box(pos=vector(
                x, 0, 0), height=self.input_box_size, length=self.input_box_size, width=self.input_box_size))

    def updateInput(self, data):
        for index, value in enumerate(data):
            self.input_boxes[index].color = self.colors[value]

    def getPositions(self):
        return self.input_poses


class Columns:
    def __init__(self, col_range, cell_range) -> None:
        self.columns_poses = np.linspace(
            col_range[0], col_range[1], COLUMN_COUNT)
        self.col_dist = (abs(col_range[0]) + abs(col_range[1])) / COLUMN_COUNT
        self.cell_size = (self.col_dist) * 0.9

        self.cell_poses = np.linspace(
            cell_range[0], cell_range[0] - COLUMN_HEIGHT * self.col_dist, COLUMN_HEIGHT)

        self.columns = []
        self.connections = []
        self.input_poses = []

    def initColumns(self):
        for col_pos in self.columns_poses:
            column = []
            for cell_pos in self.cell_poses:
                column.append(box(pos=vector(col_pos, cell_pos, 0), height=self.cell_size,
                                  length=self.cell_size, width=self.cell_size))
            self.columns.append(column)

    def initConnections(self, connections):


        sxs = self.columns_poses
        sy = self.cell_poses[-1]

        

        sphere(pos=vector(sxs[4],sy,0),radius=2)

        # for col_ind, col_pos in enumerate(self.columns_poses):
        #     for conn in connections[col_ind]:
        #         curve(pos=[vector(col_pos, bottom, 0),
        #               vector(self.input_poses[conn], -10, 0)])


    def setInputPoses(self, poses):
        self.input_poses = poses


inputs = InputVisual((-10, 10))
inputs.initBoxes()

columns = Columns((-20, 20), (5,))
columns.initColumns()
columns.setInputPoses(inputs.getPositions())
columns.initConnections(0)


