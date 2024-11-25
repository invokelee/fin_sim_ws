import os
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument, RegisterEventHandler, ExecuteProcess, TimerAction, LogInfo
from launch.substitutions import Command, LaunchConfiguration
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
from ament_index_python.packages import get_package_prefix
from launch_ros.descriptions import ParameterValue
from launch.event_handlers import OnProcessExit

def generate_launch_description():

    description_package_name = "rb1_ros2_description"
    install_dir = get_package_prefix(description_package_name)

    # This is to find the models inside the models folder in rb1_ros2_description package
    gazebo_models_path = os.path.join(description_package_name, 'meshes')
    if 'GAZEBO_MODEL_PATH' in os.environ:
        os.environ['GAZEBO_MODEL_PATH'] = os.environ['GAZEBO_MODEL_PATH'] + \
            ':' + install_dir + '/share' + ':' + gazebo_models_path
    else:
        os.environ['GAZEBO_MODEL_PATH'] = install_dir + \
            "/share" + ':' + gazebo_models_path

    if 'GAZEBO_PLUGIN_PATH' in os.environ:
        os.environ['GAZEBO_PLUGIN_PATH'] = os.environ['GAZEBO_PLUGIN_PATH'] + \
            ':' + install_dir + '/lib'
    else:
        os.environ['GAZEBO_PLUGIN_PATH'] = install_dir + '/lib'

    print("GAZEBO MODELS PATH=="+str(os.environ["GAZEBO_MODEL_PATH"]))
    print("GAZEBO PLUGINS PATH=="+str(os.environ["GAZEBO_PLUGIN_PATH"]))

    use_sim_time = LaunchConfiguration('use_sim_time', default='true')

    # Define the launch arguments for the Gazebo launch file
    gazebo_launch_args = {
        'verbose': 'false',
        'pause': 'false',
    }

   # Include the Gazebo launch file with the modified launch arguments
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory('gazebo_ros'), 'launch'), '/gazebo.launch.py']),
        launch_arguments=gazebo_launch_args.items(),
    )

    # Define the robot model files to be used
    robot_desc_file = "rb1_ros2_base.urdf.xacro"
    robot_desc_path = os.path.join(get_package_share_directory(
        "rb1_ros2_description"), "xacro", robot_desc_file)

    robot_name_1 = "rb1_robot"

    rsp_robot1 = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        namespace=robot_name_1,
        parameters=[{'use_sim_time': use_sim_time,
                     'robot_description': ParameterValue(Command(['xacro ', robot_desc_path, ' robot_name:=', robot_name_1]), value_type=str)}],
        output="screen"
    )

    spawn_robot1 = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=['-entity', robot_name_1, '-x', '13.0', '-y', '-17.5', '-z', '0.0', '-Y', '3.14',
                   '-topic', robot_name_1+'/robot_description',
                   '-timeout', '180.0'
                  ]
    )

    load_joint_state_controller = ExecuteProcess(
        cmd=['ros2', 'control', 'load_controller', '--set-state', 'active',
            'joint_state_broadcaster'],
        output='screen'
    )
    
    load_diff_drive_controller = ExecuteProcess(
        cmd=['ros2', 'control', 'load_controller', '--set-state', 'active',
            'diffbot_base_controller'],
        output='screen'
    )

    load_diff_position_controller = ExecuteProcess(
        cmd=['ros2', 'control', 'load_controller', '--set-state', 'active',
            'position_controller'],
        output='screen'
    )

    


    return LaunchDescription([
        RegisterEventHandler(
            event_handler=OnProcessExit(
                target_action=spawn_robot1,
                on_exit = [
                    LogInfo(msg='After 3 sec. controller will be loaded...'),
                    TimerAction(
                        period=3.0,
                        actions=[
                            LogInfo(msg='Try to load controllers'),
                            load_joint_state_controller
                        ]
                    )
                ]
            )
        ),
        RegisterEventHandler(
            event_handler=OnProcessExit(
                target_action=load_joint_state_controller,
                on_exit=[load_diff_drive_controller],
                
            )
        ),
        RegisterEventHandler(
            event_handler=OnProcessExit(
                target_action=load_joint_state_controller,
                on_exit=[load_diff_position_controller],
                
            )
        ),
        
        # gazebo,
        rsp_robot1,
        spawn_robot1,
    ])
