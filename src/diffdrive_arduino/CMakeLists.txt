cmake_minimum_required(VERSION 3.8)
project(diffdrive_arduino)

# Find ROS 2 Humble dependencies
find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(rclcpp_lifecycle REQUIRED)
find_package(hardware_interface REQUIRED)
find_package(pluginlib REQUIRED)
find_package(serial REQUIRED) # This is the C++ serial library

# --- Build diffdrive_arduino (Real Robot) ---
add_library(diffdrive_arduino SHARED
  src/diffdrive_arduino.cpp
  src/arduino_comms.cpp
  src/wheel.cpp
)
ament_target_dependencies(diffdrive_arduino
  rclcpp
  rclcpp_lifecycle
  hardware_interface
  pluginlib
  serial
)
target_include_directories(diffdrive_arduino PUBLIC
  $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
  $<INSTALL_INTERFACE:include>
)

# --- Build fake_robot ---
add_library(fake_robot SHARED
  src/fake_robot.cpp
  src/wheel.cpp
)
ament_target_dependencies(fake_robot
  rclcpp
  rclcpp_lifecycle
  hardware_interface
  pluginlib
)
target_include_directories(fake_robot PUBLIC
  $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
  $<INSTALL_INTERFACE:include>
)

# --- Export and Register Plugins ---
# This is the line (around 42) that fixes your error
# It now points to the single, correct plugins.xml file
pluginlib_export_plugin_description_file(hardware_interface plugins.xml)

# --- Install Rules ---
install(
  TARGETS diffdrive_arduino fake_robot
  ARCHIVE DESTINATION lib
  LIBRARY DESTINATION lib
  RUNTIME DESTINATION bin
)

install(
  DIRECTORY include/
  DESTINATION include
)

install(
  FILES plugins.xml
  DESTINATION share/${PROJECT_NAME}
)

# --- Final ROS 2 Setup ---
ament_package()