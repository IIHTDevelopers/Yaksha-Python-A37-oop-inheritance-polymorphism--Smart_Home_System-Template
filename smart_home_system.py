"""
Smart Home System - A simplified implementation for HomeHub Technologies
"""

class DeviceNotFoundException(Exception):
    """Exception raised when a device is not found in the smart home."""
    pass

class InvalidInputException(Exception):
    """Exception raised when invalid input is provided."""
    pass

class Device:
    """Base class representing any device in the smart home system."""
    device_count = 0
    
    def __init__(self, id, name, is_on, connected, location):
        if not isinstance(id, str) or not id:
            raise InvalidInputException("Device ID must be non-empty string")
        self._id = id
        self._name = name
        self._is_on = is_on
        self._connected = connected
        self._location = location
        Device.device_count += 1
    
    def __del__(self):
        Device.device_count -= 1
    
    @property
    def id(self): return self._id
    @property
    def name(self): return self._name
    @property
    def is_on(self): return self._is_on
    @property
    def connected(self): return self._connected
    @property
    def location(self): return self._location
    
    def toggle_power(self):
        self._is_on = not self._is_on
        return self._is_on
    
    def connect(self):
        self._connected = True
        return self._connected
    
    def disconnect(self):
        self._connected = False
        return self._connected
    
    def display_info(self):
        power = "On" if self._is_on else "Off"
        conn = "Connected" if self._connected else "Disconnected"
        return f"ID: {self._id} | {self._name} | {power} | {conn} | {self._location}"

class Light(Device):
    """Class representing light devices."""
    def __init__(self, id, name, is_on, connected, location, brightness, color):
        super().__init__(id, name, is_on, connected, location)
        if not (0 <= brightness <= 100):
            raise InvalidInputException("Brightness must be between 0-100")
        self._brightness = brightness
        self._color = color
    
    @property
    def brightness(self): return self._brightness
    @property
    def color(self): return self._color
    
    def dim(self, level):
        if not (0 <= level <= 100):
            raise InvalidInputException("Brightness must be between 0-100")
        self._brightness = level
        return self._brightness
    
    def change_color(self, color):
        self._color = color
        return self._color
    
    def display_info(self):
        return f"{super().display_info()} | Brightness: {self._brightness}% | Color: {self._color}"

class Thermostat(Device):
    """Class representing thermostat devices."""
    VALID_MODES = ["Heat", "Cool", "Auto", "Off"]
    
    def __init__(self, id, name, is_on, connected, location, temperature, mode, target_temp):
        super().__init__(id, name, is_on, connected, location)
        if not (5 <= temperature <= 35):
            raise InvalidInputException("Temperature must be between 5-35°C")
        if mode not in self.VALID_MODES:
            raise InvalidInputException(f"Mode must be one of {self.VALID_MODES}")
        if not (5 <= target_temp <= 35):
            raise InvalidInputException("Target temperature must be between 5-35°C")
        self._temperature = temperature
        self._mode = mode
        self._target_temp = target_temp
    
    @property
    def temperature(self): return self._temperature
    @property
    def mode(self): return self._mode
    @property
    def target_temp(self): return self._target_temp
    
    def toggle_power(self):
        result = super().toggle_power()
        if not result:
            self._mode = "Off"
        return result
    
    def set_temperature(self, temperature):
        if not (5 <= temperature <= 35):
            raise InvalidInputException("Temperature must be between 5-35°C")
        self._target_temp = temperature
        return self._target_temp
    
    def change_mode(self, mode):
        if mode not in self.VALID_MODES:
            raise InvalidInputException(f"Mode must be one of {self.VALID_MODES}")
        self._mode = mode
        if mode == "Off":
            self._is_on = False
        return self._mode
    
    def display_info(self):
        return f"{super().display_info()} | Current: {self._temperature}°C | Target: {self._target_temp}°C | Mode: {self._mode}"

class SecurityDevice(Device):
    """Base class representing security devices."""
    def __init__(self, id, name, is_on, connected, location, armed_status, sensitivity):
        super().__init__(id, name, is_on, connected, location)
        if not (0 <= sensitivity <= 100):
            raise InvalidInputException("Sensitivity must be between 0-100")
        self._armed_status = armed_status
        self._sensitivity = sensitivity
    
    @property
    def armed_status(self): return self._armed_status
    @property
    def sensitivity(self): return self._sensitivity
    
    def toggle_power(self):
        result = super().toggle_power()
        if not result:
            self._armed_status = "Disarmed"
        return result
    
    def arm(self):
        if not self._is_on:
            return self._armed_status
        self._armed_status = "Armed"
        return self._armed_status
    
    def disarm(self):
        self._armed_status = "Disarmed"
        return self._armed_status
    
    def display_info(self):
        return f"{super().display_info()} | Status: {self._armed_status} | Sensitivity: {self._sensitivity}%"

class Camera(SecurityDevice):
    """Class representing camera devices."""
    def __init__(self, id, name, is_on, connected, location, armed_status, sensitivity, resolution, recording):
        super().__init__(id, name, is_on, connected, location, armed_status, sensitivity)
        self._resolution = resolution
        self._recording = recording
    
    @property
    def resolution(self): return self._resolution
    @property
    def recording(self): return self._recording
    
    def arm(self):
        result = super().arm()
        if result == "Armed" and not self._recording:
            self._recording = True
        return result
    
    def disarm(self):
        result = super().disarm()
        self._recording = False
        return result
    
    def start_recording(self):
        if not self._is_on:
            return False
        self._recording = True
        return self._recording
    
    def stop_recording(self):
        self._recording = False
        return self._recording
    
    def display_info(self):
        rec_status = "Recording" if self._recording else "Not Recording"
        return f"{super().display_info()} | Resolution: {self._resolution} | {rec_status}"

class MotionSensor(SecurityDevice):
    """Class representing motion sensor devices."""
    def __init__(self, id, name, is_on, connected, location, armed_status, sensitivity, detection_range, last_triggered):
        super().__init__(id, name, is_on, connected, location, armed_status, sensitivity)
        self._detection_range = detection_range
        self._last_triggered = last_triggered
    
    @property
    def detection_range(self): return self._detection_range
    @property
    def last_triggered(self): return self._last_triggered
    
    def detect_motion(self, timestamp=None):
        if not self._is_on or self._armed_status != "Armed":
            return None
        self._last_triggered = timestamp
        return self._last_triggered
    
    def reset_trigger(self):
        self._last_triggered = None
        return self._last_triggered
    
    def display_info(self):
        trigger = f"Last Triggered: {self._last_triggered}" if self._last_triggered else "Never Triggered"
        return f"{super().display_info()} | Range: {self._detection_range}m | {trigger}"

class SmartHome:
    """Class representing a smart home system."""
    VALID_MODES = ["Home", "Away", "Night", "Vacation"]
    
    def __init__(self, name):
        self.__name = name
        self.__devices = []
        self.__rooms = set()
        self.__mode = "Home"
    
    @property
    def name(self): return self.__name
    @property
    def mode(self): return self.__mode
    @property
    def devices(self): return self.__devices.copy()
    @property
    def rooms(self): return self.__rooms.copy()
    
    def add_device(self, device):
        if not isinstance(device, Device):
            raise InvalidInputException("Can only add Device objects")
        if any(d.id == device.id for d in self.__devices):
            return False
        self.__devices.append(device)
        self.__rooms.add(device.location)
        return True
    
    def remove_device(self, device_id):
        for i, device in enumerate(self.__devices):
            if device.id == device_id:
                self.__devices.pop(i)
                self.__rooms = set(d.location for d in self.__devices)
                return True
        return False
    
    def get_devices_by_type(self, device_class):
        return [d for d in self.__devices if isinstance(d, device_class)]
    
    def get_devices_by_room(self, room):
        return [d for d in self.__devices if d.location == room]
    
    def find_device(self, device_id):
        for device in self.__devices:
            if device.id == device_id:
                return device
        raise DeviceNotFoundException(f"Device with ID {device_id} not found")
    
    def execute_automation(self, automation_name):
        if automation_name == "Good Morning":
            # Turn on lights in bedrooms and kitchen
            for device in self.__devices:
                if isinstance(device, Light) and device.location in ["Bedroom", "Kitchen"]:
                    if not device.is_on: device.toggle_power()
                    device.dim(100 if device.location == "Kitchen" else 60)
            # Set thermostat to comfortable temperature
            for device in self.__devices:
                if isinstance(device, Thermostat):
                    if not device.is_on: device.toggle_power()
                    device.set_temperature(22)
                    device.change_mode("Heat")
            return True
        elif automation_name == "Good Night":
            # Turn off all lights except hallway
            for device in self.__devices:
                if isinstance(device, Light):
                    if device.location == "Hallway":
                        if not device.is_on: device.toggle_power()
                        device.dim(30)
                    elif device.is_on:
                        device.toggle_power()
            # Set thermostat to night temperature
            for device in self.__devices:
                if isinstance(device, Thermostat):
                    if not device.is_on: device.toggle_power()
                    device.set_temperature(18)
                    device.change_mode("Heat")
            # Arm all security devices
            for device in self.__devices:
                if isinstance(device, SecurityDevice):
                    if not device.is_on: device.toggle_power()
                    device.arm()
            return True
        elif automation_name == "Away Mode":
            # Turn off all lights
            for device in self.__devices:
                if isinstance(device, Light) and device.is_on:
                    device.toggle_power()
            # Set thermostat to energy saving mode
            for device in self.__devices:
                if isinstance(device, Thermostat):
                    if not device.is_on: device.toggle_power()
                    device.set_temperature(16)
                    device.change_mode("Auto")
            # Arm all security devices
            for device in self.__devices:
                if isinstance(device, SecurityDevice):
                    if not device.is_on: device.toggle_power()
                    device.arm()
            return True
        return False
    
    def change_mode(self, mode):
        if mode not in self.VALID_MODES:
            raise InvalidInputException(f"Mode must be one of {self.VALID_MODES}")
        self.__mode = mode
        if mode == "Away": self.execute_automation("Away Mode")
        elif mode == "Night": self.execute_automation("Good Night")
        elif mode == "Home": self.execute_automation("Good Morning")
        return self.__mode
    
    def display_info(self):
        output = []
        output.append("===== SMART HOME SYSTEM =====")
        output.append(f"Home: {self.__name}")
        output.append(f"Mode: {self.__mode}")
        output.append(f"Total Devices: {len(self.__devices)}")
        output.append("Devices by Room:")
        for room in sorted(self.__rooms):
            room_devices = self.get_devices_by_room(room)
            output.append(f"  {room}: {len(room_devices)}")
        connected_count = sum(1 for d in self.__devices if d.connected)
        output.append(f"Connected Devices: {connected_count}/{len(self.__devices)}")
        return "\n".join(output)

def main():
    """Main function to run the smart home system."""
    # Create a smart home
    my_home = SmartHome("My Smart Home")
    
    # Add some initial devices
    try:
        my_home.add_device(Light("L001", "Living Room Light", True, True, "Living Room", 80, "White"))
        my_home.add_device(Thermostat("T001", "Main Thermostat", True, True, "Living Room", 22.5, "Heat", 23.0))
        my_home.add_device(Light("L002", "Kitchen Light", False, True, "Kitchen", 100, "White"))
        my_home.add_device(Light("L003", "Bedroom Light", False, True, "Bedroom", 60, "Warm White"))
        my_home.add_device(Camera("C001", "Front Door Camera", True, True, "Front Door", "Armed", 80, "1080p", False))
        my_home.add_device(MotionSensor("M001", "Backyard Sensor", True, True, "Backyard", "Armed", 60, 10, None))
    except Exception as e:
        print(f"Error setting up smart home: {e}")
    
    # Menu-based interaction
    while True:
        print("\n" + my_home.display_info())
        
        print("\nMenu:")
        print("1. Add Device to Smart Home")
        print("2. Control Device")
        print("3. Run Automation Scenario")
        print("4. Change Home Mode")
        print("5. Display All Devices")
        print("0. Exit")
        
        try:
            choice = int(input("\nEnter your choice (0-5): "))
            
            if choice == 1:
                # Add Device logic
                device_type = int(input("\nSelect device type (1-Light, 2-Thermostat, 3-Camera, 4-MotionSensor): "))
                device_id = input("Enter device ID: ")
                device_name = input("Enter device name: ")
                is_on = input("Is device on? (y/n): ").lower() == 'y'
                connected = input("Is device connected? (y/n): ").lower() == 'y'
                location = input("Enter device location (room): ")
                
                try:
                    if device_type == 1:  # Light
                        brightness = int(input("Enter brightness (0-100): "))
                        color = input("Enter light color: ")
                        device = Light(device_id, device_name, is_on, connected, location, brightness, color)
                    elif device_type == 2:  # Thermostat
                        temperature = float(input("Enter current temperature (5-35): "))
                        mode_choice = int(input("Select mode (1-Heat, 2-Cool, 3-Auto, 4-Off): "))
                        mode_options = ["Heat", "Cool", "Auto", "Off"]
                        mode = mode_options[mode_choice - 1]
                        target_temp = float(input("Enter target temperature (5-35): "))
                        device = Thermostat(device_id, device_name, is_on, connected, location, temperature, mode, target_temp)
                    elif device_type == 3:  # Camera
                        armed_status = "Armed" if input("Is device armed? (y/n): ").lower() == 'y' else "Disarmed"
                        sensitivity = int(input("Enter sensitivity (0-100): "))
                        resolution = input("Enter camera resolution: ")
                        recording = input("Is camera recording? (y/n): ").lower() == 'y'
                        device = Camera(device_id, device_name, is_on, connected, location, armed_status, sensitivity, resolution, recording)
                    elif device_type == 4:  # Motion Sensor
                        armed_status = "Armed" if input("Is device armed? (y/n): ").lower() == 'y' else "Disarmed"
                        sensitivity = int(input("Enter sensitivity (0-100): "))
                        detection_range = int(input("Enter detection range (meters): "))
                        device = MotionSensor(device_id, device_name, is_on, connected, location, armed_status, sensitivity, detection_range, None)
                    else:
                        raise InvalidInputException("Invalid device type selected")
                    
                    if my_home.add_device(device):
                        print(f"Device '{device_id}' added successfully.")
                    else:
                        print(f"Device with ID {device_id} already exists.")
                
                except Exception as e:
                    print(f"Error adding device: {e}")
            
            elif choice == 2:
                # Control Device logic
                try:
                    device_id = input("Enter device ID to control: ")
                    device = my_home.find_device(device_id)
                    print(f"\nSelected Device: {device.display_info()}")
                    
                    if isinstance(device, Light):
                        control_choice = int(input("\nOptions: 1-Toggle Power, 2-Connect/Disconnect, 3-Adjust Brightness, 4-Change Color: "))
                    elif isinstance(device, Thermostat):
                        control_choice = int(input("\nOptions: 1-Toggle Power, 2-Connect/Disconnect, 3-Set Temperature, 4-Change Mode: "))
                    elif isinstance(device, Camera):
                        control_choice = int(input("\nOptions: 1-Toggle Power, 2-Connect/Disconnect, 3-Arm/Disarm, 4-Start/Stop Recording: "))
                    elif isinstance(device, MotionSensor):
                        control_choice = int(input("\nOptions: 1-Toggle Power, 2-Connect/Disconnect, 3-Arm/Disarm, 4-Reset Trigger: "))
                    else:
                        control_choice = int(input("\nOptions: 1-Toggle Power, 2-Connect/Disconnect: "))
                    
                    if control_choice == 1:
                        print(f"Device is now {'On' if device.toggle_power() else 'Off'}")
                    elif control_choice == 2:
                        if device.connected:
                            device.disconnect()
                            print("Device disconnected")
                        else:
                            device.connect()
                            print("Device connected")
                    elif control_choice == 3:
                        if isinstance(device, Light):
                            brightness = int(input("Enter brightness (0-100): "))
                            device.dim(brightness)
                            print(f"Brightness set to {brightness}%")
                        elif isinstance(device, Thermostat):
                            temp = float(input("Enter target temperature (5-35): "))
                            device.set_temperature(temp)
                            print(f"Temperature set to {temp}°C")
                        elif isinstance(device, SecurityDevice):
                            if device.armed_status == "Armed":
                                device.disarm()
                                print("Device disarmed")
                            else:
                                device.arm()
                                print("Device armed")
                    elif control_choice == 4:
                        if isinstance(device, Light):
                            color = input("Enter new color: ")
                            device.change_color(color)
                            print(f"Color changed to {color}")
                        elif isinstance(device, Thermostat):
                            mode_choice = int(input("Select mode (1-Heat, 2-Cool, 3-Auto, 4-Off): "))
                            mode_options = ["Heat", "Cool", "Auto", "Off"]
                            device.change_mode(mode_options[mode_choice - 1])
                            print(f"Mode changed to {device.mode}")
                        elif isinstance(device, Camera):
                            if device.recording:
                                device.stop_recording()
                                print("Recording stopped")
                            else:
                                device.start_recording()
                                print("Recording started")
                        elif isinstance(device, MotionSensor):
                            device.reset_trigger()
                            print("Trigger reset")
                
                except DeviceNotFoundException as e:
                    print(f"Error: {e}")
                except Exception as e:
                    print(f"Error controlling device: {e}")
            
            elif choice == 3:
                # Run Automation
                automation_choice = int(input("\nSelect automation (1-Good Morning, 2-Good Night, 3-Away Mode): "))
                try:
                    automations = ["Good Morning", "Good Night", "Away Mode"]
                    if 1 <= automation_choice <= 3:
                        automation = automations[automation_choice - 1]
                        if my_home.execute_automation(automation):
                            print(f"'{automation}' automation executed")
                    else:
                        print("Invalid automation choice")
                except Exception as e:
                    print(f"Error executing automation: {e}")
            
            elif choice == 4:
                # Change Home Mode
                mode_choice = int(input("\nSelect mode (1-Home, 2-Away, 3-Night, 4-Vacation): "))
                try:
                    mode_options = ["Home", "Away", "Night", "Vacation"]
                    if 1 <= mode_choice <= 4:
                        new_mode = my_home.change_mode(mode_options[mode_choice - 1])
                        print(f"Home mode changed to {new_mode}")
                    else:
                        print("Invalid mode choice")
                except Exception as e:
                    print(f"Error changing mode: {e}")
            
            elif choice == 5:
                # Display All Devices
                print("\nAll Devices:")
                for device in my_home.devices:
                    print(device.display_info())
            
            elif choice == 0:
                # Exit
                print("Thank you for using the Smart Home System!")
                break
            
            else:
                print("Invalid choice. Please enter a number between 0 and 5.")
        
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()