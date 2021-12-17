import csv
import signal
import math
import datetime
import time
from INA226 import INA226
from robot import Robot
from smbus import SMBus

BIWAKO = Robot(way_point=[0.0, 0.0])
power_sensor_addr = 0x40
power_sensor = INA226(power_sensor_addr)
power_sensor.initial_operation()
arduino = 0x04
i2cbus = SMBus(1)
log_data = []

frequency = 100 # [Hz]
interval = 1/frequency # [s]

# mode determination method
def input_mode():
    while True:
        print("Please select a control mode")
        print("0: RC mode, 1: Auto mode, 2: Manual mode, 3: END")
        input_value = int(input())
        if input_value < 0 or input_value > 3:
            print("Invalid value. Input again")
        else:
            return input_value

# robot action determination method
def input_performance_number():
    while True:
        print("Please input robot performance number")
        print("0:Stop, 1: Forward, 2: Backward, 3: Left, 4: Right, 5:CW, 6: CCW")
        input_value = int(input())
        if input_value < 0 or input_value > 6:
            print("Invalid number. Input again")
        else:
            if input_value == 0:
                print("Stop")
            elif input_value == 1:
                print("Forward")
            elif input_value == 2:
                print("Backward")
            elif input_value == 3:
                print("Left")
            elif input_value == 4:
                print("Right")
            elif input_value == 5:
                print("CW")
            elif input_value == 6:
                print("CCW")
            return input_value

# thruster power determination method
def input_power():
    while True:
        print("Please input thruster power")
        print("0 - 100 [%]")
        input_value = int(input())
        if input_value < 0.0 or input_value > 100.0:
            print("Invalid value. Input again")
        else:
            return input_value

def logging(arg1, args2):
    v = power_sensor.get_voltage()
    c = power_sensor.get_current()
    p = power_sensor.get_power()
    kJ = p/1000
    BIWAKO.count = BIWAKO.count + interval
    BIWAKO.consumed_energy = BIWAKO.consumed_energy + kJ
    data = [BIWAKO.count, BIWAKO.lat, BIWAKO.lon, math.degrees(BIWAKO.yaw),
            BIWAKO.cmd, BIWAKO.pwm, v, c, p, kJ, BIWAKO.consumed_energy, BIWAKO.diff_distance]
    log_data.append(data)

def kill_signal_process(arg1, args2):
    pass

# init the variables value
mode_value = 0
performance_value = 0
power_value = 0

# get date time object
detail = datetime.datetime.now()
date = detail.strftime("%Y%m%d%H%M%S")
# open csv file
file = open('./csv/'+ date +'.csv', 'a', newline='')
csvWriter = csv.writer(file)
data_items = ['count', 'latitude', 'longitude', 'yaw', 'cmd',
                'pwm', 'voltage', 'current', 'power_consumption', 'kJ_poewr_consumption', 'accum_power_consumption', 'distance']
csvWriter.writerow(data_items)

signal.signal(signal.SIGALRM, logging)
signal.setitimer(signal.ITIMER_REAL, 0.01, interval)

strength1 = int(input_power())
strength2 = int(input_power())
strength = strength1
st = time.perf_counter()
ed = 0.0
is_first = 0
# main loop
while True:
    try:
        mode_value = 2
        cmd = [1, strength]
        i2cbus.write_i2c_block_data(arduino, mode_value, cmd)
        time.sleep(0.1)
        """
        
        ed = time.perf_counter()
        if ed - st > 5.0 and is_first==0:
            st = time.perf_counter()
            ed = 0.0
            strength = strength2
            is_first = 1
        if ed - st > 5.0 and is_first==1:
            strength = 0
            cmd = [1, strength]
            i2cbus.write_i2c_block_data(arduino, 0, cmd)
            for i in range(len(log_data)):
                csvWriter.writerow(log_data[i])
            file.close()

        """
    except KeyboardInterrupt:
        for i in range(len(log_data)):
            csvWriter.writerow(log_data[i])
        file.close()
        cmd = [0, 0]
        i2cbus.write_i2c_block_data(arduino, 0, cmd)
        time.sleep(1)
        signal.signal(signal.SIGALRM, kill_signal_process)
        signal.setitimer(signal.ITIMER_REAL, 0.1, 0.1)
        break
