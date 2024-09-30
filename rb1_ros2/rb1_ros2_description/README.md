
# The rb1_ros2_description package

This package contains a ROS2 robot model description for Robotnik's RB-1 mobile base.   

## Disclaimer:  
This package only modifies/adapts files from these repositories/packages:  
- [RobotnikAutomation/rb1_base_sim](https://github.com/RobotnikAutomation/rb1_base_sim) licensed under the BSD 2-Clause "Simplified" License
- [RobotnikAutomation/rb1_base_common/rb1_base_description](https://github.com/RobotnikAutomation/rb1_base_common/tree/melodic-devel/rb1_base_description), licensed under the BSD License
- [RobotnikAutomation/robotnik_sensors],(https://github.com/RobotnikAutomation/robotnik_sensors) licensed under the BSD License

\
It is designed to test `ros2_control` possibilieties for ROS Masterclass, CP8:
- Enable the differential drive ROS2 control controller
- Implement a solution to have a functional lifting unit

To install this package, clone it in your workspace `src` folder and build it with command: `colcon build --packages-select rb1_ros2_description`

**Rememeber** to install required dependencies:
- xacro
- urdf
- robot_state_publisher
- `ros2_control` and `gazebo` related packages


To launch this package source your workspace and use command: `ros2 launch rb1_ros2_description rb1_ros2_xacro.launch.py`

To list hardware interfaces, use: `ros2 control list_hardware_interfaces`

To list controllers and check their states, use: `ros2 control list_controllers`

To change controller state, use: `ros2 control set_controller_state "{controller_name}" stop/start/configure`

To load/unload controller, use: `ros2 control load/unload_controller "{controller_name}"`

## For task 1:
The robot can be controlled via keyboard teleoperation or by sending velocity commands via the command line on topic `/diffbot_base_controller/cmd_vel_unstamped`. 
\
Try: `ros2 run teleop_twist_keyboard teleop_twist_keyboard --ros-args -r /cmd_vel:=diffbot_base_controller/cmd_vel_unstamped`


## For task 1:

This package use ROS2 Control **position_controllers** controller for the robot's lifting mechanism. By default controller is already loaded and active. All you need to do is publish data on topic `/position_controller/commands` for joint `robot_evelator_platform_joint`.

To lift platform: `ros2 topic pub  /position_controller/commands std_msgs/msg/Float64MultiArray "{data: [0.034]}" -1`
\
To let down: `ros2 topic pub  /position_controller/commands std_msgs/msg/Float64MultiArray "{data: [0.0]}" -1`




