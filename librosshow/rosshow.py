# This file should be written to be both python2 and python3 compatible

import os

try:
    import rospy # ROS1
except ImportError:
    import librosshow.rospy2 as rospy # ROS2, run as module
except ModuleNotFoundError as e:
    print(str(e))
    exit(1)

import sys
import time
import random
import threading
from librosshow.getch import Getch
import librosshow.termgraphics as termgraphics

VIEWER_MAPPING = {

  "nav_msgs/Odometry": ("librosshow.viewers.nav_msgs.OdometryViewer", "OdometryViewer", {}),
  "nav_msgs/OccupancyGrid": ("librosshow.viewers.nav_msgs.OccupancyGridViewer", "OccupancyGridViewer", {}),
  "nav_msgs/Path": ("librosshow.viewers.nav_msgs.PathViewer", "PathViewer", {}),
  "std_msgs/Bool": ("librosshow.viewers.generic.SinglePlotViewer", "SinglePlotViewer", {}),
  "std_msgs/Float32": ("librosshow.viewers.generic.SinglePlotViewer", "SinglePlotViewer", {}),
  "std_msgs/Float64": ("librosshow.viewers.generic.SinglePlotViewer", "SinglePlotViewer", {}),
  "std_msgs/Int8": ("librosshow.viewers.generic.SinglePlotViewer", "SinglePlotViewer", {}),
  "std_msgs/Int16": ("librosshow.viewers.generic.SinglePlotViewer", "SinglePlotViewer", {}),
  "std_msgs/Int32": ("librosshow.viewers.generic.SinglePlotViewer", "SinglePlotViewer", {}),
  "std_msgs/Int64": ("librosshow.viewers.generic.SinglePlotViewer", "SinglePlotViewer", {}),
  "std_msgs/UInt8": ("librosshow.viewers.generic.SinglePlotViewer", "SinglePlotViewer", {}),
  "std_msgs/UInt16": ("librosshow.viewers.generic.SinglePlotViewer", "SinglePlotViewer", {}),
  "std_msgs/UInt32": ("librosshow.viewers.generic.SinglePlotViewer", "SinglePlotViewer", {}),
  "std_msgs/UInt64": ("librosshow.viewers.generic.SinglePlotViewer", "SinglePlotViewer", {}),
  "sensor_msgs/CompressedImage": ("librosshow.viewers.sensor_msgs.CompressedImageViewer", "CompressedImageViewer", {}),
  "sensor_msgs/FluidPressure": ("librosshow.viewers.generic.SinglePlotViewer", "SinglePlotViewer", {"data_field": "fluid_pressure"}),
  "sensor_msgs/RelativeHumidity": ("librosshow.viewers.generic.SinglePlotViewer", "SinglePlotViewer", {"data_field": "relative_humidity"}),
  "sensor_msgs/Illuminance": ("librosshow.viewers.generic.SinglePlotViewer", "SinglePlotViewer", {"data_field": "illuminance"}),
  "sensor_msgs/Image": ("librosshow.viewers.sensor_msgs.ImageViewer", "ImageViewer", {}),
  "sensor_msgs/Imu": ("librosshow.viewers.sensor_msgs.ImuViewer", "ImuViewer", {}),
  "sensor_msgs/LaserScan": ("librosshow.viewers.sensor_msgs.LaserScanViewer", "LaserScanViewer", {}),
  "sensor_msgs/NavSatFix": ("librosshow.viewers.sensor_msgs.NavSatFixViewer", "NavSatFixViewer", {}),
  "sensor_msgs/PointCloud2": ("librosshow.viewers.sensor_msgs.PointCloud2Viewer", "PointCloud2Viewer", {}),
  "sensor_msgs/Range": ("librosshow.viewers.generic.SinglePlotViewer", "SinglePlotViewer", {"data_field": "range"}),
  "sensor_msgs/Temperature": ("librosshow.viewers.generic.SinglePlotViewer", "SinglePlotViewer", {"data_field": "temperature"}),
  "geometry_msgs/Twist": ("librosshow.viewers.generic.MultiPlotViewer", "MultiPlotViewer", {"data_fields": ["linear.x", "linear.y", "linear.z", "angular.x", "angular.y", "angular.z"]}),
}

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
        print("Unsupported message type.")
        exit()

    # Create the canvas and viewer accordingly

    canvas = termgraphics.TermGraphics( \
            mode = (termgraphics.MODE_EASCII if USE_ASCII else termgraphics.MODE_UNICODE),
            color_support = color_support)

    module_name, class_name, viewer_kwargs = VIEWER_MAPPING[topic_types[TOPIC]]
    viewer_class = getattr(__import__(module_name, fromlist=(class_name)), class_name)
    viewer = viewer_class(canvas, title = TOPIC, **viewer_kwargs)

    message_package, message_name = topic_types[TOPIC].split("/", 2)
    message_class = getattr(__import__(message_package + ".msg", fromlist=(message_name)), message_name)

    # Subscribe to the topic so the viewer actually gets the data

    rospy.Subscriber(TOPIC, message_class, viewer.update)

    # Listen for keypresses

    getch = Getch()

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
