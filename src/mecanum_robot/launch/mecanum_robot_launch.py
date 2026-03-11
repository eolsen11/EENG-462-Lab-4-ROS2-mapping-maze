import launch
from launch.substitutions import Command, LaunchConfiguration
import launch_ros
import os

def generate_launch_description():
    pkgPath = launch_ros.substitutions.FindPackageShare(package='urdf_test').find('urdf_test')
    urdfModelPath= os.path.join(pkgPath, 'urdf/model.urdf')

    # This node launches the driver I wrote for the yaboom board
    Node(
        package='mecanum_robot',
        namespace='ros_robot',
        executable='mecanum_robot',         # Do I need to specify it as a .py?
        name='robot'
    ),
    
    # This code launches the rplidar code, change to a different executable for non-rviz
    # TODO: seperate rviz to launch separately from rplidar
    Node(
        package='rplidar_ros',
        namespace='ros_robot',
        executable='view_rplidar_a1_launch.py',
        name='rplidar'
    ),

    # This launches the SLAM toolbox
    Node(
        package='slam_toolbox',
        namespace='ros_robot',
        executable='online_async_launch.py',
        name='slam_mapping'
    ),


