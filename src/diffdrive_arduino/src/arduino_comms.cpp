#include "diffdrive_arduino/arduino_comms.h"
#include <sstream>
#include <cstdlib>

// Updated setup to receive and store the logger
void ArduinoComms::setup(const std::string &serial_device, int32_t baud_rate, int32_t timeout_ms, rclcpp::Logger &logger)
{
    logger_ = logger; // Store the logger from the hardware interface
    serial_conn_.setPort(serial_device);
    serial_conn_.setBaudrate(baud_rate);
    serial::Timeout tt = serial::Timeout::simpleTimeout(timeout_ms);
    serial_conn_.setTimeout(tt);
    
    RCLCPP_INFO(logger_, "Opening serial port %s at %d baud...", serial_device.c_str(), baud_rate);
    try
    {
        serial_conn_.open();
    }
    catch (serial::IOException& e)
    {
        RCLCPP_ERROR(logger_, "Failed to open serial port: %s", e.what());
        return;
    }
    RCLCPP_INFO(logger_, "Serial port opened successfully.");
}


void ArduinoComms::sendEmptyMsg()
{
    std::string response = sendMsg("\r");
}

void ArduinoComms::readEncoderValues(int &val_1, int &val_2)
{
    std::string response = sendMsg("e\r");

    std::string delimiter = " ";
    size_t del_pos = response.find(delimiter);
    if (del_pos == std::string::npos)
    {
        RCLCPP_WARN(logger_, "Invalid encoder response. Got: '%s'", response.c_str());
        val_1 = 0;
        val_2 = 0;
        return;
    }
    std::string token_1 = response.substr(0, del_pos);
    std::string token_2 = response.substr(del_pos + delimiter.length());

    val_1 = std::atoi(token_1.c_str());
    val_2 = std::atoi(token_2.c_str());
}

void ArduinoComms::setMotorValues(int val_1, int val_2)
{
    std::stringstream ss;
    ss << "m " << val_1 << " " << val_2 << "\r";
    sendMsg(ss.str(), false); // Don't print output, too spammy
}

void ArduinoComms::setPidValues(float k_p, float k_d, float k_i, float k_o)
{
    std::stringstream ss;
    ss << "u " << k_p << ":" << k_d << ":" << k_i << ":" << k_o << "\r";
    sendMsg(ss.str());
}

std::string ArduinoComms::sendMsg(const std::string &msg_to_send, bool print_output)
{
    try
    {
        serial_conn_.write(msg_to_send);
        std::string response = serial_conn_.readline();

        if (print_output)
        {
            RCLCPP_INFO(logger_, "Sent: %s", msg_to_send.c_str());
            RCLCPP_INFO(logger_, "Received: %s", response.c_str());
        }
        return response;
    }
    catch (serial::IOException& e)
    {
        RCLCPP_ERROR(logger_, "Serial read/write error: %s", e.what());
        return "";
    }
    catch (serial::SerialException& e)
    {
        RCLCPP_ERROR(logger_, "Serial exception: %s", e.what());
        return "";
    }
}