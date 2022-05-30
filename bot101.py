import pybullet as p
import utils

p.connect(p.GUI)
p.setPhysicsEngineParameter(enableFileCaching=0)

plane_shape = p.createCollisionShape(p.GEOM_PLANE)
floor = p.createMultiBody(plane_shape, plane_shape)

bot101 = p.loadURDF('bot101.urdf')

print(p.isNumpyEnabled())
p.setGravity(0, 0, -10)
utils.wait_ctrl_c(p)
