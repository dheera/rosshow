# rosshow: Visualize ROS topics in a terminal

Have you ever SSH'ed into a robot to debug whether sensors are outputting
what they should, e.g. ```rostopic echo /camera/image_raw```?

If so, rosshow is for you.

This displays various sensor messages in a useful fashion using Unicode Braille art in the terminal so you don't need to fire up port forwards, rviz, or any other shenanigans just to see if something is working. It currently only supports types from std_msgs and sensor_msgs but support for more types is coming. Contributions welcome!

# Installation

Prerequisites:

```
sudo pip install numpy pillow requests
```

This package will install to your ROS bin directory, i.e. where other ROS binaries such as rostopic, rosnode, etc. are located. Or if you don't want to do that or don't have permissions, you can add it to your catkin workspace and run it using rosrun.

To install to the system:

```
source /opt/ros/<kinetic, melodic, noetic>/setup.bash
./configure-ros1
./ros-install-this
```

# Usage

If you installed it to the system:

```
rosshow <topicname>
```

If you're using it from a catkin workspace:

```
rosrun rosshow rosshow <topicname>
```

Most visualizations use Unicode Braille characters to render visualizations. If your terminal supports only ASCII, you can use the `-a` option for a purely ASCII-art render:
```
rosshow -a <topicname>
```
You can also force 1-bit, 4-bit, or 24-bit color modes if your terminal type is not detected correctly. You may need these when using rosshow inside of a `screen`.
```
rosshow -c1 <topicname>
rosshow -c4 <topicname>
rosshow -c24 <topicname>
```

# Screenshots

## sensor_msgs/PointCloud2

You can rotate and tilt with the arrow keys, and zoom with the +/- keys.
This has been tested with Velodyne data. PointClouds from devices that don't have "x", "y", and "z" fields are not supported.

![screenshot](/screenshots/screenshot5.png?raw=true "screenshot")

## sensor_msgs/Image, sensor_msgs/CompressedImage

![screenshot](/screenshots/screenshot4.png?raw=true "screenshot")

## sensor_msgs/LaserScan

You can zoom with the +/- keys.

![screenshot](/screenshots/screenshot0.png?raw=true "screenshot")

## sensor_msgs/Imu

![screenshot](/screenshots/screenshot2.png?raw=true "screenshot")

## sensor_msgs/NavSatFix

The NavSatFix visualization fetches map tiles from OpenStreetMaps, so your machine or robot needs to have internet access to be able to view those. Otherwise, you'll still be able to see a trace of points.

![screenshot](/screenshots/screenshot3.png?raw=true "screenshot")

The ASCII-only "-a" option works for all types. Here's what the NavSatFix message looks like on pure ASCII:

![screenshot](/screenshots/screenshot3-ascii.png?raw=true "screenshot")

## std_msgs/Int32, std_msgs/Float32, etc.

For most std_msgs numeric types you will get a time series plot.

![screenshot](/screenshots/screenshot6.png?raw=true "screenshot")

Neat trick: You can reduce your terminal font size to get slightly higher resolution. Here's a nav\_msgs/OccupancyGrid:
![screenshot](/screenshots/screenshot7.png?raw=true "screenshot")

# Full list of supported types

### nav_msgs
* nav_msgs/OccupancyGrid
* nav_msgs/Odometry
* nav_msgs/Path

### std_msgs
* std_msgs/Bool
* std_msgs/Float32
* std_msgs/Float64
* std_msgs/Int8
* std_msgs/Int16
* std_msgs/Int32
* std_msgs/Int64
* std_msgs/UInt8
* std_msgs/UInt16
* std_msgs/UInt32
* std_msgs/UInt64

### sensor_msgs
* sensor_msgs/CompressedImage
* sensor_msgs/FluidPressure
* sensor_msgs/Illuminance
* sensor_msgs/Image
* sensor_msgs/Imu
* sensor_msgs/LaserScan
* sensor_msgs/NavSatFix
* sensor_msgs/PointCloud2
* sensor_msgs/Range
* sensor_msgs/RelativeHumidity
* sensor_msgs/Temperature
