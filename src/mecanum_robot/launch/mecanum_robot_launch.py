import launch
from launch.substitutions import Command, LaunchConfiguration
from launch import LaunchDescription
import launch_ros
from launch_ros.actions import Node
import os
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    pkgPath = launch_ros.substitutions.FindPackageShare(package='mecanum_robot').find('mecanum_robot')
    urdfModelPath= os.path.join(pkgPath, 'urdf/mecanum_robot.urdf')

    # Launch lidar, taken from Canon
    lidar_launch = os.path.join(
        get_package_share_directory('rplidar_ros'),
        'launch',
        'rplidar_a1_launch.py'
    )

    # Launch slam_toolbox from here
    # https://tekbot-robotics-challenge.github.io/2025-Team-Epibot-Docs/week3/pole-it/slam_toolbox.html
    slam_config_file = os.path.join(
        get_package_share_directory('slam_toolbox'),
        'config',
        'mapper_params_online_async.yaml'
    )

    return LaunchDescription([
        
        # This node launches the driver I wrote for the yaboom board
        Node(
            package='mecanum_robot',
            namespace='ros_robot',
            executable='mecanum_robot',         # Do I need to specify it as a .py?
            name='robot'
        ),
    
        # This code launches the rplidar code, change to a different executable for non-rviz
        # TODO: seperate rviz to launch separately from rplidar
        launch.actions.IncludeLaunchDescription(
            launch.launch_description_sources.PythonLaunchDescriptionSource(lidar_launch)
        ),
#        Node(
#            package='rplidar_ros',
#            namespace='ros_robot',
#            #executable='view_rplidar_a1_launch.py',
#            executable='view_rplidar_a1_launch',
#            name='rplidar'
#        ),

        # This launches the SLAM toolbox
        Node(
            package='slam_toolbox',
            namespace='ros_robot',
            executable='async_slam_toolbox_node',
            name='slam_mapping',
            parameters=[slam_config_file]
        ),


    ])
    

