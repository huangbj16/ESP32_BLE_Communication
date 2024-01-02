# In settings.json first activate computer vision mode:
# https://github.com/Microsoft/AirSim/blob/main/docs/image_apis.md#computer-vision-mode

import airsim

# requires Python 3.5.3 :: Anaconda 4.4.0
# pip install opencv-python
import time
import sys

class AirSim_Module:
    def __init__(self):
        self.client = airsim.MultirotorClient()
        print("AirSim Connected!")

    def get_distance_by_sensor(self, sensor_id):
        return self.client.getDistanceSensorData(sensor_id)


if __name__ == "__main__":
    frameCount = 0
    startTime = time.time()
    fps = 0
    motor_num = 5
    is_trigger_array = [False for _ in range(motor_num)]
    airsim_control = AirSim_Module()
    while True:
        for i in range(motor_num):
            rawDistance = airsim_control.get_distance_by_sensor("Distance"+str(i+1))
            if rawDistance.distance <= 2.0 and not is_trigger_array[i]:
                is_trigger_array[i] = True
                # print("distance sensor ", i, "triggered")
                # trigger vibration i
            if rawDistance.distance > 2.0 and is_trigger_array[i]:
                is_trigger_array[i] = False
                # print("distance sensor ", i, "canceled")
                # stop vibration i

        frameCount = frameCount  + 1
        endTime = time.time()
        diff = endTime - startTime
        if (diff > 1):
            fps = frameCount
            print(fps)
            frameCount = 0
            startTime = endTime
