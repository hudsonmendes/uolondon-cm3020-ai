import pybullet as p
import utils
plane_shape, floor = utils.setup_env(p)

bot101 = p.loadURDF('bot101.urdf')

print(p.isNumpyEnabled())
p.setGravity(0, 0, -10)
utils.wait_ctrl_c(p)
