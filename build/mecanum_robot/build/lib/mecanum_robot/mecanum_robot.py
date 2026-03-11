# This program subscribes to a topic that carries a Twist message 
# It then sends out serial data to the motor drivers via serial

# Yaboom motor library
from Rosmaster_Lib import Rosmaster

import rclpy
from rclpy.node import Node
import math
from rclpy.qos import QoSProfile
from geometry_msgs.msg import Quaternion
from sensor_msgs.msg import JointState
from tf2_ros import TransformBroadcaster, TransformStamped
from nav_msgs.msg import Odometry

# I don't know what this does, do I need it?
# https://docs.ros.org/en/humble/Concepts/Intermediate/About-Quality-of-Service-Settings.html
#from rclpy.qos import qos_profile_default

# Twist is a message for position and vector
from geometry_msgs.msg import Twist


# Create an instance of our yaboom motor
# Note that the usb device may change from 0 to another number todo: add an assert
rm = Rosmaster(com="/dev/ttyCH341USB0", debug=True)

class MecanumRobot(Node):
    def __init__(self):
        # Name of the node
        super().__init__('mecanum_robot')
        rm.create_receive_threading()               # Enable rm to control the robot

        self.odom_pub = self.create_publisher(Odometry, 'odom', 10)
        self.tf_broadcaster = TransformBroadcaster(self)

        self.subscription = self.create_subscription(
            Twist,                                      # This is the datatype of the message
            'cmd_vel',                                  # This is the name of the topic we're subscribing to
            self.driveMotors,
            10                                          # What does the 10 do
        )
        self.get_logger().info("Started mecanum driver")

        self.x = 0.0
        self.y = 0.0
        self.theta = 0.0

        self.last_encoders = None

        self.wheel_radius = 0.04
        self.ticks_per_rev = 2464
        self.L = 0.18
        self.W = 0.15

        self.last_time = self.get_clock().now()



    def driveMotors(self, msg):
        # Note that we ignore msg.angular.x and msg.angular.y since our robot can only rotate around zhat
        # Angular momentum calculations msg.angular.z * (1/2 l + 1/2 h). Let's ignore for now to see what happens
        # That is 1/2 22cm + 1/2 21cm =  21.5 cm or 0.215m
        # The motors turn at 3 rpm at a value of 100 so desired_rpm * (100/3) = motor_value
        # value =  1250/3pi * speed in m/s       

        # Front left
        MotorFL = 20 * (msg.linear.x - msg.linear.y - msg.angular.z)
        # Front right
        MotorFR = 20 * (msg.linear.x + msg.linear.y + msg.angular.z)
        # Back left
        MotorBL = 20 * (msg.linear.x + msg.linear.y - msg.angular.z)
        # Back right
        MotorBR = 20 * (msg.linear.x - msg.linear.y + msg.angular.z)

        # Now drive the motors at this velocity
        rm.set_motor(-MotorFR, MotorFL, -MotorBL, MotorBR)

        # Log our messages
        self.get_logger().info(f"Front Left motor: {MotorFL}, Front Right motor: {MotorFR}, Back Left motor: {MotorBL}, Back Right motor: {MotorBR}")
        
        # Update odom
        now = self.get_clock().now()
        wheel_encoder_touple = rm.get_motor_encoder()

        dt = max((now - self.last_time).nanoseconds * 1e-9, 1e-6)
        self.last_time = now

        if self.last_encoders is None:
            self.last_encoders = wheel_encoder_touple
            return

        # Got this code from canon, may need to rewrite it to match my robot's wheel arrangement/direction        
        dFL = wheel_encoder_touple[1] - self.last_encoders[1]
        dFR = wheel_encoder_touple[0] - self.last_encoders[0]
        dBL = wheel_encoder_touple[2] - self.last_encoders[2]
        dBR = wheel_encoder_touple[3] - self.last_encoders[3]

        # Update state
        self.last_encoders = wheel_encoder_touple
        
        # Might need these vals from canon
        tpr = self.ticks_per_rev
        r = self.wheel_radius
        
        wFL = (dFL / tpr) * 2 * math.pi / dt
        wFR = (dFR / tpr) * 2 * math.pi / dt
        wBL = (dBL / tpr) * 2 * math.pi / dt
        wBR = (dBR / tpr) * 2 * math.pi / dt

        # Again, depends on how our code differs. may need to change this
        vx = (r / 4) * -(wFL + wFR + wBL + wBR)
        vy = (r / 4) * -(-wFL + wFR + wBL - wBR)
        omega = (r / (4 * (self.L + self.W))) * (-wFL + wFR - wBL + wBR)

        self.x += (vx * math.cos(self.theta) - vy * math.sin(self.theta)) * dt
        self.y += (vx * math.sin(self.theta) + vy * math.cos(self.theta)) * dt
        self.theta += omega * dt

        # wrap angle
        self.theta = (self.theta + math.pi) % (2 * math.pi) - math.pi

        odom = Odometry()

        odom.header.stamp = now.to_msg()
        odom.header.frame_id = "odom"
        odom.child_frame_id = "base_link"

        odom.pose.pose.position.x = self.x
        odom.pose.pose.position.y = self.y

        odom.pose.pose.orientation.z = math.sin(self.theta / 2.0)
        odom.pose.pose.orientation.w = math.cos(self.theta / 2.0)

        # covariance (important for mappers)
        odom.pose.covariance[0] = 0.01
        odom.pose.covariance[7] = 0.01
        odom.pose.covariance[35] = 0.05

        odom.twist.twist.linear.x = vx
        odom.twist.twist.linear.y = vy
        odom.twist.twist.angular.z = omega

        self.odom_pub.publish(odom)

        t = TransformStamped()

        t.header.stamp = now.to_msg()
        t.header.frame_id = "odom"
        t.child_frame_id = "base_link"

        t.transform.translation.x = self.x
        t.transform.translation.y = self.y
        t.transform.translation.z = 0.0

        t.transform.rotation.z = math.sin(self.theta / 2.0)
        t.transform.rotation.w = math.cos(self.theta / 2.0)

        self.tf_broadcaster.sendTransform(t)



def main(args=None):
    rclpy.init(args=args)

    # Create a node of our class
    mecanum_robot = MecanumRobot()

    print("hello!")

    # Keep our node running
    rclpy.spin(mecanum_robot)

    # Destroy the node
    mecanum_robot.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
