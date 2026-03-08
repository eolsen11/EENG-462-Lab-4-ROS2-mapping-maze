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

