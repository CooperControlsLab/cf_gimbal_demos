from util.cf_interface import CFDroneControls, CommandValues


if __name__ == "__main__":
    cfdc = CFDroneControls('yamls/cf_test_1.yaml')
    # cfdc.get_params()
    # cfdc.dump_yaml()
    i = CommandValues(0,0,0,40000)
    f = CommandValues(0,30,0,40000)
    cfdc.set_params()
    cfdc.basic_step_test()
    # cfdc.basic_step_test(init_command=i, step_command=f, step_time=5)
    cfdc.disconnect()