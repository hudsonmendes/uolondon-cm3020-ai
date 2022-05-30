import pybullet as p
import utils

p.connect(p.GUI)

floor_shape = p.createCollisionShape(p.GEOM_PLANE)
floor = p.createMultiBody(floor_shape, floor_shape)

box_shape = p.createCollisionShape(p.GEOM_BOX, halfExtents = [1, 1, 1])
box_object1 = p.createMultiBody(box_shape,box_shape)
box_object2 = p.createMultiBody(box_shape,box_shape)
p.resetBasePositionAndOrientation(box_object1, [0, -1, 2], [0, 0, 0, 1])
p.resetBasePositionAndOrientation(box_object2, [0, 1, 2], [0, 0, 0, 1])
p.setGravity(0, 0, -10)
p.setRealTimeSimulation(1)
utils.wait_ctrl_c(p)