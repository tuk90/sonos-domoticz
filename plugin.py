"""
<plugin key="RemehaHome" name="Remeha Home Plugin" author="Nick Baring/GizMoCuz" version="1.3.0">
    <params>
        <param field="Mode1" label="Email" width="200px" required="true"/>
        <param field="Mode2" label="Password" width="200px" password="true" required="true"/>
        <param field="Mode3" label="Poll Interval" width="100px" required="true">
            <options>
                <option label="30 seconds" value="30"/>
                <option label="1 minute" value="60" default="true"/>
                <option label="2 minutes" value="120"/>
                <option label="5 minutes" value="300"/>
            </options>
        </param>
    </params>
</plugin>
"""
import Domoticz
import requests
import json

class SonosAPI:
    def __init__(self):
        # Initialize a session for making HTTP requests
        self._session = requests.Session()

def onStart(self):
        # Called when the plugin is started
        Domoticz.Log("Sonos API started.")
        
        # Read options from Domoticz GUI
        self.readOptions()
        # Check if there are no existing devices
        if len(Devices) != 10:
            # Example: Create devices for temperature, pressure, and setpoint
            self.createDevices()
        Domoticz.Heartbeat(5)
        Domoticz.Log(f"Poll Interval: {self.poll_interval}")

def onStop(self):
        # Called when the plugin is stopped
        Domoticz.Log("Remeha Home Plugin stopped.")

def readOptions(self):
        # Read options from Domoticz GUI
        if Parameters["Mode1"]:
            self.email = Parameters["Mode1"]
        if "Mode2" in Parameters and Parameters["Mode2"]:
            self.password = Parameters["Mode2"]
        else:
            Domoticz.Error("Password not configured in the Domoticz plugin configuration.")
        self.poll_interval = int(Parameters["Mode3"])            
        if self.poll_interval < 30:
            self.poll_interval = 30
        if self.poll_interval > 300:
            self.poll_interval = 300

def createDevices(self):
        # Declare Devices variable
        global Devices

        # Create devices for temperature, pressure, and setpoint
        Domoticz.Device(Name="roomTemperature", Unit=1, TypeName="Temperature", Used=1).Create()
        Domoticz.Device(Name="outdoorTemperature", Unit=2, TypeName="Temperature", Used=1).Create()
        Domoticz.Device(Name="waterPressure", Unit=3, TypeName="Pressure", Used=1).Create()
        Domoticz.Device(Name="setPoint", Unit=4, TypeName="Setpoint", Used=1).Create()
        Domoticz.Device(Name="dhwTemperature", Unit=5, TypeName="Temperature", Used=1).Create()
        Domoticz.Device(Name="EnergyConsumption", Unit=6, Type=243, TypeName="Kwh", Subtype=29, Used=1).Create()
        Domoticz.Device(Name="gasCalorificValue", Unit=7, Type=243, Subtype=31, Used=1).Create()
        Domoticz.Device(Name="zoneMode", Unit=8, TypeName="Selector Switch", Image=15, Options={"LevelNames":"Scheduling|Manual|TemporaryOverride|FrostProtection", "LevelOffHidden": "false", "SelectorStyle": "1"}, Used=1).Create()
        Domoticz.Device(Name="waterPressureToLow", Unit=9, TypeName="Switch", Switchtype=0, Image=13, Used=1).Create()
        Domoticz.Device(Name="EnergyDelivered", Unit=10, Type=243, TypeName="Kwh", Subtype=29, Switchtype=4, Used=1).Create()


# Create an instance of the SonosAPI class
_plugin = SonosAPI()

def onStart():
    _plugin.onStart()

def onStop():
    _plugin.onStop()

def onHeartbeat():
    _plugin.onheartbeat()

def onCommand(unit, command, level, hue):
    _plugin.oncommand(unit, command, level, hue)

def onConfigurationChanged():
    _plugin.readOptions()