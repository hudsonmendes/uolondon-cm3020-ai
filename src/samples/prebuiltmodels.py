import pybullet as p
import pybullet_data as pd
from .. import utils

p.connect(p.GUI)

plane_shape = p.createCollisionShape(p.GEOM_PLANE)
floor = p.createMultiBody(plane_shape, plane_shape)

import os
robot = p.loadURDF(os.path.join(pd.getDataPath(), 'r2d2.urdf'))
sam = p.loadURDF(os.path.join(pd.getDataPath(), 'samurai.urdf'))

p.setGravity(0, 0, -10)
utils.wait_ctrl_c(p)
