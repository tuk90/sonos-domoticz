"""
<plugin key="SonosAPI" name="Sonos API" author="Nick Baring" version="0.2">
    <params>
        <param field="Mode1" label="Ipadress" width="200px" required="true"/>
        <param field="Mode2" label="Port" width="200px" required="true"/>
        <param field="Mode3" label="Volume adjustment in %" width="200px" required="true"/>
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
        # Declare Devices variable
        global Devices
        # Assumes device is on on start
        self.device_online = True
        
        # Read options from Domoticz GUI
        self.readOptions()
        
        self.favoriteList()
        # Check if there are no existing devices
        if len(Devices) != 3:
            # Example: Create devices
            self.createDevices()
        else:
            options = {
            "LevelNames": self.all_favorites_for_device,
            "LevelOffHidden": "false",
            "SelectorStyle": "1"
            }
            #Devices[1].Update(Options={"LevelNames": self.all_favorites_for_device})
        Domoticz.Heartbeat(15)

    def onStop(self):
        # Called when the plugin is stopped
        Domoticz.Log("Sonos API stopped.")

    def readOptions(self):
        # Read options from Domoticz GUI
        if Parameters["Mode1"]:
            self.ipadress = Parameters["Mode1"]
        if "Mode2" in Parameters and Parameters["Mode2"]:
            self.port = Parameters["Mode2"]
        if "Mode3" in Parameters and Parameters["Mode3"]:
            self.volumeAdjustment = Parameters["Mode3"]
        else:
            Domoticz.Error("Ipadress or port not configured")

        
    def favoriteList(self): # Gets all favorites from Sonos.
        favorite_response = requests.get(f'http://{self.ipadress}:{self.port}/favorites')
        if favorite_response.status_code == 200:
            json_response = favorite_response.json()
            self.level_names = {0: "Off"}  # Default level 0 to "Off"
            # Update the dictionary with the response, starting from level 10
            self.level_names.update({(i + 1) * 10: name for i, name in enumerate(json_response)})
            
            # Accumulate values of key-value pairs
            self.all_favorites_for_device = "|".join(self.level_names.values())

            # Log accumulated values
            Domoticz.Log("All values: {}".format(self.all_favorites_for_device))
            for level, name in self.level_names.items():
                Domoticz.Log("Level {}: {}".format(level, name))
        else:
            Domoticz.Log("Failed to fetch favorites. Status code: {}".format(favorite_response.status_code))
    
    def createDevices(self):

        # Create devices for sonos
        options = {
        "LevelNames": self.all_favorites_for_device,
        "LevelOffHidden": "false",
        "SelectorStyle": "1"
        }
        Domoticz.Device(Name="Favorites", Unit=1, TypeName="Selector Switch", Image=8, Options=options, Used=1).Create()
        options = {
        "LevelNames": "🔉|🔊|❚◄◄|►❚❚|►►❚",
        "LevelOffHidden": "false",
        "SelectorStyle": "0"
        }
        Domoticz.Device(Name="Control", Unit=2, TypeName="Selector Switch", Image=8, Options=options, Used=1).Create()
        Domoticz.Device(Name="Current playing", Unit=3, TypeName="Text", Used=1).Create()
        
    
    def get_play_state(self,data): # Gets the state of the device, play or shuffle and sets it accordingly
        shuffle_value = data["playMode"]["shuffle"]
        if shuffle_value == True: # If state is Shuffle set mode in Domoticz to shuffel else play/pause
            Devices[2].Update(nValue=50, sValue="50")
        else:
            Devices[2].Update(nValue=30, sValue="30")
           
                
    def get_current_playing(self, data): # Gets current artist and number     
        current_track = data.get("currentTrack", {})
        artist = current_track.get("artist")
        title = current_track.get("title")
        playbackState = data.get("playbackState")
        
        if playbackState != "PLAYING":
            Devices[3].Update(nValue=1, sValue="")

        elif artist is not None and title is not None:
            combined_info = f"{artist} - {title}"
            Devices[3].Update(nValue=1, sValue=combined_info)
            #Domoticz.Log(combined_info)
        elif artist is not None:
            Devices[3].Update(nValue=1, sValue=artist)
            #Domoticz.Log(artist)
        elif title is not None:
            Devices[3].Update(nValue=1, sValue=title)
            #Domoticz.Log(title)
        else:
            Devices[3].Update(nValue=1, sValue="Artist and title are not available")
            #Domoticz.Log("Artist and title are not available.")
    
                
    def onheartbeat(self):
        Domoticz.Log("Heartbeat Sonos")
        if self.device_online == True:
            try:
                response = requests.get(f'http://{self.ipadress}:{self.port}/state')
                data = json.loads(response.text)  # Extract text content before parsing
                self.get_play_state(data)
                self.get_current_playing(data)  
            except requests.RequestException as e:
                # Handle HTTP request errors
                Domoticz.Error(f"HTTP request error: {e}")
                Devices[1].Update(nValue=0,sValue="0") # Sets favorite device to "Off"           
                self.device_online = False
    
    def onCommand(self, unit, command, level, hue):
        try:
            self.device_online = True #When oncommand is triggered the get state heartbeat starts again
            if unit == 1: # Favorite list device
                level_name = self.level_names.get(level) #gets name of the level to be used in the API call
                if level == 0:
                    response = requests.get(
                    f'http://{self.ipadress}:{self.port}/pause')
                    Devices[1].Update(nValue=level,sValue=str(level))
                    Domoticz.Log(response.url)
                else:
                    response = requests.get(
                    f'http://{self.ipadress}:{self.port}/favorite/{level_name}')
                    Devices[1].Update(nValue=level,sValue=str(level))
                    Domoticz.Log(response.url)
                response.raise_for_status()
            if unit == 2: # Sonos Controll device
                if level == 0:
                    response = requests.get(
                    f'http://{self.ipadress}:{self.port}/volume/-{self.volumeAdjustment}') 
                elif level == 10:
                    response = requests.get(
                    f'http://{self.ipadress}:{self.port}/volume/+{self.volumeAdjustment}') 
                elif level == 20:
                    response = requests.get(
                    f'http://{self.ipadress}:{self.port}/previous')
                elif level == 30:
                    response = requests.get(
                    f'http://{self.ipadress}:{self.port}/playpause')
                elif level == 40:
                    response = requests.get(
                    f'http://{self.ipadress}:{self.port}/next') 
                elif level == 50:
                    response = requests.get(
                    f'http://{self.ipadress}:{self.port}/shuffle/toggle') 
                response.raise_for_status()
        except requests.exceptions.RequestException as e:
            Domoticz.Error(f"Request failed: {e}")
        except Exception as e:
            Domoticz.Error(f"An unexpected error occurred: {e}")   
            

# Create an instance of the SonosAPI class
_plugin = SonosAPI()

def onStart():
    _plugin.onStart()

def onStop():
    _plugin.onStop()

def onHeartbeat():
    _plugin.onheartbeat()

def onCommand(unit, command, level, hue):
    _plugin.onCommand(unit, command, level, hue)

def onConfigurationChanged():
    _plugin.readOptions()