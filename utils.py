
def load_bg(p):
    import os
    import pybullet_data as pd
    bg = p.loadURDF(os.path.join(pd.getDataPath(), 'samurai.urdf'))

def wait_ctrl_c(p):
    print("Press CTRL+C to interrupt...")
    import time
    while True:
        p.stepSimulation()
        time.sleep(1.0/240)