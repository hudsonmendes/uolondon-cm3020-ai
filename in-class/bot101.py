import pybullet as p
import utils
plane_shape, floor = utils.setup_env(p)

bot101 = p.loadURDF('bot101.urdf')
p.setJointMotorControl2(bot101, 0, controlMode=p.VELOCITY_CONTROL, targetVelocity=0.25, targetPosition=0.5)
p.setJointMotorControl2(bot101, 1, controlMode=p.POSITION_CONTROL, targetVelocity=0.5, targetPosition=0.25)

utils.wait_ctrl_c(p)
