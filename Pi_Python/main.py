import pywemo
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

class Smoker:
    
    def __init__(self):
        # Default name =
        self.nameOfWeMoDevice = "SmokerWeMo"
        self.wemoDeviceName = None

        # These will be temps of probes
        self.meatProbe = None
        self.smokerProbe = None

        self.listOfDevices = None

    def findWeMoDevices(self):
        # Find the wemo we want to control
        self.listOfDevices = pywemo.discover_devices()

        # If we have a name saved for the WeMo then look for it!
        if not self.nameOfWeMoDevice == None:
            for device in self.listOfDevices:
                if self.nameOfWeMoDevice in str(device):
                    self.wemoDeviceName = device
                    break

        return self.listOfDevices

    def returnName(self):
        return self.wemoDeviceName

@app.route('/wemoDeviceList')
def wemo_deviceList():
    return smoker.findWeMoDevices()

@app.route('/wemoDeviceName')
def wemo_deviceName():
    return str(smoker.returnName())

@app.route('/status')
def smoker_piStatus():
    return str(200)

if __name__ == "__main__":
    print("Starting!")

    smoker = Smoker()

    # Start flask service
    app.run(host='0.0.0.0', port=5000)
    