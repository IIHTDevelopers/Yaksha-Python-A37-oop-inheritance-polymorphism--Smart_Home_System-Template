import pytest
from test.TestUtils import TestUtils
from smart_home_system import Device, Light, Thermostat, SecurityDevice, Camera, MotionSensor, SmartHome

class TestFunctional:
    """Test cases for functional requirements of the smart home system."""
    
    def test_base_device_functionality(self):
        """Test Device class functionality and attribute management."""
        try:
            # Test Device creation and attributes
            device = Device("D001", "Test Device", True, True, "Living Room")
            assert device.id == "D001"
            assert device.name == "Test Device"
            assert device.is_on == True
            assert device.connected == True
            assert device.location == "Living Room"
            
            # Test class variable tracking
            initial_count = Device.device_count
            second_device = Device("D002", "Second Device", False, True, "Kitchen")
            assert Device.device_count == initial_count + 1
            
            # Test methods
            device.toggle_power()
            assert device.is_on == False
            
            device.disconnect()
            assert device.connected == False
            
            device.connect()
            assert device.connected == True
            
            # Test display_info
            info = device.display_info()
            assert "D001" in info
            assert "Test Device" in info
            assert "Off" in info
            assert "Connected" in info
            assert "Living Room" in info
            
            # Clean up
            del second_device
            
            TestUtils.yakshaAssert("test_base_device_functionality", True, "functional")
        except Exception as e:
            TestUtils.yakshaAssert("test_base_device_functionality", False, "functional")
            raise e
    
    def test_light_and_thermostat(self):
        """Test Light and Thermostat classes - inheritance and functionality."""
        try:
            # Test Light
            light = Light("L001", "Living Room Light", True, True, "Living Room", 80, "White")
            assert isinstance(light, Device)
            assert light.brightness == 80
            assert light.color == "White"
            
            light.dim(50)
            assert light.brightness == 50
            
            light.change_color("Warm White")
            assert light.color == "Warm White"
            
            light_info = light.display_info()
            assert "Brightness: 50%" in light_info
            assert "Color: Warm White" in light_info
            
            # Test Thermostat
            thermostat = Thermostat("T001", "Main Thermostat", True, True, "Hallway", 22.5, "Heat", 23.0)
            assert isinstance(thermostat, Device)
            assert thermostat.temperature == 22.5
            assert thermostat.mode == "Heat"
            assert thermostat.target_temp == 23.0
            
            thermostat.set_temperature(21.0)
            assert thermostat.target_temp == 21.0
            
            thermostat.change_mode("Cool")
            assert thermostat.mode == "Cool"
            
            thermostat.toggle_power()
            assert thermostat.is_on == False
            assert thermostat.mode == "Off"  # Override behavior
            
            thermo_info = thermostat.display_info()
            assert "Current: 22.5°C" in thermo_info
            assert "Target: 21.0°C" in thermo_info
            assert "Mode: Off" in thermo_info
            
            TestUtils.yakshaAssert("test_light_and_thermostat", True, "functional")
        except Exception as e:
            TestUtils.yakshaAssert("test_light_and_thermostat", False, "functional")
            raise e
    
    def test_security_devices(self):
        """Test SecurityDevice and its subclasses (Camera and MotionSensor)."""
        try:
            # Test SecurityDevice base class
            security = SecurityDevice("S001", "Security Device", True, True, "Front Door", "Disarmed", 80)
            assert isinstance(security, Device)
            assert security.armed_status == "Disarmed"
            assert security.sensitivity == 80
            
            security.arm()
            assert security.armed_status == "Armed"
            
            security.disarm()
            assert security.armed_status == "Disarmed"
            
            # Test Camera subclass
            camera = Camera("C001", "Front Door Camera", True, True, "Front Door", "Disarmed", 80, "1080p", False)
            assert isinstance(camera, SecurityDevice)
            assert isinstance(camera, Device)
            assert camera.resolution == "1080p"
            assert camera.recording == False
            
            camera.start_recording()
            assert camera.recording == True
            
            camera.arm()
            assert camera.armed_status == "Armed"
            assert camera.recording == True  # Start recording when armed
            
            camera.disarm()
            assert camera.armed_status == "Disarmed"
            assert camera.recording == False  # Stop recording when disarmed
            
            # Test MotionSensor subclass
            motion = MotionSensor("M001", "Backyard Sensor", True, True, "Backyard", "Armed", 60, 10, None)
            assert isinstance(motion, SecurityDevice)
            assert motion.detection_range == 10
            assert motion.last_triggered == None
            
            motion.detect_motion("12:00")
            assert motion.last_triggered == "12:00"
            
            motion.reset_trigger()
            assert motion.last_triggered == None
            
            motion.disarm()
            motion.detect_motion("13:00")
            assert motion.last_triggered == None  # Should not detect when disarmed
            
            motion.arm()
            motion.detect_motion("14:00")
            assert motion.last_triggered == "14:00"
            
            TestUtils.yakshaAssert("test_security_devices", True, "functional")
        except Exception as e:
            TestUtils.yakshaAssert("test_security_devices", False, "functional")
            raise e
    
    def test_polymorphism(self):
        """Test polymorphic behavior across all device classes."""
        try:
            # Create devices of different types
            light = Light("L001", "Living Room Light", True, True, "Living Room", 80, "White")
            thermostat = Thermostat("T001", "Main Thermostat", True, True, "Living Room", 22.5, "Heat", 23.0)
            camera = Camera("C001", "Front Door Camera", True, True, "Front Door", "Disarmed", 80, "1080p", False)
            motion = MotionSensor("M001", "Backyard Sensor", True, True, "Backyard", "Armed", 60, 10, None)
            
            # Create a list of devices to test polymorphic behavior
            devices = [light, thermostat, camera, motion]
            
            # Test display_info polymorphism
            for device in devices:
                info = device.display_info()
                assert device.id in info
                assert device.name in info
                
                # Each type should include its specific attributes
                if isinstance(device, Light):
                    assert "Brightness" in info
                    assert "Color" in info
                elif isinstance(device, Thermostat):
                    assert "Current" in info
                    assert "Target" in info
                    assert "Mode" in info
                elif isinstance(device, Camera):
                    assert "Resolution" in info
                    assert "Not Recording" in info
                elif isinstance(device, MotionSensor):
                    assert "Range" in info
                
            # Test toggle_power polymorphism
            for device in devices:
                initial_state = device.is_on
                device.toggle_power()
                assert device.is_on != initial_state
                
                # Type-specific behaviors
                if isinstance(device, Thermostat):
                    assert device.mode == "Off"
                elif isinstance(device, SecurityDevice):
                    assert device.armed_status == "Disarmed"
            
            TestUtils.yakshaAssert("test_polymorphism", True, "functional")
        except Exception as e:
            TestUtils.yakshaAssert("test_polymorphism", False, "functional")
            raise e
    
    def test_smart_home_device_management(self):
        """Test SmartHome device management capabilities."""
        try:
            # Create SmartHome
            home = SmartHome("My Smart Home")
            assert home.name == "My Smart Home"
            assert home.mode == "Home"
            
            # Create various devices
            light = Light("L001", "Living Room Light", True, True, "Living Room", 80, "White")
            thermostat = Thermostat("T001", "Main Thermostat", True, True, "Living Room", 22.5, "Heat", 23.0)
            camera = Camera("C001", "Front Door Camera", True, True, "Front Door", "Disarmed", 80, "1080p", False)
            
            # Test add_device
            home.add_device(light)
            home.add_device(thermostat)
            home.add_device(camera)
            assert len(home.devices) == 3
            
            # Test get_devices_by_type
            lights = home.get_devices_by_type(Light)
            assert len(lights) == 1
            assert lights[0].id == "L001"
            
            security_devices = home.get_devices_by_type(SecurityDevice)
            assert len(security_devices) == 1
            assert security_devices[0].id == "C001"
            
            # Test get_devices_by_room
            living_room_devices = home.get_devices_by_room("Living Room")
            assert len(living_room_devices) == 2
            assert any(d.id == "L001" for d in living_room_devices)
            assert any(d.id == "T001" for d in living_room_devices)
            
            # Test find_device
            found_light = home.find_device("L001")
            assert found_light.id == "L001"
            assert isinstance(found_light, Light)
            
            # Test remove_device
            assert home.remove_device("L001") == True
            assert len(home.devices) == 2
            assert len(home.get_devices_by_type(Light)) == 0
            
            # Test find non-existent device
            try:
                home.find_device("L001")
                assert False, "Should raise DeviceNotFoundException"
            except:
                pass  # Expected behavior
            
            TestUtils.yakshaAssert("test_smart_home_device_management", True, "functional")
        except Exception as e:
            TestUtils.yakshaAssert("test_smart_home_device_management", False, "functional")
            raise e
    
    def test_smart_home_automations(self):
        """Test SmartHome automation capabilities."""
        try:
            # Create SmartHome
            home = SmartHome("My Smart Home")
            
            # Create devices for automation testing
            kitchen_light = Light("L001", "Kitchen Light", False, True, "Kitchen", 80, "White")
            bedroom_light = Light("L002", "Bedroom Light", False, True, "Bedroom", 80, "White")
            living_room_light = Light("L003", "Living Room Light", True, True, "Living Room", 80, "White")
            thermostat = Thermostat("T001", "Main Thermostat", True, True, "Living Room", 22.5, "Heat", 23.0)
            camera = Camera("C001", "Front Door Camera", True, True, "Front Door", "Disarmed", 80, "1080p", False)
            motion = MotionSensor("M001", "Backyard Sensor", True, True, "Backyard", "Armed", 60, 10, None)
            
            # Add all devices to home
            home.add_device(kitchen_light)
            home.add_device(bedroom_light)
            home.add_device(living_room_light)
            home.add_device(thermostat)
            home.add_device(camera)
            home.add_device(motion)
            
            # Test Good Morning automation
            home.execute_automation("Good Morning")
            
            # Check expected changes
            assert kitchen_light.is_on == True
            assert kitchen_light.brightness == 100
            assert bedroom_light.is_on == True
            assert bedroom_light.brightness == 60
            assert thermostat.target_temp == 22
            assert thermostat.mode == "Heat"
            
            # Test Good Night automation
            home.execute_automation("Good Night")
            
            # Check expected changes
            assert kitchen_light.is_on == False
            assert bedroom_light.is_on == False
            assert living_room_light.is_on == False
            assert camera.armed_status == "Armed"
            assert motion.armed_status == "Armed"
            assert thermostat.target_temp == 18
            
            # Test Away Mode automation
            home.execute_automation("Away Mode")
            
            # Check expected changes
            assert thermostat.target_temp == 16
            assert thermostat.mode == "Auto"
            assert camera.armed_status == "Armed"
            
            # Test mode change triggering automation
            home.change_mode("Home")
            assert kitchen_light.is_on == True  # Should be turned on by Good Morning
            assert bedroom_light.is_on == True  # Should be turned on by Good Morning
            
            TestUtils.yakshaAssert("test_smart_home_automations", True, "functional")
        except Exception as e:
            TestUtils.yakshaAssert("test_smart_home_automations", False, "functional")
            raise e
    
    def test_encapsulation(self):
        """Test proper encapsulation with protected and private attributes."""
        try:
            # Test Device protected attributes
            device = Device("D001", "Test Device", True, True, "Living Room")
            
            # Verify protected attribute naming
            assert hasattr(device, "_id")
            assert hasattr(device, "_name")
            assert hasattr(device, "_is_on")
            assert hasattr(device, "_connected")
            assert hasattr(device, "_location")
            
            # Test SmartHome private attributes
            home = SmartHome("My Smart Home")
            
            # Verify private attribute naming with name mangling
            assert hasattr(home, "_SmartHome__name")
            assert hasattr(home, "_SmartHome__devices")
            assert hasattr(home, "_SmartHome__rooms")
            assert hasattr(home, "_SmartHome__mode")
            
            # Test immutability of returned collections
            devices_copy = home.devices
            assert len(devices_copy) == 0
            
            home.add_device(device)
            assert len(home.devices) == 1
            assert len(devices_copy) == 0  # Original copy unchanged
            
            # Test private attribute access via properties
            assert home.name == "My Smart Home"
            assert isinstance(home.devices, list)
            assert isinstance(home.rooms, set)
            assert home.mode == "Home"
            
            TestUtils.yakshaAssert("test_encapsulation", True, "functional")
        except Exception as e:
            TestUtils.yakshaAssert("test_encapsulation", False, "functional")
            raise e