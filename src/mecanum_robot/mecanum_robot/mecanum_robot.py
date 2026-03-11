# This program subscribes to a topic that carries a Twist message 
# It then sends out serial data to the motor drivers via serial

# Yaboom motor library
from Rosmaster_Lib import Rosmaster

import rclpy
from rclpy.node import Node

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
        rm.create_receive_threading()                   # Enable rm to control the robot
        self.publisher = self.create_publisher(
            Int32MultiArray,                            # Canon is using this, docs say this is bad idea
            'wheel_encoders',                           # Name of topic
            self.getEncoderVals,
            10)

        self.subscription = self.create_subscription(
            Twist,                                      # This is the datatype of the message
            'cmd_vel',                                  # This is the name of the topic we're subscribing to
            self.driveMotors,
            10                                          # What does the 10 do
        )
        self.get_logger().info("Started mecanum subscriber")

    def GetEncoderVals(self):
        msg = Int32MultiArray
        #msg.data = 

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

        # Front left
#        MotorFL = 20 * (msg.linear.x - msg.linear.y - msg.angular.z)
#        # Front right
#        MotorFR = 20 * (msg.linear.x + msg.linear.y + msg.angular.z)
#        # Back left
#        MotorBL = 20 * (msg.linear.x + msg.linear.y + msg.angular.z)
#        # Back right
#        MotorBR = 20 * (msg.linear.x - msg.linear.y - msg.angular.z)

        # Now drive the motors at this velocity
        rm.set_motor(-MotorFR, MotorFL, -MotorBL, MotorBR)

        # Log our messages
        self.get_logger().info(f"Front Left motor: {MotorFL}, Front Right motor: {MotorFR}, Back Left motor: {MotorBL}, Back Right motor: {MotorBR}")

        # Logging data about the recieved twist. Add more stuff like response time
        #self.get_logger().info('recieved twist: "%s"; % msg.data)

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
