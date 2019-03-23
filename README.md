# rosshow: Visualize ROS topics in a terminal

Have you ever SSH'ed into a robot to debug whether sensors are outputting
what they should, e.g. ```rostopic echo /camera/image_raw```?

If so, rosshow is for you.

This displays various sensor messages in a useful fashion using Unicode Braille art in the terminal so you don't need to fire up port forwards, rviz, or any other shenanigans just to see if something is working. It currently only supports a few types (Image, Imu, NavSatFix, LaserScan) but support for more types is coming. Contributions welcome!

# Installation

This package will install to your ROS bin directory, i.e. where other ROS binaries such as rostopic, rosnode, etc. are located. Or if you don't want to do that or don't have permissions, you can add it to your catkin workspace and run it using rosrun.

To install to the system:

```
cd rosshow
source /opt/ros/kinetic/setup.bash
./ros-install-this
```

# Usage
```
rosshow <topicname>
```

# Screenshots

## sensor_msgs/PointCloud2

![screenshot](/screenshot5.png?raw=true "screenshot")

## sensor_msgs/Image

![screenshot](/screenshot4.png?raw=true "screenshot")

## sensor_msgs/LaserScan

![screenshot](/screenshot0.png?raw=true "screenshot")

## sensor_msgs/Imu

![screenshot](/screenshot2.png?raw=true "screenshot")

## sensor_msgs/NavSatFix

![screenshot](/screenshot3.png?raw=true "screenshot")
