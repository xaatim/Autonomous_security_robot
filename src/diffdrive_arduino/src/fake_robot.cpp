#include "diffdrive_arduino/fake_robot.h"
#include "hardware_interface/types/hardware_interface_type_values.hpp"
#include "rclcpp/rclcpp.hpp"


FakeRobot::FakeRobot()
    : logger_(rclcpp::get_logger("FakeRobot"))
{}


CallbackReturn FakeRobot::on_init(const hardware_interface::HardwareInfo & info)
{
    if (hardware_interface::SystemInterface::on_init(info) != CallbackReturn::SUCCESS)
    {
        return CallbackReturn::ERROR;
    }

    RCLCPP_INFO(logger_, "Configuring...");

    cfg_.left_wheel_name = info_.hardware_parameters["left_wheel_name"];
    cfg_.right_wheel_name = info_.hardware_parameters["right_wheel_name"];
    
    // Check if enc_counts_per_rev is provided, otherwise use default
    if (info_.hardware_parameters.count("enc_counts_per_rev"))
    {
        cfg_.enc_counts_per_rev = std::stoi(info_.hardware_parameters["enc_counts_per_rev"]);
    }
    else
    {
        RCLCPP_INFO(logger_, "enc_counts_per_rev not provided, using default 1920");
        cfg_.enc_counts_per_rev = 1920;
    }

    // Set up the wheels
    l_wheel_.setup(cfg_.left_wheel_name, cfg_.enc_counts_per_rev);
    r_wheel_.setup(cfg_.right_wheel_name, cfg_.enc_counts_per_rev);

    RCLCPP_INFO(logger_, "Finished Configuration");
    return CallbackReturn::SUCCESS;
}

std::vector<hardware_interface::StateInterface> FakeRobot::export_state_interfaces()
{
    std::vector<hardware_interface::StateInterface> state_interfaces;

    state_interfaces.emplace_back(hardware_interface::StateInterface(l_wheel_.name, hardware_interface::HW_IF_VELOCITY, &l_wheel_.vel));
    state_interfaces.emplace_back(hardware_interface::StateInterface(l_wheel_.name, hardware_interface::HW_IF_POSITION, &l_wheel_.pos));
    state_interfaces.emplace_back(hardware_interface::StateInterface(r_wheel_.name, hardware_interface::HW_IF_VELOCITY, &r_wheel_.vel));
    state_interfaces.emplace_back(hardware_interface::StateInterface(r_wheel_.name, hardware_interface::HW_IF_POSITION, &r_wheel_.pos));

    return state_interfaces;
}

std::vector<hardware_interface::CommandInterface> FakeRobot::export_command_interfaces()
{
    std::vector<hardware_interface::CommandInterface> command_interfaces;

    command_interfaces.emplace_back(hardware_interface::CommandInterface(l_wheel_.name, hardware_interface::HW_IF_VELOCITY, &l_wheel_.cmd));
    command_interfaces.emplace_back(hardware_interface::CommandInterface(r_wheel_.name, hardware_interface::HW_IF_VELOCITY, &r_wheel_.cmd));

    return command_interfaces;
}


CallbackReturn FakeRobot::on_activate(const rclcpp_lifecycle::State & /*previous_state*/)
{
    RCLCPP_INFO(logger_, "Starting FakeRobot Controller...");
    return CallbackReturn::SUCCESS;
}

CallbackReturn FakeRobot::on_deactivate(const rclcpp_lifecycle::State & /*previous_state*/)
{
    RCLCPP_INFO(logger_, "Stopping FakeRobot Controller...");
    return CallbackReturn::SUCCESS;
}

hardware_interface::return_type FakeRobot::read(const rclcpp::Time & /*time*/, const rclcpp::Duration & period)
{
    double deltaSeconds = period.seconds();

    // Simulate wheel position based on last command
    l_wheel_.pos = l_wheel_.pos + l_wheel_.vel * deltaSeconds;
    r_wheel_.pos = r_wheel_.pos + r_wheel_.vel * deltaSeconds;

    return hardware_interface::return_type::OK;
}

hardware_interface::return_type FakeRobot::write(const rclcpp::Time & /*time*/, const rclcpp::Duration & /*period*/)
{
    // The fake robot's velocity is just whatever is commanded
    l_wheel_.vel = l_wheel_.cmd;
    r_wheel_.vel = r_wheel_.cmd;

    return hardware_interface::return_type::OK;
}

#include "pluginlib/class_list_macros.hpp"

PLUGINLIB_EXPORT_CLASS(
    FakeRobot,
    hardware_interface::SystemInterface
)