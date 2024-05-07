# Sonos API Plugin for Domoticz

This plugin allows you to control your Sonos speaker system through Domoticz.

## Installation

1. Clone or download this repository.
2. Copy the `plugin.py` file to your Domoticz plugins directory (`/domoticz/plugins/`).
3. Restart your Domoticz service.

## Configuration

1. Open the Domoticz web interface.
2. Navigate to the Hardware section.
3. Click on "Add" to add a new hardware device.
4. Select the "Sonos API" plugin from the dropdown menu.
5. Enter the IP address and port of your Sonos device.
6. Click on "Add" to save your settings.

## Usage

1. After adding the plugin, three devices will be created: "Favorites", "Control", and "Current playing".
2. Use the "Favorites" selector switch to choose a favorite from your Sonos device.
3. Use the "Control" selector switch to control playback, volume, and shuffle mode.
4. The "Current playing" text device will display information about the currently playing track.

## Contributing

Contributions are welcome! If you would like to contribute to the development of this plugin, please fork the repository and submit a pull request.

## License

This plugin is distributed under the [MIT License](https://opensource.org/licenses/MIT).
