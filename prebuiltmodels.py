import pybullet as p
import utils
plane_shape, floor = utils.setup_env(p)

import os
robot = p.loadURDF(os.path.join(pd.getDataPath(), 'r2d2.urdf'))
sam = p.loadURDF(os.path.join(pd.getDataPath(), 'samurai.urdf'))

p.setGravity(0, 0, -10)
utils.wait_ctrl_c(p)
