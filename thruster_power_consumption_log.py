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
        print("Please input thruster strength[%]")
        print("0-100[%]")
        input_value = int(input())
        if input_value < 0 or input_value > 100:
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

def set_RC_mode():
    i2cbus.write_i2c_block_data(arduino, 0, [0, 0])

def control_thruster(cmd):
    i2cbus.write_i2c_block_data(arduino, 2, cmd)

# get date time object
detail = datetime.datetime.now()
date = detail.strftime("%Y%m%d%H%M%S")
# open csv file
file = open('./csv/'+ date +'.csv', 'a', newline='')
csvWriter = csv.writer(file)
data_items = ['count', 'latitude', 'longitude', 'yaw', 'cmd',
                'pwm', 'voltage', 'current', 'power_consumption', 'kJ_poewr_consumption', 'accum_power_consumption', 'distance']
csvWriter.writerow(data_items)

try:
    strength = int(input_mode())
    signal.signal(signal.SIGALRM, logging)
    signal.setitimer(signal.ITIMER_REAL, 0.5, interval)
    cmd = [1, strength]
    while BIWAKO.count < 5.0:
        control_thruster(cmd)
        time.sleep(0.2)
    set_RC_mode()
    for i in range(len(log_data)):
        csvWriter.writerow(log_data[i])
    file.close() 
    
except KeyboardInterrupt:
    set_RC_mode()
    for i in range(len(log_data)):
        csvWriter.writerow(log_data[i])
    file.close()

