from util.cf_interface import CFDroneControls, CommandValues
from util.data_struct import DataStruct

if __name__ == "__main__":
    try:
    
        csvfilename = input("Please enter a valid filename: ")
        csvfilename = 'csvs/' + csvfilename + '.csv'
    
        cfdc = CFDroneControls('yamls/cf_test_1.yaml')
        # cfdc.get_params()
        # cfdc.dump_yaml()
        i = CommandValues(0,0,0,40000)
        f = CommandValues(0,30,0,40000)
        cfdc.set_params()
        # cfdc.basic_step_test(csvfilename, i, f, steptime=5)
        cfdc.trajectory_test(csvfilename, freq = 0.25, amplitude = 20, duration=10, thrust=40000)
        cfdc.disconnect()

        # Plot data
        d = DataStruct()
        d.from_csv(csvfilename)
        d.plot_subplots()

    except Exception as e:
        print(e)