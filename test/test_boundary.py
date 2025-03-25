import pytest
from test.TestUtils import TestUtils
from smart_home_system import Device, Light, Thermostat, SecurityDevice, Camera, MotionSensor, SmartHome
from smart_home_system import DeviceNotFoundException, InvalidInputException

class TestBoundary:
    """Test cases for boundary conditions in the smart home system."""
    
    def test_system_boundaries(self):
        """Test all boundary conditions for the smart home system."""
        try:
            # Device boundary tests
            try:
                # Empty ID should raise exception
                device = Device("", "Test Device", True, True, "Test Room")
                assert False, "Should raise InvalidInputException for empty ID"
            except InvalidInputException:
                pass  # Expected behavior
            
            # Valid device creation
            device = Device("D001", "Test Device", True, True, "Test Room")
            assert device.id == "D001"
            assert device.name == "Test Device"
            assert device.is_on is True
            assert device.connected is True
            assert device.location == "Test Room"
            
            # Light boundary tests
            try:
                # Brightness below 0 should raise exception
                light = Light("L001", "Test Light", True, True, "Living Room", -10, "White")
                assert False, "Should raise InvalidInputException for brightness < 0"
            except InvalidInputException:
                pass  # Expected behavior
                
            try:
                # Brightness above 100 should raise exception
                light = Light("L001", "Test Light", True, True, "Living Room", 110, "White")
                assert False, "Should raise InvalidInputException for brightness > 100"
            except InvalidInputException:
                pass  # Expected behavior
            
            # Valid light creation
            light = Light("L001", "Test Light", True, True, "Living Room", 80, "White")
            assert light.id == "L001"
            assert light.brightness == 80
            assert light.color == "White"
            
            # Test dim method boundaries
            try:
                light.dim(-5)
                assert False, "Should raise InvalidInputException for brightness < 0"
            except InvalidInputException:
                pass  # Expected behavior
                
            try:
                light.dim(110)
                assert False, "Should raise InvalidInputException for brightness > 100"
            except InvalidInputException:
                pass  # Expected behavior
                
            # Valid dim values
            assert light.dim(0) == 0
            assert light.dim(100) == 100
            assert light.dim(50) == 50
            
            # Thermostat boundary tests
            try:
                # Temperature below 5 should raise exception
                thermostat = Thermostat("T001", "Test Thermostat", True, True, "Living Room", 0, "Heat", 22)
                assert False, "Should raise InvalidInputException for temperature < 5"
            except InvalidInputException:
                pass  # Expected behavior
                
            try:
                # Temperature above 35 should raise exception
                thermostat = Thermostat("T001", "Test Thermostat", True, True, "Living Room", 40, "Heat", 22)
                assert False, "Should raise InvalidInputException for temperature > 35"
            except InvalidInputException:
                pass  # Expected behavior
                
            try:
                # Invalid mode should raise exception
                thermostat = Thermostat("T001", "Test Thermostat", True, True, "Living Room", 22, "Invalid", 22)
                assert False, "Should raise InvalidInputException for invalid mode"
            except InvalidInputException:
                pass  # Expected behavior
            
            # Valid thermostat creation
            thermostat = Thermostat("T001", "Test Thermostat", True, True, "Living Room", 22.5, "Heat", 23.0)
            assert thermostat.id == "T001"
            assert thermostat.temperature == 22.5
            assert thermostat.mode == "Heat"
            assert thermostat.target_temp == 23.0
            
            # Test set_temperature method boundaries
            try:
                thermostat.set_temperature(0)
                assert False, "Should raise InvalidInputException for temperature < 5"
            except InvalidInputException:
                pass  # Expected behavior
                
            try:
                thermostat.set_temperature(40)
                assert False, "Should raise InvalidInputException for temperature > 35"
            except InvalidInputException:
                pass  # Expected behavior
                
            # Valid temperature values
            assert thermostat.set_temperature(5) == 5
            assert thermostat.set_temperature(35) == 35
            assert thermostat.set_temperature(20) == 20
            
            # Test change_mode method boundaries
            try:
                thermostat.change_mode("Invalid")
                assert False, "Should raise InvalidInputException for invalid mode"
            except InvalidInputException:
                pass  # Expected behavior
                
            # Valid mode values
            assert thermostat.change_mode("Cool") == "Cool"
            assert thermostat.change_mode("Heat") == "Heat"
            assert thermostat.change_mode("Auto") == "Auto"
            
            # Test toggle power with Off mode
            thermostat.change_mode("Off")
            assert thermostat.is_on is False  # Off mode should turn off the device
            
            # Security Device boundary tests
            try:
                # Sensitivity below 0 should raise exception
                security = SecurityDevice("S001", "Test Security", True, True, "Living Room", "Armed", -10)
                assert False, "Should raise InvalidInputException for sensitivity < 0"
            except InvalidInputException:
                pass  # Expected behavior
                
            try:
                # Sensitivity above 100 should raise exception
                security = SecurityDevice("S001", "Test Security", True, True, "Living Room", "Armed", 110)
                assert False, "Should raise InvalidInputException for sensitivity > 100"
            except InvalidInputException:
                pass  # Expected behavior
            
            # Valid security device creation
            security = SecurityDevice("S001", "Test Security", True, True, "Front Door", "Armed", 80)
            assert security.id == "S001"
            assert security.armed_status == "Armed"
            assert security.sensitivity == 80
            
            # Test arm/disarm methods
            security.toggle_power()  # Turn off
            assert security.is_on is False
            assert security.armed_status == "Disarmed"  # Should be disarmed when turned off
            
            # Arm while device is off should not change status
            security.arm()
            assert security.armed_status == "Disarmed"
            
            security.toggle_power()  # Turn back on
            security.arm()
            assert security.armed_status == "Armed"
            
            security.disarm()
            assert security.armed_status == "Disarmed"
            
            # Camera boundary tests
            camera = Camera("C001", "Test Camera", True, True, "Front Door", "Armed", 80, "1080p", False)
            assert camera.id == "C001"
            assert camera.resolution == "1080p"
            assert camera.recording is False
            
            # Test start/stop recording
            camera.toggle_power()  # Turn off
            assert camera.start_recording() is False  # Should not start when off
            
            camera.toggle_power()  # Turn back on
            assert camera.start_recording() is True
            assert camera.recording is True
            
            assert camera.stop_recording() is False
            assert camera.recording is False
            
            # Arm should start recording
            camera.arm()
            assert camera.armed_status == "Armed"
            assert camera.recording is True
            
            # Disarm should stop recording
            camera.disarm()
            assert camera.armed_status == "Disarmed"
            assert camera.recording is False
            
            # Motion Sensor boundary tests
            motion = MotionSensor("M001", "Test Motion", True, True, "Backyard", "Armed", 60, 10, None)
            assert motion.id == "M001"
            assert motion.detection_range == 10
            assert motion.last_triggered is None
            
            # Test detect_motion method
            motion.toggle_power()  # Turn off
            assert motion.detect_motion("12:00") is None  # Should not detect when off
            
            motion.toggle_power()  # Turn back on
            motion.disarm()
            assert motion.detect_motion("12:00") is None  # Should not detect when disarmed
            
            motion.arm()
            assert motion.detect_motion("12:00") == "12:00"
            assert motion.last_triggered == "12:00"
            
            motion.reset_trigger()
            assert motion.last_triggered is None
            
            # Smart Home boundary tests
            home = SmartHome("Test Home")
            assert home.name == "Test Home"
            assert home.mode == "Home"
            assert len(home.devices) == 0
            assert len(home.rooms) == 0
            
            # Test add_device method
            assert home.add_device(light) is True
            assert home.add_device(thermostat) is True
            assert home.add_device(camera) is True
            assert home.add_device(motion) is True
            
            # Adding same device twice should return False
            assert home.add_device(light) is False
            
            try:
                # Adding non-Device object should raise exception
                home.add_device("not a device")
                assert False, "Should raise InvalidInputException for non-Device object"
            except InvalidInputException:
                pass  # Expected behavior
            
            # Test get_devices_by_type method
            lights = home.get_devices_by_type(Light)
            assert len(lights) == 1
            assert lights[0].id == "L001"
            
            # Test get_devices_by_room method
            living_room_devices = home.get_devices_by_room("Living Room")
            assert len(living_room_devices) == 2  # Light and Thermostat
            
            # Test find_device method
            found_device = home.find_device("L001")
            assert found_device.id == "L001"
            
            try:
                # Finding non-existent device should raise exception
                home.find_device("NONEXISTENT")
                assert False, "Should raise DeviceNotFoundException"
            except DeviceNotFoundException:
                pass  # Expected behavior
            
            # Test remove_device method
            assert home.remove_device("L001") is True
            assert home.remove_device("NONEXISTENT") is False
            
            # Verify device removal
            try:
                home.find_device("L001")
                assert False, "Should raise DeviceNotFoundException"
            except DeviceNotFoundException:
                pass  # Expected behavior
            
            # Test change_mode method
            try:
                home.change_mode("Invalid")
                assert False, "Should raise InvalidInputException for invalid mode"
            except InvalidInputException:
                pass  # Expected behavior
                
            # Valid mode values
            assert home.change_mode("Away") == "Away"
            assert home.change_mode("Night") == "Night"
            assert home.change_mode("Vacation") == "Vacation"
            assert home.change_mode("Home") == "Home"
            
            # Test execute_automation method
            # Add devices first for automation testing
            kitchen_light = Light("L002", "Kitchen Light", False, True, "Kitchen", 100, "White")
            bedroom_light = Light("L003", "Bedroom Light", False, True, "Bedroom", 60, "Warm White")
            hallway_light = Light("L004", "Hallway Light", False, True, "Hallway", 50, "White")
            living_room_thermostat = Thermostat("T002", "Living Room Thermostat", True, True, "Living Room", 22, "Heat", 22)
            front_camera = Camera("C002", "Front Camera", True, True, "Front Door", "Disarmed", 80, "1080p", False)
            
            home.add_device(kitchen_light)
            home.add_device(bedroom_light)
            home.add_device(hallway_light)
            home.add_device(living_room_thermostat)
            home.add_device(front_camera)
            
            # Test Good Morning automation
            assert home.execute_automation("Good Morning") is True
            assert kitchen_light.is_on is True
            assert kitchen_light.brightness == 100
            assert bedroom_light.is_on is True
            assert bedroom_light.brightness == 60
            assert living_room_thermostat.target_temp == 22
            
            # Test Good Night automation
            assert home.execute_automation("Good Night") is True
            assert kitchen_light.is_on is False
            assert bedroom_light.is_on is False
            assert hallway_light.is_on is True
            assert hallway_light.brightness == 30
            assert living_room_thermostat.target_temp == 18
            assert front_camera.armed_status == "Armed"
            
            # Test Away Mode automation
            assert home.execute_automation("Away Mode") is True
            assert kitchen_light.is_on is False
            assert bedroom_light.is_on is False
            assert hallway_light.is_on is False
            assert living_room_thermostat.target_temp == 16
            assert living_room_thermostat.mode == "Auto"
            assert front_camera.armed_status == "Armed"
            
            # Non-existent automation should return False
            assert home.execute_automation("Non-existent") is False
            
            # Display info should return a string
            info = home.display_info()
            assert isinstance(info, str)
            assert "Test Home" in info
            assert "Total Devices:" in info
            
            TestUtils.yakshaAssert("test_system_boundaries", True, "boundary")
        except Exception as e:
            TestUtils.yakshaAssert("test_system_boundaries", False, "boundary")
            raise e