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

I messed with launch files for a bit and got nothing working right

I think I need to use robot_state_publisher with my urdf
https://docs.ros.org/en/humble/Tutorials/Intermediate/URDF/Using-URDF-with-Robot-State-Publisher-py.html

A classmate sent me some code for a node that published odometry data and broadcast transforms
I implemented it, I might need to modify some bits to get all the directions correct

I think I'll redo the init files to python since I can't find a good tutorial for adding urdf files in the xml init files

## TODO
Implement SLAM
	Write/incorporate URDF file
	Write URDF file with wheels, collision, LIDAR, camera pole, camera

Hug the right wall while mapping
	Follow right wall to end of map

Implement vslam
	Use vslam on the camera to detect green tape
	Waypoint in vslam on map to find exit (green tape on maze exit)
	How does ROS2 do waypoints on maps?
	How does ROS2 do vslam?

	Can I use a color sensor on the front of the robot to look for green tape?
