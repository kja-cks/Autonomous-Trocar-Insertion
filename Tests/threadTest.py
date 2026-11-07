import threading
import time
import queue
import random

tasks = queue.Queue()

def stereoSensing():
    #Simulating Data creation
    for i in range(5):
        data = i
        tasks.put(data)
        print(f"Estimated Depth: {i}")
        time.sleep(random.random())

def stepperMotorMovement():
    #simulating processing
    while True:
        try:
            data = tasks.get(timeout=5)
            print(f"position: {data}")
            time.sleep(random.random())
            tasks.task_done()
        except queue.Empty:
            print("no more data")
            break

stereoThread = threading.Thread(target=stereoSensing)
stepperThread = threading.Thread(target=stepperMotorMovement)

stereoThread.start()
stepperThread.start()

tasks.join()