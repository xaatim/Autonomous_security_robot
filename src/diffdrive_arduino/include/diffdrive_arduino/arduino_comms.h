#ifndef DIFFDRIVE_ARDUINO_ARDUINO_COMMS_H
#define DIFFDRIVE_ARDUINO_ARDUINO_COMMS_H

#include <serial/serial.h>
#include <string>
#include "rclcpp/rclcpp.hpp" // For logging

class ArduinoComms
{
public:
    ArduinoComms() = default;

    // Pass logger in setup
    void setup(const std::string &serial_device, int32_t baud_rate, int32_t timeout_ms, rclcpp::Logger &logger);
    void sendEmptyMsg();
    void readEncoderValues(int &val_1, int &val_2);
    void setMotorValues(int val_1, int val_2);
    void setPidValues(float k_p, float k_d, float k_i, float k_o);
    bool connected() const { return serial_conn_.isOpen(); }

private:
    std::string sendMsg(const std::string &msg_to_send, bool print_output = true);

    serial::Serial serial_conn_;
    // Store the logger
    rclcpp::Logger logger_ = rclcpp::get_logger("ArduinoComms"); 
};

#endif // DIFFDRIVE_ARDUINO_ARDUINO_COMMS_H