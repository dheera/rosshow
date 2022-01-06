# This file should be written to be both python2 and python3 compatible

import os

try:
    import rospy # ROS1
except ImportError:
    import rosshow.rospy2 as rospy # ROS2
except ModuleNotFoundError as e:
    print(str(e))
    exit(1)

import sys
import time
import random
import threading
from rosshow.getch import Getch
import rosshow.termgraphics as termgraphics

getch = Getch()

VIEWER_MAPPING = {

  # ROS1.
  "nav_msgs/Odometry": ("rosshow.viewers.nav_msgs.OdometryViewer", "OdometryViewer", {}),
  "nav_msgs/OccupancyGrid": ("rosshow.viewers.nav_msgs.OccupancyGridViewer", "OccupancyGridViewer", {}),
  "nav_msgs/Path": ("rosshow.viewers.nav_msgs.PathViewer", "PathViewer", {}),
  "std_msgs/Bool": ("rosshow.viewers.generic.SinglePlotViewer", "SinglePlotViewer", {}),
  "std_msgs/Float32": ("rosshow.viewers.generic.SinglePlotViewer", "SinglePlotViewer", {}),
  "std_msgs/Float64": ("rosshow.viewers.generic.SinglePlotViewer", "SinglePlotViewer", {}),
  "std_msgs/Int8": ("rosshow.viewers.generic.SinglePlotViewer", "SinglePlotViewer", {}),
  "std_msgs/Int16": ("rosshow.viewers.generic.SinglePlotViewer", "SinglePlotViewer", {}),
  "std_msgs/Int32": ("rosshow.viewers.generic.SinglePlotViewer", "SinglePlotViewer", {}),
  "std_msgs/Int64": ("rosshow.viewers.generic.SinglePlotViewer", "SinglePlotViewer", {}),
  "std_msgs/UInt8": ("rosshow.viewers.generic.SinglePlotViewer", "SinglePlotViewer", {}),
  "std_msgs/UInt16": ("rosshow.viewers.generic.SinglePlotViewer", "SinglePlotViewer", {}),
  "std_msgs/UInt32": ("rosshow.viewers.generic.SinglePlotViewer", "SinglePlotViewer", {}),
  "std_msgs/UInt64": ("rosshow.viewers.generic.SinglePlotViewer", "SinglePlotViewer", {}),
  "sensor_msgs/CompressedImage": ("rosshow.viewers.sensor_msgs.CompressedImageViewer", "CompressedImageViewer", {}),
  "sensor_msgs/FluidPressure": ("rosshow.viewers.generic.SinglePlotViewer", "SinglePlotViewer", {"data_field": "fluid_pressure"}),
  "sensor_msgs/RelativeHumidity": ("rosshow.viewers.generic.SinglePlotViewer", "SinglePlotViewer", {"data_field": "relative_humidity"}),
  "sensor_msgs/Illuminance": ("rosshow.viewers.generic.SinglePlotViewer", "SinglePlotViewer", {"data_field": "illuminance"}),
  "sensor_msgs/Image": ("rosshow.viewers.sensor_msgs.ImageViewer", "ImageViewer", {}),
  "sensor_msgs/Imu": ("rosshow.viewers.sensor_msgs.ImuViewer", "ImuViewer", {}),
  "sensor_msgs/LaserScan": ("rosshow.viewers.sensor_msgs.LaserScanViewer", "LaserScanViewer", {}),
  "sensor_msgs/NavSatFix": ("rosshow.viewers.sensor_msgs.NavSatFixViewer", "NavSatFixViewer", {}),
  "sensor_msgs/PointCloud2": ("rosshow.viewers.sensor_msgs.PointCloud2Viewer", "PointCloud2Viewer", {}),
  "sensor_msgs/Range": ("rosshow.viewers.generic.SinglePlotViewer", "SinglePlotViewer", {"data_field": "range"}),
  "sensor_msgs/Temperature": ("rosshow.viewers.generic.SinglePlotViewer", "SinglePlotViewer", {"data_field": "temperature"}),
  "geometry_msgs/Twist": ("rosshow.viewers.generic.MultiPlotViewer", "MultiPlotViewer", {"data_fields": ["linear.x", "linear.y", "linear.z", "angular.x", "angular.y", "angular.z"]}),
}

# ROS2, e.g. nav_msgs/Odometry -> nav_msgs/msg/Odometry.
_viewer_mapping_ros2 = {}
for k, v in VIEWER_MAPPING.items():
    message_package, message_name = k.split("/", 2)
    _viewer_mapping_ros2[f'{message_package}/msg/{message_name}'] = v
VIEWER_MAPPING.update(_viewer_mapping_ros2)


def capture_key_loop(viewer):
    global getch
    while True:
        c = getch()
        if c == '\x03': # Ctrl+C
            rospy.signal_shutdown("Ctrl+C pressed")

        if "keypress" not in dir(viewer):
            continue

        if c == '\x1B': # ANSI escape
            c = getch()
            if c == '\x5B':
                c = getch()
                if c == '\x41':
                    viewer.keypress("up")
                if c == '\x42':
                    viewer.keypress("down")
                if c == '\x43':
                    viewer.keypress("left")
                if c == '\x44':
                    viewer.keypress("right")
        else:
            viewer.keypress(c)

def main():
    # Parse arguments
    # TODO: proper argument parsing
    TOPIC = "-"
    argi = 1
    while TOPIC.startswith("-"):
        if argi >= len(sys.argv):
            print("Usage: rosshow [-a] <topic>")
            print("   -a:   Use ASCII only (no Unicode)")
            print("   -c1:  Force monochrome")
            print("   -c4:  Force 4-bit color (16 colors)")
            print("   -c24: Force 24-bit color")
            sys.exit(0)
        TOPIC = sys.argv[argi]
        argi+= 1

    if ("-a" in sys.argv) or ("--ascii" in sys.argv):
        USE_ASCII = True
    else:
        USE_ASCII = False

    if "-c1" in sys.argv:
        color_support = termgraphics.COLOR_SUPPORT_1
    elif "-c4" in sys.argv:
        color_support = termgraphics.COLOR_SUPPORT_16
    elif "-c24" in sys.argv:
        color_support = termgraphics.COLOR_SUPPORT_24BIT
    else:
        color_support = None # TermGraphics class will autodetect

    rospy.init_node('rosshow', anonymous=True)

    # Get information on all topic types

    topic_types = dict(rospy.get_published_topics())
    if TOPIC not in topic_types:
        print("Topic {0} does not appear to be published yet.".format(TOPIC))
        sys.exit(0)

    if topic_types[TOPIC] not in VIEWER_MAPPING:
        print(f"Unsupported message type '{topic_types[TOPIC]}'.")
        exit()

    # Create the canvas and viewer accordingly

    canvas = termgraphics.TermGraphics( \
            mode = (termgraphics.MODE_EASCII if USE_ASCII else termgraphics.MODE_UNICODE),
            color_support = color_support)

    module_name, class_name, viewer_kwargs = VIEWER_MAPPING[topic_types[TOPIC]]
    viewer_class = getattr(__import__(module_name, fromlist=(class_name)), class_name)
    viewer = viewer_class(canvas, title = TOPIC, **viewer_kwargs)

    try:
        # ROS1.
        message_package, message_name = topic_types[TOPIC].split("/", 2)
    except ValueError:
        # ROS2.
        message_package, _, message_name = topic_types[TOPIC].split("/", 3)

    message_class = getattr(__import__(message_package + ".msg", fromlist=(message_name)), message_name)

    # Subscribe to the topic so the viewer actually gets the data

    rospy.Subscriber(TOPIC, message_class, viewer.update)

    # Listen for keypresses

    thread = threading.Thread(target = capture_key_loop, args = (viewer,))
    thread.daemon = True
    thread.start()

    # Drawing loop
    frame_rate = 15.
    frame_duration = 1. / frame_rate
    try:
        while not rospy.is_shutdown():
            start_time = time.time()
            viewer.draw()
            stop_time = time.time()
            draw_time = stop_time - start_time
            delay_time = max(0, frame_duration - draw_time)
            time.sleep(delay_time)
    except rospy.exceptions.ROSInterruptException:
        sys.stdout.write("")

    finally:
        getch.reset()
        sys.stdout.write("\033[%d;0H\n" % canvas.term_shape[1])
        sys.stdout.flush()

if __name__ == "__main__":
    main()
