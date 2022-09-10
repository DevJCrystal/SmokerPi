import math
import shelve
import pywemo
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

class Smoker:
    
    def __init__(self):
        
        self.completed_init = False;

        self.wemoDevice = None
        self.nameOfWeMoDevice = None
        self.listOfDevices = None

        # Calibration settings
        self.calibration_temps = []
        self.calibration_resistance = []

        # These will be temps of probes
        self.meat_temp = None
        self.smoker_temp = None

        self.C = None
        self.B = None
        self.A = None

        self.tempK = None
        self.tempC = None
        self.tempF = None

    # Below Steinhart equation is from:
    # https://github.com/kyleflan/tempiture
    def init_temp(self):
        L1 = math.log(self.calibration_resistances[0])
        L2 = math.log(self.calibration_resistances[1])
        L3 = math.log(self.calibration_resistances[2])
        Y1 = 1/self.calibration_temps[0];
        Y2 = 1/self.calibration_temps[1];
        Y3 = 1/self.calibration_temps[2];
        gma2 = (Y2-Y1)/(L2-L1);
        gma3 = (Y3-Y1)/(L3-L1);

        # A, B, and C are variables used in the Steinhart-Hart equation
		# to determine temperature from resistance in a thermistor. These
		# values will be set during the init() function.
        self.C = ((gma3-gma2)/(L3-L2))*math.pow((L1+L2+L3), -1)
        self.B = gma2 - self.C * (math.pow(L1, 2)+L1*L2+math.pow(L2,2))
        self.A = Y1 - (self.B+math.pow(L1, 2)*self.C)*L1

    def resistanceToTemperature(self, R):
        return 1/(self.A+self.B*math.log(R)+self.C*math.pow(math.log(R),3));

    def abcToResistance(self, abc_value, R):
        # Returns resistance based on the ADC value
        return (R / ((1023/abc_value)-1));

    def converABCValueToTemperature(self, abc_value, R):
        # Get Kelvin Temperature
        r = self.abcToResistance(abc_value)

        self.tempK = self.resistanceToTemperature(r);

		# convert to Celsius and round to 1 decimal place
        self.tempC = self.tempK - 273.15
        self.tempC = math.round(self.tempC*10)/10;

		# get the Fahrenheit temperature, rounded
        self.tempF = (self.tempC * 1.8) + 32;
        self.tempF = math.round(self.tempF*10)/10;

    def findWeMoDevices(self):
        # Find the wemo we want to control
        self.listOfDevices = pywemo.discover_devices()

        # If we have a name saved for the WeMo then look for it!
        if not self.nameOfWeMoDevice == None:
            for device in self.listOfDevices:
                if self.nameOfWeMoDevice in str(device):
                    self.wemoDevice = device
                    break

        return self.listOfDevices

    def returnName(self):
        return self.nameOfWeMoDevice

@app.route('/wemoDeviceList')
def wemo_deviceList():
    return smoker.findWeMoDevices()

@app.route('/wemoDeviceName')
def wemo_deviceName():
    return str(smoker.returnName())

@app.route('/init', methods = ['POST'])
def probes_init():
    # In here we will set the 3 temps and 3 resistance values
    return smoker

@app.route('/status')
def smoker_piStatus():
    return str(smoker.completed_init)

if __name__ == "__main__":
    print("Starting SmokerPi WebServer...")

    smoker = Smoker()
    db = shelve.open('smokerpi_db')
    smoker.completed_init = len(db.keys()) > 0
    if (len(db.keys()) > 0):
        smoker.completed_init = True
        smoker.calibration_temps = db['cal_temps']
        smoker.calibration_resistance = db['cal_resistance']

        smoker.init_temp()
    else:
        smoker.completed_init = False
    print(smoker.completed_init)
    db.close()

    # Start flask service
    app.run(host='0.0.0.0', port=5000)
    