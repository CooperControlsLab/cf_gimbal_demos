import csv
import numpy as np
import matplotlib.pyplot as plt

class DataStruct:
    def __init__(self, ):
        self.timestamps = []
        self.data = []
        self.input = []
        self.names = []
        self.rawdata = []

    def to_csv(self, filename=None):
        try:
            if(filename==None):
                print("No filename given!")
                raise NameError
            keys = list(self.data[0].keys())
            keys.insert(0, 'timestamp')
            for a in list(self.input[0].keys()): keys.append(a)
            file = open(filename, 'w',newline='')
            writer = csv.writer(file, delimiter=',')
            writer.writerow(keys)
            for i in range(len(self.timestamps)):
                row = []
                row.append(self.timestamps[i])
                for j in list(self.data[i].values()):
                    row.append(j)
                for h in list(self.input[i].values()):
                    row.append(h)
                writer.writerow(row)
            file.close()
        except Exception as e: 
            print(e)

    def from_csv(self, filename=None):
        try:
            if(filename==None):
                print("No filename given!")
                raise NameError

            file = open(filename, 'r',newline='')
            self.rawdata = np.genfromtxt(file, delimiter=',',names=True,dtype=np.float64)
            self.names = self.rawdata.dtype.names

            file.close()
            # file = open(filename, 'r',newline='')
            # reader = csv.DictReader(file, fieldnames=names, delimiter=',')
            # listdata = list(reader)
            # for i in range(1,len(listdata)):
            #     self.timestamps.append(listdata[i]['timestamp'])
            #     del listdata[i]['timestamp']
            #     self.data.append(listdata[i])

            # file.close()

        except Exception as e: 
            print(e)

    def plot_unorganized(self):
        time = self.rawdata['timestamp']
        roll = self.rawdata['stabilizerroll']
        pitch = self.rawdata['stabilizerpitch']*-1 # for some reason it's inverted
        desiredpitchrate = self.rawdata['controllerpitchRate'] # pitchrate at controller is in deg/sec
        desiredrollrate = self.rawdata['controllerrollRate']
        rollrate = self.rawdata['stateEstimateZrateRoll']*180.0/(np.pi*1000.0)
        pitchrate = self.rawdata['stateEstimateZratePitch']*180.0/(np.pi*1000.0) # state estimate reading is in millirad/sec
        inputpitch = self.rawdata['pitch']
        inputroll = self.rawdata['roll']


        plt.figure(1)
        plt.title("Pitch Step Input Response")
        plt.plot(time, inputpitch, 'r-', label='desired-pitch')
        plt.plot(time, pitch, 'g-', label='actual-pitch')
        plt.xlabel('Time (ms)')
        plt.ylabel('Pitch (deg)')
        plt.legend()
        
        plt.figure(2)
        plt.title("Pitch Rate")
        plt.plot(time, desiredpitchrate, 'r-', label='desired-pitchrate')
        plt.plot(time, pitchrate, 'g-', label='actual-pitchrate')
        plt.xlabel('Time (ms)')
        plt.ylabel('Omega (deg/sec)')
        plt.legend()
        
        plt.figure(3)
        plt.title("Roll Step Input Response")
        plt.plot(time, inputroll, 'r-', label='desired-roll')
        plt.plot(time, roll, 'g-', label='actual-roll')
        plt.xlabel('Time (ms)')
        plt.ylabel('Roll (deg)')
        plt.legend()
        
        plt.figure(4)
        plt.title("Roll Rate")
        plt.plot(time, desiredrollrate, 'r-', label='desired-rollrate')
        plt.plot(time, rollrate, 'g-', label='actual-rollrate')
        plt.xlabel('Time (ms)')
        plt.ylabel('Omega (deg/sec)')
        plt.legend()
        
        
        plt.show(block=True)

    def plot_subplots(self):
        time = self.rawdata['timestamp']
        roll = self.rawdata['stabilizerroll']
        pitch = self.rawdata['stabilizerpitch']*-1 # for some reason it's inverted
        desiredpitchrate = self.rawdata['controllerpitchRate'] # pitchrate at controller is in deg/sec
        desiredrollrate = self.rawdata['controllerrollRate']
        rollrate = self.rawdata['stateEstimateZrateRoll']*180.0/(np.pi*1000.0)
        pitchrate = self.rawdata['stateEstimateZratePitch']*180.0/(np.pi*1000.0) # state estimate reading is in millirad/sec
        inputpitch = self.rawdata['pitch']
        inputroll = self.rawdata['roll']

        fig,ax = plt.subplots(2,2, sharex=True)
        ax[0,0].set_title("Pitch Step Input Response")
        ax[0,0].plot(time, inputpitch, 'r-', label='desired-pitch')
        ax[0,0].plot(time, pitch, 'g-', label='actual-pitch')
        ax[0,0].set_xlabel('Time (ms)')
        ax[0,0].set_ylabel('Pitch (deg)')
        ax[0,0].legend()
        
        ax[1,0].set_title("Pitch Rate")
        ax[1,0].plot(time, desiredpitchrate, 'r-', label='desired-pitchrate')
        ax[1,0].plot(time, pitchrate, 'g-', label='actual-pitchrate')
        ax[1,0].set_xlabel('Time (ms)')
        ax[1,0].set_ylabel('Omega (deg/sec)')
        ax[1,0].legend()
        
        ax[0,1].set_title("Roll Step Input Response")
        ax[0,1].plot(time, inputroll, 'r-', label='desired-roll')
        ax[0,1].plot(time, roll, 'g-', label='actual-roll')
        ax[0,1].set_xlabel('Time (ms)')
        ax[0,1].set_ylabel('Roll (deg)')
        ax[0,1].legend()
        
        ax[1,1].set_title("Roll Rate")
        ax[1,1].plot(time, desiredrollrate, 'r-', label='desired-rollrate')
        ax[1,1].plot(time, rollrate, 'g-', label='actual-rollrate')
        ax[1,1].set_xlabel('Time (ms)')
        ax[1,1].set_ylabel('Omega (deg/sec)')
        ax[1,1].legend()
        
        
        plt.show(block=True)

if __name__ == "__main__":
    d = DataStruct()
    d.from_csv('csvs/step.csv')
    # d.plot_unorganized()
    d.plot_subplots()
    print('d')