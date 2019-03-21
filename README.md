# rosshow: Visualize ROS topics in a terminal

Have you ever SSH'ed into a robot to debug whether sensors are outputting
what they should, e.g. ```rostopic echo /camera/image_raw```?

If so, rosshow is for you.

This displays various sensor messages in a useful fashion using Unicode Braille art in the terminal so you don't need to fire up port forwards, rviz, or any other shenanigans just to see if something is working. It currently only supports a few types (Image, Imu, NavSatFix, LaserScan) but support for more types is coming. Contributions welcome!

# Installation

This package will install to your ROS bin directory, i.e. where other ROS binaries such as rostopic, rosnode, etc. are located.

```
cd rosshow
source /opt/ros/kinetic/setup.bash
./ros-install-this
```

# Usage
```
./rosshow <topicname>
```

# Screenshots

## sensor_msgs/LaserScan and sensor_msgs/PointCloud2

![screenshot](/screenshot0.png?raw=true "screenshot")

## sensor_msgs/Imu

![screenshot](/screenshot2.png?raw=true "screenshot")

## sensor_msgs/NavSatFix

![screenshot](/screenshot3.png?raw=true "screenshot")

## sensor_msgs/Image

![screenshot](/screenshot4.png?raw=true "screenshot")
