from argparse import ArgumentParser
parser = ArgumentParser()
parser.add_argument("--n_bots", type=int, default=10)
args = parser.parse_args()

import pybullet as p
import utils
plane_shape, floor = utils.setup_env(p)

from random import random
for _ in range(args.n_bots):
    botId = p.loadURDF('bot101.urdf')
    for jointIndex in range(p.getNumJoints(botId)):
        if random() > 0.5:
            p.setJointMotorControl2(
                botId,
                jointIndex,
                controlMode=p.VELOCITY_CONTROL,
                targetVelocity=max(0.25, random() * 10))
        else:
            p.setJointMotorControl2(
                botId,
                jointIndex,
                controlMode=p.POSITION_CONTROL,
                targetPosition=max(0.25, random() * 10))

utils.wait_ctrl_c(p)
