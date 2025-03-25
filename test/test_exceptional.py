import pytest
from test.TestUtils import TestUtils
from smart_home_system import Device, Light, Thermostat, SecurityDevice, Camera, MotionSensor, SmartHome
from smart_home_system import DeviceNotFoundException, InvalidInputException

class TestExceptional:
    """Test cases for exceptional conditions in the smart home system."""
    
    def test_exception_handling(self):
        """Test all exception handling across the smart home system."""
        try:
            # Device validation exceptions
            try:
                Device("", "Test Device", True, True, "Test Room")
                assert False, "Empty id should be rejected"
            except InvalidInputException:
                pass  # Expected behavior
                
            try:
                Device(123, "Test Device", True, True, "Test Room")
                assert False, "Non-string id should be rejected"
            except InvalidInputException:
                pass  # Expected behavior
            
            # Light validation exceptions
            try:
                Light("L001", "Test Light", True, True, "Living Room", -10, "White")
                assert False, "Negative brightness should be rejected"
            except InvalidInputException:
                pass  # Expected behavior
                
            try:
                Light("L001", "Test Light", True, True, "Living Room", 110, "White")
                assert False, "Brightness > 100 should be rejected"
            except InvalidInputException:
                pass  # Expected behavior
            
            # Valid light but invalid dim method call
            light = Light("L001", "Test Light", True, True, "Living Room", 80, "White")
            try:
                light.dim(-5)
                assert False, "Negative brightness should be rejected"
            except InvalidInputException:
                pass  # Expected behavior
                
            try:
                light.dim(150)
                assert False, "Brightness > 100 should be rejected"
            except InvalidInputException:
                pass  # Expected behavior
            
            # Thermostat validation exceptions
            try:
                Thermostat("T001", "Test Thermostat", True, True, "Living Room", 0, "Heat", 22)
                assert False, "Temperature < 5 should be rejected"
            except InvalidInputException:
                pass  # Expected behavior
                
            try:
                Thermostat("T001", "Test Thermostat", True, True, "Living Room", 40, "Heat", 22)
                assert False, "Temperature > 35 should be rejected"
            except InvalidInputException:
                pass  # Expected behavior
                
            try:
                Thermostat("T001", "Test Thermostat", True, True, "Living Room", 22, "Invalid", 22)
                assert False, "Invalid mode should be rejected"
            except InvalidInputException:
                pass  # Expected behavior
                
            try:
                Thermostat("T001", "Test Thermostat", True, True, "Living Room", 22, "Heat", 0)
                assert False, "Target temperature < 5 should be rejected"
            except InvalidInputException:
                pass  # Expected behavior
                
            try:
                Thermostat("T001", "Test Thermostat", True, True, "Living Room", 22, "Heat", 40)
                assert False, "Target temperature > 35 should be rejected"
            except InvalidInputException:
                pass  # Expected behavior
            
            # Valid thermostat but invalid method calls
            thermostat = Thermostat("T001", "Test Thermostat", True, True, "Living Room", 22, "Heat", 23)
            try:
                thermostat.set_temperature(0)
                assert False, "Target temperature < 5 should be rejected"
            except InvalidInputException:
                pass  # Expected behavior
                
            try:
                thermostat.set_temperature(40)
                assert False, "Target temperature > 35 should be rejected"
            except InvalidInputException:
                pass  # Expected behavior
                
            try:
                thermostat.change_mode("Invalid")
                assert False, "Invalid mode should be rejected"
            except InvalidInputException:
                pass  # Expected behavior
            
            # SecurityDevice validation exceptions
            try:
                SecurityDevice("S001", "Test Security", True, True, "Front Door", "Armed", -10)
                assert False, "Negative sensitivity should be rejected"
            except InvalidInputException:
                pass  # Expected behavior
                
            try:
                SecurityDevice("S001", "Test Security", True, True, "Front Door", "Armed", 110)
                assert False, "Sensitivity > 100 should be rejected"
            except InvalidInputException:
                pass  # Expected behavior
            
            # Camera validation should inherit from SecurityDevice
            try:
                Camera("C001", "Test Camera", True, True, "Front Door", "Armed", -10, "1080p", False)
                assert False, "Negative sensitivity should be rejected"
            except InvalidInputException:
                pass  # Expected behavior
            
            # MotionSensor validation should inherit from SecurityDevice
            try:
                MotionSensor("M001", "Test Motion", True, True, "Backyard", "Armed", -10, 10, None)
                assert False, "Negative sensitivity should be rejected"
            except InvalidInputException:
                pass  # Expected behavior
            
            # Test behavior of methods when device is off or disarmed
            security = SecurityDevice("S001", "Test Security", False, True, "Front Door", "Disarmed", 80)
            assert security.arm() == "Disarmed", "Arming should fail when device is off"
            
            security = SecurityDevice("S001", "Test Security", True, True, "Front Door", "Disarmed", 80)
            security.arm()
            security.toggle_power()  # Turn off
            assert security.armed_status == "Disarmed", "Device should be disarmed when off"
            
            camera = Camera("C001", "Test Camera", False, True, "Front Door", "Disarmed", 80, "1080p", False)
            assert camera.start_recording() is False, "Recording should fail when device is off"
            
            motion = MotionSensor("M001", "Test Motion", False, True, "Backyard", "Disarmed", 80, 10, None)
            assert motion.detect_motion("12:00") is None, "Detection should fail when device is off"
            
            motion = MotionSensor("M001", "Test Motion", True, True, "Backyard", "Disarmed", 80, 10, None)
            assert motion.detect_motion("12:00") is None, "Detection should fail when device is disarmed"
            
            # SmartHome validation and exceptional behavior tests
            home = SmartHome("Test Home")
            
            # Adding non-Device objects should be rejected
            try:
                home.add_device("not a device")
                assert False, "Non-Device object should be rejected"
            except InvalidInputException:
                pass  # Expected behavior
            
            # Finding a non-existent device should raise DeviceNotFoundException
            try:
                home.find_device("NONEXISTENT")
                assert False, "Should raise DeviceNotFoundException for non-existent ID"
            except DeviceNotFoundException:
                pass  # Expected behavior
            
            # Removing a non-existent device should return False
            assert home.remove_device("NONEXISTENT") is False
            
            # Test changing to an invalid mode
            try:
                home.change_mode("Invalid")
                assert False, "Invalid mode should be rejected"
            except InvalidInputException:
                pass  # Expected behavior
            
            # Test device list immutability
            home.add_device(Device("D001", "Test Device", True, True, "Test Room"))
            devices_copy = home.devices
            
            # Modify the copy (should not affect original)
            if len(devices_copy) > 0:
                devices_copy.pop()
            
            # Verify home's devices list wasn't affected
            assert len(home.devices) == 1
            
            # Test duplicate device addition
            device = Device("D001", "Test Device", True, True, "Test Room")
            assert home.add_device(device) is False, "Duplicate device addition should return False"
            
            # Test executing a non-existent automation
            assert home.execute_automation("Non-existent") is False
            
            # Test edge cases in automations
            empty_home = SmartHome("Empty Home")
            assert empty_home.execute_automation("Good Morning") is True, "Automation should succeed even with no devices"
            assert empty_home.change_mode("Away") == "Away", "Mode change should succeed even with no devices"
            
            # Test complex interaction scenario with device state changes
            test_home = SmartHome("Complex Home")
            
            # Add devices for complex testing
            light = Light("L001", "Test Light", False, True, "Living Room", 50, "White")
            thermostat = Thermostat("T001", "Test Thermostat", True, True, "Living Room", 22, "Heat", 23)
            camera = Camera("C001", "Test Camera", True, False, "Front Door", "Disarmed", 80, "1080p", False)
            
            test_home.add_device(light)
            test_home.add_device(thermostat)
            test_home.add_device(camera)
            
            # Run Good Morning automation (should turn on lights and set thermostat)
            test_home.execute_automation("Good Morning")
            
            # Disconnect devices (simulating network failure)
            light.disconnect()
            thermostat.disconnect()
            camera.disconnect()
            
            # Connected devices count should be 0
            info = test_home.display_info()
            assert "Connected Devices: 0/3" in info
            
            # Run Away Mode automation (should still work with disconnected devices)
            test_home.execute_automation("Away Mode")
            
            # Automation should have affected device states even when disconnected
            assert light.is_on is False  # Should be turned off
            assert thermostat.target_temp == 16  # Should be set to energy saving
            assert camera.armed_status == "Armed"  # Should be armed
            
            # Removing all devices should not cause errors
            test_home.remove_device("L001")
            test_home.remove_device("T001")
            test_home.remove_device("C001")
            
            assert len(test_home.devices) == 0
            assert len(test_home.rooms) == 0
            
            # Display info should still work with empty home
            info = test_home.display_info()
            assert "Total Devices: 0" in info
            
            TestUtils.yakshaAssert("test_exception_handling", True, "exceptional")
        except Exception as e:
            TestUtils.yakshaAssert("test_exception_handling", False, "exceptional")
            raise e