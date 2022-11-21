import logging
import time

import cflib.crtp
from cflib.crazyflie import Crazyflie
from cflib.utils.callbacks import Caller
from cflib.utils import uri_helper

from threading import Thread

# URI to the Crazyflie to connect to
uri = uri_helper.uri_from_env(default='radio://0/100/2M/E7E7E7E702')

logging.basicConfig(level=logging.ERROR)

def log_callback(timestamp, data, logconf):
    print('[%d][%s]: %s' % (timestamp, logconf.name, data))

if __name__ == '__main__':
    # Initialize the low-level drivers
    cflib.crtp.init_drivers(enable_debug_driver=False)

    # connected = Caller()

    cf = Crazyflie(rw_cache='./cache')
    # cf.connected.add_callback(connected)
    cf.open_link(uri)

    # # Set some values
    # cf.param.set_value('pid_rate.roll_kp', 0.1)
    # print(f"roll kp: {cf.param.get_value('pid_rate.roll_kff', 0)}")

    r=0.0
    p=0.0
    yawdot=0.0
    thrust=30000
    print("Send zero")
    cf.commander.send_setpoint(0.0, 0.0, 0, 0)
    print(f"send r:{r}, pitch:{p}, yawdot:{yawdot}, thrust:{thrust}")
    for i in range(50):
        cf.commander.send_setpoint(r, p, yawdot, thrust)
        time.sleep(0.1)
    r=10
    print(f"send r:{r}, pitch:{p}, yawdot:{yawdot}, thrust:{thrust}")
    for i in range(50):
        cf.commander.send_setpoint(r, p+30, yawdot, thrust)
        time.sleep(0.1)
    r=0
    print(f"send r:{r}, pitch:{p}, yawdot:{yawdot}, thrust:{thrust}")
    for i in range(50):
        cf.commander.send_setpoint(r, p, yawdot, thrust)
        time.sleep(0.1)
    
    cf.commander.send_setpoint(0,0,0,0)
    print("STOP!")

    cf.close_link()

            
