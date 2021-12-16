import re
from time import sleep
from vispy import scene, app, color
from vispy.scene import visuals
from vispy.visuals import MarkersVisual
import numpy as np
from multiprocessing import Process

from vpython.vpython import canvas

from config import COLUMN_COUNT, COLUMN_HEIGHT, INPUT_SIZE, SPATIAL_CONNECTION_COUNT


class COLORS:
    DEFAULT = [1, 1, 1]
    INACTIVE = [1, 1, 1]
    ACTIVE = [0, 1, 0]


class InputVisual:
    def __init__(self, parent, x_range, y_range) -> None:

        self.colors = np.ones((INPUT_SIZE, 3), dtype=np.float32)
        self.cell_poses = self.initCellPoses(x_range, y_range)
        self.cells = scene.visuals.Markers(
            pos=self.cell_poses,
            edge_width=0,
            face_color=self.colors,
            parent=parent,
            symbol='square',
            scaling=True
        )

    def initCellPoses(self, x_range, y_range):
        poses = np.empty((INPUT_SIZE, 3))
        poses[:, 0] = np.linspace(x_range[0], x_range[1], INPUT_SIZE)
        poses[:, 1] = 0
        poses[:, 2] = y_range[0]
        return poses

    def updateWinners(self, winner_columns):
        self.colors[:] = COLORS.INACTIVE
        self.colors[winner_columns] = COLORS.ACTIVE
        self.cells.set_data(pos=self.cell_poses,
                            face_color=self.colors, edge_width=0)

class SpatialConVisual:
    def __init__(self,parent) -> None:
        self.connections = scene.visuals.Line(
            parent=parent,
            
        )

    def updatePermenance(self,permenance):
        pass

    def initConnections(self,connections):
        pass


class ColumnVisual:
    def __init__(self, parent, x_range, z_range) -> None:
        self.cell_poses = self.initCellPoses(x_range, z_range[0])
        self.cells = scene.visuals.Markers(
            parent=parent,
            pos=self.cell_poses.reshape((-1, 3)),
            symbol='square',
            edge_width=0,
            scaling=True
        )

    def initCellPoses(self, x_range, z_start):
        column_distance = (abs(x_range[0]) + abs(x_range[1])) / COLUMN_COUNT

        y_range = (z_start, z_start - (COLUMN_HEIGHT * column_distance))

        xs = np.linspace(x_range[0], x_range[1],
                         COLUMN_COUNT, dtype=np.float32)
        zs = np.linspace(y_range[0], y_range[1],
                         COLUMN_HEIGHT, dtype=np.float32)

        poses = np.array(np.meshgrid(xs, [0], zs)).T.reshape(
            (COLUMN_COUNT, COLUMN_HEIGHT, 3))


        return poses


class HTMVisual:
    def __init__(self) -> None:

        self.canvas = scene.SceneCanvas(
            keys='interactive', bgcolor='black', show=True, fullscreen=True)

        self.view = self.canvas.central_widget.add_view()
        self.view.camera = scene.cameras.TurntableCamera(distance=1200)

        self.input_visuals = InputVisual(
            self.view.scene, (-1000, 1000), (-100,))
        self.column_visuals = ColumnVisual(
            self.view.scene, (-1000, 1000), (300,))


        self.connections_poses = np.empty((COLUMN_COUNT,SPATIAL_CONNECTION_COUNT,2,3))
        self.connections = scene.visuals.Line(
            parent=self.view.scene,
            pos=np.random.uniform(-400, 400, (40, 2, 3)),
            connect='segments'
        )

        

    def initConnections(self, connections):
        column_poses=self.column_visuals.cell_poses
        input_poses= self.input_visuals.cell_poses
        connected_poses= input_poses[connections]

        connections = []
        for column in column_poses:
            pass


    def updateWinners(self,winner_columns):
        self.input_visuals.updateWinners(winner_columns)



htm = HTMVisual()
#htm.initConnections(0)



