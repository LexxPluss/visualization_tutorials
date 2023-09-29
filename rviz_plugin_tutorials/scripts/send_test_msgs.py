#!/usr/bin/env python3

import roslib
roslib.load_manifest( 'rviz_plugin_tutorials' )
from sensor_msgs.msg import Imu
import rospy
from math import cos, sin
from transforms3d.euler import euler2quat
from tf2_ros.transform_broadcaster import TransformBroadcaster
from geometry_msgs.msg import (
    Quaternion,
    Transform,
    TransformStamped,
    Vector3
)
from std_msgs.msg import Header

topic = 'test_imu'
publisher = rospy.Publisher( topic, Imu, queue_size=5 )

rospy.init_node( 'test_imu' )

br = TransformBroadcaster()
rate = rospy.Rate(10)
radius = 5
angle = 0

dist = 3
while not rospy.is_shutdown():

    imu = Imu()
    imu.header.frame_id = "/base_link"
    imu.header.stamp = rospy.Time.now()
   
    imu.linear_acceleration.x = sin( 10 * angle )
    imu.linear_acceleration.y = sin( 20 * angle )
    imu.linear_acceleration.z = sin( 40 * angle )

    publisher.publish( imu )

    quat = euler2quat(0, 0, angle)
    t_stamped = TransformStamped(
        Header(stamp=rospy.Time.now(), frame_id="map"),
        "base_link",
        Transform(
            Vector3(radius * cos(angle), radius * sin(angle), 0),
            Quaternion(quat[1], quat[2], quat[3], quat[0])
        )
    )
    br.sendTransform(t_stamped)
    angle += .01
    rate.sleep()

