from util.cf_interface import CFDroneControls

if __name__ == "__main__":
    cfdc = CFDroneControls('yamls/cf_test_1.yaml')
    # cfdc.get_params()
    # cfdc.dump_yaml()
    cfdc.set_params()
    cfdc.basic_step_test()
    cfdc.disconnect()