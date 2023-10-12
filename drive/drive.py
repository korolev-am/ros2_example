import rclpy
import math
import time
from rclpy.node import Node

from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan
from rclpy.qos import qos_profile_sensor_data


class Drive(Node):

    distance = 0.3
    critical_distanse = 0.2

    def __init__(self):
        super().__init__('drive')
        self.publisher_ = self.create_publisher(Twist, 'cmd_vel', 1)
        self.timer_period = 0.25  # seconds
        self.timer = self.create_timer(self.timer_period, self.timer_callback)
        self.subscription = self.create_subscription(
            LaserScan,
            'scan',
            self.listener_callback,
            qos_profile_sensor_data)
        self.subscription  # prevent unused variable warning
        self.scan_msg = LaserScan()

        self.dist = -1
        self.er = 0
        self.status = "init1"
        self.get_logger().info(self.status)
        self.speed = 0.03
        self.spin_cnt = 0
        self.max_dist = {"dist" : -1, "cnt": -1}
        self.coef = 10


    def listener_callback(self, msg):
        self.scan_msg = msg


    def timer_callback(self):

        if self.status == "emergency stop!":
            return


        #==================================CORRECTION=======================================#


        else:
            stop_turning = False
            if self.status == "turning":
                msg = Twist()
                msg.linear.x = self.speed
                msg.angular.z = 0.0
                self.status = "going straight"
                self.get_logger().info(self.status)
                stop_turning = True
            
            if self.scan_msg.ranges :
                self.get_logger().info('I heard: "%s"' % min(list(set([val for val in self.scan_msg.ranges if val != math.inf]))))
                self.dist = min([val for val in self.scan_msg.ranges if val != math.inf])
                if not self.check_distance(): return
            else:
                self.get_logger().info('Nothing around me')
                return

            er = self.distance - self.dist
            if abs(self.er) < abs(er):
                msg = Twist()
                msg.linear.x = self.speed
                msg.angular.z = er * self.coef
                self.status = "turning"
                self.get_logger().info(self.status)
                self.publisher_.publish(msg)
                stop_turning = False

            if stop_turning:
                self.publisher_.publish(msg)

            self.er = er

    def check_distance(self):
        if self.dist <= self.critical_distanse:
            msg = Twist()
            msg.linear.x = 0.0
            msg.angular.z = 0.0
            self.status = "emergency stop!"
            self.get_logger().info(self.status)
            self.publisher_.publish(msg)
            return False
        return True

    def emergency_stop(self):
        msg = Twist()
        msg.linear.x = 0.0
        msg.angular.z = 0.0
        self.status = "emergency stop!"
        self.get_logger().info(self.status)
        self.publisher_.publish(msg)


def main(args=None):

    print('Hi')
    rclpy.init(args=args)
    drive = Drive()

    rclpy.spin(drive)

    drive.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
