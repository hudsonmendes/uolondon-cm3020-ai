
def load_bg(p):
    import os
    import pybullet_data as pd
    bg = p.loadURDF(os.path.join(pd.getDataPath(), 'samurai.urdf'))

def  setup_env(p):
    p.connect(p.GUI)
    p.setPhysicsEngineParameter(enableFileCaching=0)
    p.configureDebugVisualizer(p.COV_ENABLE_GUI, 0)
    plane_shape = p.createCollisionShape(p.GEOM_PLANE)
    floor = p.createMultiBody(plane_shape, plane_shape)
    return plane_shape, floor

def wait_ctrl_c(p):
    print("Press CTRL+C to interrupt...")
    import time
    while True:
        p.stepSimulation()
        time.sleep(1.0/240)