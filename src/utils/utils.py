def wait_ctrl_c(p):
    print("Press CTRL+C to interrupt...")
    import time
    while True:
        p.stepSimulation()
        time.sleep(1.0/240)
