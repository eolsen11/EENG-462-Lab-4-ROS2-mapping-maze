# EENG-462-Lab-4-ROS2-mapping-maze

## Background

The class provided this repo for working with the lidar sensor
https://github.com/Slamtec/sllidar_ros2.git

specifically we have the SLLIDAR model A1 so we need to run
`ros2 launch sllidar_ros2 view_sllidar_a1_launch.py`

Here's a repo by Yaboom for an ROS2 implementation of the gmapping SLAM algo
https://www.yahboom.net/public/upload/upload-html/1699598882/7.ROS2_Gmapping%20mapping%20algorithm.html
https://github.com/Project-MANAS/slam_gmapping

This git repo is a bit of a mess because it has two packages that depend on one another within the git repo, not having a distinct git repo per-package

I also struggled to get the "map" to show up. Here's a supposed solution. I have yet to test it.
https://github.com/Project-MANAS/slam_gmapping/issues/9

Here's another slam module, but I couldn't build it due to problems with opencv
https://github.com/TixiaoShan/LIO-SAM/tree/ros2?tab=readme-ov-file#prepare-lidar-data

Found this resource for debugging using GDB
https://juraph.com/miscellaneous/ros2_and_gdb/

This creates a pdf of our transform tree
```ros2 run tf2_tools view_frames```

This blog talks about what is necessary for the lidar to work w mapping
https://www.modularmachines.ai/security_robot/2025/02/08/SecurityRobot-RPLidar.html
They also implement ros2_control, probably a tangent given my time limit
https://www.modularmachines.ai/security_robot/2025/02/22/SecurityRobot-Ros2_control.html
Here's a mapping thing they did with a tool called nav2 slam
https://www.modularmachines.ai/security_robot/2025/05/26/SecurityRobot-Mapping.html

These articles suggest maybe a tool called slam_toolbox is standard?
https://github.com/SteveMacenski/slam_toolbox I'm gonna use branch humble
I had to install a package called libcholmod3. IDK if it's the right one but colcon was complaining that it didn't have CHOLMOD libs. I also installed libsuitesparse-dev

Got further errors RQ-ing a package called ceres, but I need to go for now. I'll push just to document my research

A classmate told me to publish the encoder data from the wheels so I did that

