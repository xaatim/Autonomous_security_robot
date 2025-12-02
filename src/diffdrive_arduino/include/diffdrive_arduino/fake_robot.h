#ifndef DIFFDRIVE_ARDUINO_FAKE_ROBOT_H
#define DIFFDRIVE_ARDUINO_FAKE_ROBOT_H

#include <string>
#include <vector>

// Use the correct Humble headers
#include "hardware_interface/system_interface.hpp"
#include "hardware_interface/handle.hpp"
#include "hardware_interface/hardware_info.hpp"
#include "hardware_interface/types/hardware_interface_return_values.hpp"
#include "rclcpp/macros.hpp"
#include "rclcpp_lifecycle/node_interfaces/lifecycle_node_interface.hpp"
#include "rclcpp/rclcpp.hpp"

#include "diffdrive_arduino/config.h"
#include "diffdrive_arduino/wheel.h"

// Use the Humble CallbackReturn type
using CallbackReturn = rclcpp_lifecycle::node_interfaces::LifecycleNodeInterface::CallbackReturn;

// Inherit directly from SystemInterface
class FakeRobot : public hardware_interface::SystemInterface
{

public:
    RCLCPP_SHARED_PTR_DEFINITIONS(FakeRobot)

    FakeRobot();

    // These are the new Humble hardware interface functions
    CallbackReturn on_init(const hardware_interface::HardwareInfo & info) override;
    std::vector<hardware_interface::StateInterface> export_state_interfaces() override;
    std::vector<hardware_interface::CommandInterface> export_command_interfaces() override;
    CallbackReturn on_activate(const rclcpp_lifecycle::State & previous_state) override;
    CallbackReturn on_deactivate(const rclcpp_lifecycle::State & previous_state) override;
    hardware_interface::return_type read(const rclcpp::Time & time, const rclcpp::Duration & period) override;
    hardware_interface::return_type write(const rclcpp::Time & time, const rclcpp::Duration & period) override;

private:
    Config cfg_;
    Wheel l_wheel_;
    Wheel r_wheel_;
    rclcpp::Logger logger_;
};

#endif // DIFFDRIVE_ARDUINO_FAKE_ROBOT_H