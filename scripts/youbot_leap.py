#!/usr/bin/env python
__author__ = 'flier'
import rospy
import leap_interface
from leap_motion.msg import leap
from leap_motion.msg import leapros
from geometry_msgs.msg import Twist

# Obviously, this method publishes the data defined in leapros.msg to /leapmotion/data
def sender():
    li = leap_interface.Runner()
    li.setDaemon(True)
    li.start()
    # pub     = rospy.Publisher('leapmotion/raw',leap)
    pub_youbotleap = rospy.Publisher('cmd_vel', Twist)
    rospy.init_node('leap_youbot_pub')

    rate = rospy.Rate(10)


    speed_x = -0.1
    speed_y = -0.1

    

    # radius = 0

    while not rospy.is_shutdown():
        hand_direction_   = li.get_hand_direction()
        hand_normal_      = li.get_hand_normal()
        hand_palm_pos_    = li.get_hand_palmpos()
        hand_pitch_       = li.get_hand_pitch()
        hand_roll_        = li.get_hand_roll()
        hand_yaw_         = li.get_hand_yaw()
        msg = leapros() 
        msg.direction.x = hand_direction_[0]    
        msg.direction.y = hand_direction_[1]
        msg.direction.z = hand_direction_[2]
        # msg.normal.x = hand_normal_[0]
        # msg.normal.y = hand_normal_[1]
        # msg.normal.z = hand_normal_[2]
        msg.palmpos.x = hand_palm_pos_[0]
        msg.palmpos.y = hand_palm_pos_[1]
        msg.palmpos.z = hand_palm_pos_[2]
        msg.ypr.x = hand_yaw_
        msg.ypr.y = hand_pitch_
        msg.ypr.z = hand_roll_

        # handsecond_normal_ = li.get_handsecond_normal()

        # hand_keytapdirection_ = li.get_keytapdirection()
        # # if hand_keytapdirection_:
        # print hand_keytapdirection_[0]

        # hand_keytapdirection_ = 0
        # print hand_keytapdirection_

        # We don't publish native data types, see ROS best practices
        # pub.publish(hand_direction=hand_direction_,hand_normal = hand_normal_, hand_palm_pos = hand_palm_pos_, hand_pitch = hand_pitch_, hand_roll = hand_roll_, hand_yaw = hand_yaw_)
        #pub_ros.publish(msg)
        # Save some CPU time, circa 100Hz publishing.
        # radius = int(li.get_circle())
        # print radius

        # if radius != 0:
        #     twist.linear.x = 0
        #     twist.linear.y = 0
            
        twist = Twist()
        twist.linear.x = -1 * (hand_normal_[0] / 10 ) #+ ( handsecond_normal_[0] / 10)
        twist.linear.y = ( hand_normal_[2] / 10 ) #(-1 * handsecond_normal_[2] / 10)
        twist.linear.z = 0
        twist.angular.x = 0     
        twist.angular.y = 0
        twist.angular.z = (-1 * handsecond_normal_[0] / 5 )#+ (hand_direction_[2] / 5)
        print "xvel", twist.linear.x, "yvel", twist.linear.y, "angvel", twist.angular.z
        pub_youbotleap.publish(twist)
        rate.sleep()

     

if __name__ == '__main__':
    try:
        sender()
    except rospy.ROSInterruptException:
        pass
