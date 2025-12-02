#include "diffdrive_arduino/diffdrive_arduino.h"
#include "hardware_interface/types/hardware_interface_type_values.hpp"
#include "rclcpp/rclcpp.hpp"

DiffDriveArduino::DiffDriveArduino()
    : logger_(rclcpp::get_logger("DiffDriveArduino"))
{}

// This replaces the old 'configure' function
CallbackReturn DiffDriveArduino::on_init(const hardware_interface::HardwareInfo & info)
{
    // This is the required call to the base class
    if (hardware_interface::SystemInterface::on_init(info) != CallbackReturn::SUCCESS)
    {
        return CallbackReturn::ERROR;
    }

    RCLCPP_INFO(logger_, "Configuring...");

    // Read parameters from the URDF
    cfg_.left_wheel_name = info_.hardware_parameters["left_wheel_name"];
    cfg_.right_wheel_name = info_.hardware_parameters["right_wheel_name"];
    cfg_.loop_rate = std::stof(info_.hardware_parameters["loop_rate"]);
    cfg_.device = info_.hardware_parameters["device"];
    cfg_.baud_rate = std::stoi(info_.hardware_parameters["baud_rate"]);
    cfg_.timeout = std::stoi(info_.hardware_parameters["timeout"]);
    cfg_.enc_counts_per_rev = std::stoi(info_.hardware_parameters["enc_counts_per_rev"]);

    RCLCPP_INFO(logger_, "Hardware Parameters:");
    RCLCPP_INFO(logger_, " - left_wheel_name: %s", cfg_.left_wheel_name.c_str());
    RCLCPP_INFO(logger_, " - right_wheel_name: %s", cfg_.right_wheel_name.c_str());
    RCLCPP_INFO(logger_, " - loop_rate: %f", cfg_.loop_rate);
    RCLCPP_INFO(logger_, " - device: %s", cfg_.device.c_str());
    RCLCPP_INFO(logger_, " - baud_rate: %d", cfg_.baud_rate);
    RCLCPP_INFO(logger_, " - timeout: %d", cfg_.timeout);
    RCLCPP_INFO(logger_, " - enc_counts_per_rev: %d", cfg_.enc_counts_per_rev);

    // Set up the wheels
    l_wheel_.setup(cfg_.left_wheel_name, cfg_.enc_counts_per_rev);
    r_wheel_.setup(cfg_.right_wheel_name, cfg_.enc_counts_per_rev);

    // Set up the Arduino comms
    // We pass the logger from this node to the comms class
    arduino_.setup(cfg_.device, cfg_.baud_rate, cfg_.timeout, logger_);

    RCLCPP_INFO(logger_, "Finished Configuration");
    return CallbackReturn::SUCCESS;
}

std::vector<hardware_interface::StateInterface> DiffDriveArduino::export_state_interfaces()
{
    std::vector<hardware_interface::StateInterface> state_interfaces;

    // Export state interfaces for position and velocity for both wheels
    state_interfaces.emplace_back(hardware_interface::StateInterface(l_wheel_.name, hardware_interface::HW_IF_POSITION, &l_wheel_.pos));
    state_interfaces.emplace_back(hardware_interface::StateInterface(l_wheel_.name, hardware_interface::HW_IF_VELOCITY, &l_wheel_.vel));
    state_interfaces.emplace_back(hardware_interface::StateInterface(r_wheel_.name, hardware_interface::HW_IF_POSITION, &r_wheel_.pos));
    state_interfaces.emplace_back(hardware_interface::StateInterface(r_wheel_.name, hardware_interface::HW_IF_VELOCITY, &r_wheel_.vel));

    return state_interfaces;
}

std::vector<hardware_interface::CommandInterface> DiffDriveArduino::export_command_interfaces()
{
    std::vector<hardware_interface::CommandInterface> command_interfaces;

    // Export command interface for velocity for both wheels
    command_interfaces.emplace_back(hardware_interface::CommandInterface(l_wheel_.name, hardware_interface::HW_IF_VELOCITY, &l_wheel_.cmd));
    command_interfaces.emplace_back(hardware_interface::CommandInterface(r_wheel_.name, hardware_interface::HW_IF_VELOCITY, &r_wheel_.cmd));

    return command_interfaces;
}

// This replaces the old 'start' function
CallbackReturn DiffDriveArduino::on_activate(const rclcpp_lifecycle::State & /*previous_state*/)
{
    RCLCPP_INFO(logger_, "Starting Controller...");
    if (!arduino_.connected())
    {
        RCLCPP_ERROR(logger_, "Arduino not connected, cannot start.");
        return CallbackReturn::ERROR;
    }
    arduino_.sendEmptyMsg();
    arduino_.setPidValues(30, 20, 0, 100);
    RCLCPP_INFO(logger_, "PID values set. Controller activated.");
    return CallbackReturn::SUCCESS;
}

// This replaces the old 'stop' function
CallbackReturn DiffDriveArduino::on_deactivate(const rclcpp_lifecycle::State & /*previous_state*/)
{
    RCLCPP_INFO(logger_, "Stopping Controller...");
    // Stop the motors
    arduino_.setMotorValues(0, 0);
    RCLCPP_INFO(logger_, "Motors stopped. Controller deactivated.");
    return CallbackReturn::SUCCESS;
}

// This is the new 'read' function signature
hardware_interface::return_type DiffDriveArduino::read(const rclcpp::Time & /*time*/, const rclcpp::Duration & period)
{
    if (!arduino_.connected())
    {
        return hardware_interface::return_type::ERROR;
    }

    double deltaSeconds = period.seconds();

    arduino_.readEncoderValues(l_wheel_.enc, r_wheel_.enc);

    double pos_prev = l_wheel_.pos;
    l_wheel_.pos = l_wheel_.calcEncAngle();
    l_wheel_.vel = (l_wheel_.pos - pos_prev) / deltaSeconds;

    pos_prev = r_wheel_.pos;
    r_wheel_.pos = r_wheel_.calcEncAngle();
    r_wheel_.vel = (r_wheel_.pos - pos_prev) / deltaSeconds;

    return hardware_interface::return_type::OK;
}

// This is the new 'write' function signature
hardware_interface::return_type DiffDriveArduino::write(const rclcpp::Time & /*time*/, const rclcpp::Duration & /*period*/)
{
    if (!arduino_.connected())
    {
        return hardware_interface::return_type::ERROR;
    }

    // Convert commanded rad/s to encoder ticks per loop
    int l_motor_ticks = static_cast<int>(l_wheel_.cmd / l_wheel_.rads_per_count / cfg_.loop_rate);
    int r_motor_ticks = static_cast<int>(r_wheel_.cmd / r_wheel_.rads_per_count / cfg_.loop_rate);
    
    arduino_.setMotorValues(l_motor_ticks, r_motor_ticks);

    return hardware_interface::return_type::OK;
}

#include "pluginlib/class_list_macros.hpp"

PLUGINLIB_EXPORT_CLASS(
    DiffDriveArduino,
    hardware_interface::SystemInterface
)