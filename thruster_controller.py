import os
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
is_first = 0

frequency = 100 # [Hz]
interval = 1/frequency # [s]

# mode determination method
def input_mode():
    while True:
        print("Please select a control mode")
        print("0: RC mode, 1: Auto mode, 2: Manual mode, 3: END, 4: Time, 5: Gradation")
        input_value = int(input())
        if input_value < 0 or input_value > 5:
            print("Invalid value. Input again")
        else:
            return input_value

# robot action determination method
def input_performance_number():
    while True:
        print("Please input robot performance number")
        print("=================================================================")
        print("4 thrusters drive mode")
        print("0:Stop, 1: Positive, 2: Negative, 3: Left, 4: Right, 5:CW, 6: CCW")
        print("=================================================================")
        print("Diagonal drive mode")
        print("7: First quadrant, 8: Second quadrant, 9: Third quadrant, 10: Forth quadrant")
        print("=================================================================")
        print("2 thrusters drive mode (Push)")
        print("11: Positive, 12: Negative, 13: Left, 14: Right")
        print("=================================================================")
        print("2 thrusters drive mode (Pull)")
        print("15: Positive, 16: Negative, 17: Left, 18: Right")
        print("=================================================================")
        input_value = int(input("Command: "))
        if input_value < 0 or input_value > 18:
            print("Invalid number. Input again")
        else:
            if input_value == 0:
                print("Stop")
            elif input_value == 1:
                print("Positive")
            elif input_value == 2:
                print("Negative")
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
        input_value = int(input("Power: "))
        if input_value < 0.0 or input_value > 100.0:
            print("Invalid value. Input again")
        else:
            return input_value

# logging function
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

def time_count_control(action, power1, power2):
    exp_time = 5.0
    diff = 0.0
    power = power1
    st = time.perf_counter()
    ed = 0.0
    is_first = 0
    mode_value = 2
    cmd = [action, power]
    i2cbus.write_i2c_block_data(arduino, mode_value, cmd)
    while True:
        try:
            ed = time.perf_counter()
            if diff > exp_time and is_first==0:
                print(diff)
                st = time.perf_counter()
                ed = time.perf_counter()
                power = power2
                cmd = [action, power]
                i2cbus.write_i2c_block_data(arduino, mode_value, cmd)
                is_first = 1
            diff = ed - st
            if diff > exp_time and is_first==1:
                print(diff)
                power = 0
                cmd = [0, power]
                i2cbus.write_i2c_block_data(arduino, 0, cmd)
                csv_file_write()
                break
        except KeyboardInterrupt:
            cmd = [0, 0]
            i2cbus.write_i2c_block_data(arduino, 0, cmd)
            break

# the thruster is controled by given power to zero gradually
def gradation_control(action, power):
    duration = 1.0
    diff = 0.0
    mode_value = 2
    st = time.perf_counter()
    ed = 0.0
    cmd = [0, 0]
    i2cbus.write_i2c_block_data(arduino, 0, cmd)
    time.sleep(1)
    cmd = [action, power]
    i2cbus.write_i2c_block_data(arduino, mode_value, cmd)
    while True:
        try:
            ed = time.perf_counter()
            diff = ed - st
            if diff > duration:
                st = time.perf_counter()
                ed = time.perf_counter()
                power = power - 5
                cmd = [action, power]
                i2cbus.write_i2c_block_data(arduino, mode_value, cmd)
                if power < 10.0:
                    power = 0.0
                    cmd = [action, power]
                    i2cbus.write_i2c_block_data(arduino, mode_value, cmd)
                    break
        except KeyboardInterrupt:
            cmd = [0, 0]
            i2cbus.write_i2c_block_data(arduino, 0, cmd)
            break


# get date time object
def csv_file_make():
    detail = datetime.datetime.now()
    date = detail.strftime("%Y%m%d%H%M%S")
    # open csv file
    file_name = './csv/'+ date +'.csv'
    file = open(file_name, 'a', newline='')
    csvWriter = csv.writer(file)
    data_items = ['count', 'latitude', 'longitude', 'yaw', 'cmd',
                    'pwm', 'voltage', 'current', 'power_consumption', 'kJ_poewr_consumption', 'accum_power_consumption', 'distance']
    csvWriter.writerow(data_items)
    return file_name, file

def csv_file_write():
    detail = datetime.datetime.now()
    date = detail.strftime("%Y%m%d%H%M%S")
    # open csv file
    file_name = './csv/'+ date +'.csv'
    file = open(file_name, 'a', newline='')
    csvWriter = csv.writer(file)
    data_items = ['count', 'latitude', 'longitude', 'yaw', 'cmd',
                    'pwm', 'voltage', 'current', 'power_consumption', 'kJ_poewr_consumption', 'accum_power_consumption', 'distance']
    csvWriter.writerow(data_items)
    if os.path.isfile(file_name):
        for i in range(len(log_data)):
            csvWriter.writerow(log_data[i])
        file.close()


def kill_signal_process(arg1, args2):
    pass

# init the variables value
mode_value = 0
action_value = 0
power_value = 0

# make a csv file only one time
file_name = ''
file_make = 0

# define time variables
st = time.perf_counter()
ed = 0.0

signal.signal(signal.SIGALRM, logging)
signal.setitimer(signal.ITIMER_REAL, 0.01, interval)

# main loop
while True:
    try:
        mode_value = input_mode()
        if mode_value == 0 or mode_value == 1 or mode_value == 3 or mode_value == 4:
            cmd = [0, 0]
            i2cbus.write_i2c_block_data(arduino, mode_value, cmd)
        if mode_value == 2:
            if file_make == 0:
                file_name, file = csv_file_make()
                csvWriter = csv.writer(file)
                file_make = 1
            action_value = input_performance_number()
            if 1 <= action_value <= 18:
                power_value = input_power()
            elif action_value == 0:
                power_value = 0
            cmd = [action_value, power_value]
            print(cmd)
            i2cbus.write_i2c_block_data(arduino, mode_value, cmd)
        if mode_value == 3:
            cmd = [0, 0]
            i2cbus.write_i2c_block_data(arduino, 0, cmd)
            if os.path.isfile(file_name):
                for i in range(len(log_data)):
                    csvWriter.writerow(log_data[i])
                file.close()
            time.sleep(1)
            break
        if mode_value == 4:
            action_value = input_performance_number()
            if 1 <= action_value <= 18:
                power_value1 = input_power()
                power_value2 = input_power()
            elif action_value == 0:
                power_value = 0
            time_count_control(action_value, power_value1, power_value2)
            break
        if mode_value == 5:
            action_value = input_performance_number()
            if 1 <= action_value <= 18:
                power_value = input_power()
            elif action_value == 0:
                power_value = 0
            gradation_control(action_value, power_value)
            break


    except KeyboardInterrupt:
        cmd = [0, 0]
        i2cbus.write_i2c_block_data(arduino, 0, cmd)
        time.sleep(1)
        signal.signal(signal.SIGALRM, kill_signal_process)
        signal.setitimer(signal.ITIMER_REAL, 0.1, 0.1)
        break
