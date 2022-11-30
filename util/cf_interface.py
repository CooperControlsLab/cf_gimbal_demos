import logging
import time

import cflib.crtp
from cflib.crazyflie import Crazyflie
from cflib.utils.callbacks import Caller
from cflib.utils import uri_helper
from cflib.crazyflie.syncCrazyflie import SyncCrazyflie
from cflib.crazyflie.log import LogConfig

from threading import Thread
import yaml
from util.dict_search import nested_search
from util.data_struct import DataStruct
import numpy as np

class CommandValues(dict):
    def __init__(self, r=0.0, p=0.0, ydot=0.0, thrust=0):
        self['roll'] = r
        self['pitch'] = p
        self['yawdot'] = ydot
        self['thrust'] = thrust

class CFBase:
    def __init__(self):
        pass
    def connect(self):
        pass
    def set_params(self):
        pass
    def get_params(self):
        pass

class CFDroneControls(CFBase):
    def __init__(self, params_file):
        self.current_command = CommandValues()
        self.connected = False
        self.step_test_completed = False
        self.step_test_data = DataStruct()
        self.step_test_data2 = DataStruct()
        try:
            if type(params_file) is str:
                self.params_dict = yaml.safe_load(open(params_file, 'r'))
            else:
                self.params_dict = yaml.safe_load(params_file)
            self.initialized = True
        except Exception as e:
            print(e)
            print("CFDroneControls class not initiated!")
            self.params_dict = None
            self.initialized = False
        self.address = self.params_dict['cf']['address']
        self.connect()
    
    def async_log(self, scf, logconf, logconf2):
        cf = scf.cf
        cf.log.add_config(logconf)
        cf.log.add_config(logconf2)
        logconf.data_received_cb.add_callback(self.log_callback)
        logconf2.data_received_cb.add_callback(self.log_callback2)
        logconf.start() #TODO: need to move this somewhere else
        logconf2.start()
        # time.sleep(5) #TODO: REMOVE
        # logconf.stop() #TODO: Need to move this somewhere else as well
        while self.step_test_completed is False:
            time.sleep(0.5)
        logconf.stop()
        logconf2.stop()

    def log_callback(self, timestamp, data, logconf):
        # TODO: Make this store data into an array, then push to CSV
        self.step_test_data.timestamps.append(timestamp)
        self.step_test_data.data.append(data)
        self.step_test_data.input.append(self.current_command)
        # print('[%d][%s]: %s' % (timestamp, logconf.name, data))
    def log_callback2(self, timestamp, data, logconf):
        # TODO: Make this store data into an array, then push to CSV
        self.step_test_data2.timestamps.append(timestamp)
        self.step_test_data2.data.append(data)
        self.step_test_data2.input.append(self.current_command)
        # print('[%d][%s]: %s' % (timestamp, logconf.name, data))

    def connect(self):
        try:
            uri = uri_helper.uri_from_env(default=self.address)
            cflib.crtp.init_drivers(enable_debug_driver=False)
            self.cf = Crazyflie(rw_cache='./cache')

            self.lg_stab = LogConfig(name='Stabilizer', period_in_ms=10)
            self.lg_stab2 = LogConfig(name='MotorOutput', period_in_ms=10)
            self.lg_stab.add_variable('stabilizer.roll', 'float')
            self.lg_stab.add_variable('stabilizer.pitch', 'float')
            self.lg_stab.add_variable('stateEstimateZ.rateRoll', 'float')
            self.lg_stab.add_variable('stateEstimateZ.ratePitch', 'float')
            self.lg_stab.add_variable('controller.pitchRate', 'float')
            self.lg_stab.add_variable('controller.rollRate', 'float')
            self.lg_stab2.add_variable('motor.m1', 'float')
            self.lg_stab2.add_variable('motor.m2', 'float')
            self.lg_stab2.add_variable('motor.m3', 'float')
            self.lg_stab2.add_variable('motor.m4', 'float')

            self.scf = SyncCrazyflie(uri, cf=self.cf)
            self.log_thread = Thread(target=self.async_log, args=(self.scf, self.lg_stab, self.lg_stab2))

            self.cf.open_link(uri)
            print(f"Sucessfully connected to {self.address}")
            self.connected = True
        except Exception as e:
            print(e)
            print("Couldn't connect!")
            self.connected = False

    def disconnect(self):
        self.cf.close_link()

    def set_params(self):
        groupKeys = list(nested_search(self.params_dict, ['cf', 'params']))
        for k in groupKeys:
            names = self.params_dict['cf']['params'][k]
            for k2 in names:
                keyName = k + '.' + k2
                value = nested_search(self.params_dict, ['cf', 'params', k, k2])
                try:
                    self.cf.param.set_value(keyName, value)
                    print(f"sucessfully set {keyName} : {value}")
                except:
                    print(f"couldn't set {keyName}")

    # Remember params in cf, fullnames are group.name, pid_rate.roll_kp for example
    def get_params(self):
        print("Getting params from crazyflie")
        x=self.params_dict
        groupKeys = list(self.params_dict['cf']['params'])
        for k in groupKeys:
            names = self.params_dict['cf']['params'][k]
            for k2 in names:
                keyName = k + '.' + k2
                try:
                    val = self.cf.param.get_value(keyName, None)
                    try:
                        val = float(val)
                    except:
                        print("val is not a float")
                    x['cf']['params'][k][k2] = val
                    print(f"{keyName} : {val}")
                except:
                    print(f"key: {k2} does not exist")
                    x['cf']['params'][k][k2] = None
        self.pulled_params = x
    
    def dump_yaml(self, filename='yamls/cf_last_pulled.yaml'):
        yaml.dump(self.pulled_params, open(filename, 'w'))
    
    def basic_step_test(self, filename='default.csv', initial=CommandValues(),step=CommandValues(),steptime=1):

        self.step_test_completed = False
        self.log_thread.start()
        cmd0 = CommandValues()
        cmd1 = initial
        cmd2 = step
        # First send zero commands to start
        print(f"Sending: {cmd0}")
        self.send_command(cmd0)
        print(f"Sending: {cmd1}")
        self.current_command = cmd1
        for i in range(int(steptime/0.1)):
            self.send_command(cmd1)
            time.sleep(0.1)
        
        self.current_command = cmd2
        print(f"Sending: {cmd2}")
        for i in range(int(steptime/0.1)):
            self.send_command(cmd2)
            time.sleep(0.1)
        
        self.current_command = cmd1
        print(f"Sending: {cmd1}")
        for i in range(int(steptime/0.1)):
            self.send_command(cmd1)
            time.sleep(0.1)
        self.send_command(cmd0)

        self.step_test_completed = True
        print(f"DONE...Creating {filename}")
        self.step_test_data.to_csv(filename)

    def send_command(self, cmd: CommandValues):
        self.cf.commander.send_setpoint(cmd['roll'], cmd['pitch'], cmd['yawdot'], cmd['thrust'])

    def trajectory_test(self, filename = 'default.csv', filename2 = 'default2.csv', freq=1, amplitude=20, duration=10, thrust=40000):
        
        self.step_test_completed = False
        self.log_thread.start()
        cmd0 = CommandValues()
        cmd1 = CommandValues(0,0,0,thrust)
        cmd2 = CommandValues(0,0,0,thrust)
        steptime=5
        # First send zero commands to start
        print(f"Sending: {cmd0}")
        self.send_command(cmd0)
        print(f"Sending: {cmd1}")
        self.current_command = cmd1
        for i in range(int(steptime/0.1)):
            self.send_command(cmd1)
            time.sleep(0.1)
        
        start_time_ns = time.time_ns() #Time in nanoseconds
        start_time = start_time_ns/1000000000.0
        current_time = start_time

        print(f"Starting!!! | Time: {current_time}")
        # Send in trajectory commands
        while duration > current_time - start_time:
            current_time = (time.time_ns()/1000000000.0) 
            norm_time = current_time - start_time
            roll = amplitude*np.cos(2*np.pi*freq*norm_time)
            pitch = amplitude*np.sin(2*np.pi*freq*norm_time)
            cmd = CommandValues(roll,pitch,0,thrust)
            self.current_command = cmd
            self.send_command(cmd)
            time.sleep(0.01)
            print(f"Time: {current_time} | Command: {cmd}")

        self.step_test_completed = True
        print(f"DONE...Creating {filename}")
        self.step_test_data.to_csv(filename)
        self.step_test_data2.to_csv(filename2)