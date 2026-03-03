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

