#!/usr/bin/env python
__author__ = 'flier'
import rospy
import roslib
import leap_interface
import brics_actuator.msg
from leap_motion.msg import leap
from leap_motion.msg import leapros
from geometry_msgs.msg import Twist
from brics_actuator.msg import JointPositions, JointValue, Poison
import sys, select, termios, tty, signal


moveBindings = {
        '1':(1),   
        '2':(2),  
        '3':(3),  
        '4':(4),   
        '5':(5),    
           }

# speedBindings={
#         'q':(1.1,1.1),
#         'z':(.9,.9),
#         'w':(1.1,1),
#         'x':(.9,1),
#         'e':(1,1.1),
#         'c':(1,.9),
#           }



class TimeoutException(Exception): 
    pass 

def getKey():
    def timeout_handler(signum, frame):
        raise TimeoutException()
    
    old_handler = signal.signal(signal.SIGALRM, timeout_handler)
    signal.alarm(1) #this is the watchdog timing
    tty.setraw(sys.stdin.fileno())
    select.select([sys.stdin], [], [], 0)
    try:
       key = sys.stdin.read(1)
       #print "Read key"
    except TimeoutException:
       #print "Timeout"
       return "-"
    finally:
       signal.signal(signal.SIGALRM, old_handler)

    signal.alarm(0)
    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
    return key





# # Obviously, this method publishes the data defined in leapros.msg to /leapmotion/data
# def sender():
#     li = leap_interface.Runner()
#     li.setDaemon(True)
#     li.start()
#     # pub     = rospy.Publisher('leapmotion/raw',leap)
#     pub_youbotleaparm = rospy.Publisher('arm_1/arm_controller/position_command', JointPositions)
#     rospy.init_node('leap_youbotarm_pub')
#     r = rospy.Rate(20)

#     speed_x = -0.1
#     speed_y = -0.1

#     count = 0
#     dummy = 0.12
#     while not (rospy.is_shutdown() and count < 10):
#         # hand_direction_   = li.get_hand_direction()
#         hand_normal_      = li.get_hand_normal()
#         # handsecond_normal_ = li.get_handsecond_normal()     
#         # hand_palm_pos_    = li.get_hand_palmpos()
#         # hand_pitch_       = li.get_hand_pitch()
#         # hand_roll_        = li.get_hand_roll()
#         # hand_yaw_         = li.get_hand_yaw()
#         # msg = leapros()     
#         # msg.direction.y = hand_direction_[1]
#         # msg.direction.z = hand_direction_[2]
#         # msg.normal.x = hand_normal_[0]
#         # msg.normal.y = hand_normal_[1]
#         # msg.normal.z = hand_normal_[2]
#         # msg.palmpos.x = hand_palm_pos_[0]
#         # msg.palmpos.y = hand_palm_pos_[1]
#         # msg.palmpos.z = hand_palm_pos_[2]
#         # msg.ypr.x = hand_yaw_
#         # msg.ypr.y = hand_pitch_
#         # msg.ypr.z = hand_roll_
#         # We don't publish native data types, see ROS best practices
#         # pub.publish(hand_direction=hand_direction_,hand_normal = hand_normal_, hand_palm_pos = hand_palm_pos_, hand_pitch = hand_pitch_, hand_roll = hand_roll_, hand_yaw = hand_yaw_)
#         #pub_ros.publish(msg)
#         # Save some CPU time, circa 100Hz publishing.

#         # twist = Twist()
#         # twist.linear.x = 0 #-1 * hand_normal_[0] / 10
#         # twist.linear.y = 0 #hand_normal_[2] / 10
#         # twist.linear.z = 0
#         # twist.angular.x = 0     
#         # twist.angular.y = 0
#         # twist.angular.z = hand_pitch_ / 720 #hand_yaw_/1000
#         # pub_youbotleap.publish(twist)
        
#         joint_pos = JointPositions()
        
#         joint_number = 0

#         key = getKey()
#         if key in moveBindings.keys():
#             joint_number = moveBindings[key]

#         print joint_number 

#         default_joint_one = 0.0100692
#         default_joint_two = 0.0100692
#         default_joint_three = -5.02655
#         default_joint_four = 0.0221239
#         default_joint_five = 0.110619
    
#         joint_val_1 = JointValue()
#         joint_val_2 = JointValue()
#         joint_val_3 = JointValue()
#         joint_val_4 = JointValue()
#         joint_val_5 = JointValue()

#         # joint_val_1.value = default_joint_one
#         # joint_val_2.value = default_joint_two
#         # joint_val_3.value = default_joint_three
#         # joint_val_4.value = default_joint_four
#         # joint_val_5.value = default_joint_five
        
#         # joint_val_1.value = default_joint_one
#         # joint_val_2.value = default_joint_two
#         # joint_val_3.value = default_joint_three
#         # joint_val_4.value = 1.5 #default_joint_four
#         # joint_val_5.value = default_joint_five
        

#         joint_val_1.joint_uri = "arm_joint_1"
#         joint_val_1.unit = "rad"
#         joint_val_2.joint_uri = "arm_joint_2"
#         joint_val_2.unit = "rad"
#         joint_val_3.joint_uri = "arm_joint_3"
#         joint_val_3.unit = "rad"
#         joint_val_4.joint_uri = "arm_joint_4"
#         joint_val_4.unit = "rad"
#         joint_val_5.joint_uri = "arm_joint_5"
#         joint_val_5.unit = "rad"

#         if joint_number == 1:
#             joint_val_1 = JointValue()
#             joint_val_1.joint_uri = "arm_joint_1"
#             joint_val_1.unit = "rad"
#             default_joint_one = 0.0100692
#             joint_val_1.value = (((hand_normal_[0] /2) + 0.5) * (5.84014 - 0.0100692) ) + 0.0100692
#             count = count + 1
#             # rospy.spin()

#         elif joint_number == 2:
#             joint_val_2 = JointValue()
#             joint_val_2.joint_uri = "arm_joint_2"
#             joint_val_2.unit = "rad"
#             default_joint_two = 0.0100692
#             joint_val_2.value = (((hand_normal_[0] /2) + 0.5) * (2.61799 - 0.0100692) ) + 0.0100692 
#             count = count + 1
#             # rospy.spin() 

#         elif joint_number == 3:
#             joint_val_3 = JointValue()
#             joint_val_3.joint_uri = "arm_joint_3"
#             joint_val_3.unit = "rad"
#             default_joint_three = -5.02655
#             joint_val_3.value = (((hand_normal_[0] /2) + 0.5) * (5.02655 - 0.015708) ) - 5.02655
#             count = count + 1
            
#         elif joint_number == 4:          
#             joint_val_4 = JointValue()
#             joint_val_4.joint_uri = "arm_joint_4"
#             joint_val_4.unit = "rad"
#             default_joint_four = 0.0221239
#             joint_val_4.value = (((hand_normal_[0] /2) + 0.5) * (3.4292  - 0.0221239) ) + 0.0221239 
#             count = count + 1
               
#         elif joint_number == 5:
#             joint_val_5 = JointValue()
#             joint_val_5.joint_uri = "arm_joint_5"
#             joint_val_5.unit = "rad"
#             default_joint_five = 0.110619
#             joint_val_5.value = default_joint_five + (count/10)
#             joint_val_5.value = (((hand_normal_[0] /2) + 0.5) * (5.64159 - 0.110619) ) + 0.110619 
#             count = count + 1

#         # print "joint_val_5: %f " % (joint_val_5.value)
#         # print hand_normal_[0]


#  # joint arm_joint_1 valid range is between 0.0100692 and 5.84014 
#  # joint arm_joint_2 valid range is between 0.0100692 and 2.61799 
#  # joint arm_joint_3 valid range is between -5.02655 and -0.015708
#  # joint arm_joint_4 valid range is between 0.0221239 and 3.4292 
#  # joint arm_joint_5 valid range is between 0.110619 and 5.64159 
 
#         # joint_val_1.value = (((hand_normal_[0] /2) + 0.5) * (5.84014 - 0.0100692) ) + 0.0100692

#         # joint_val_2.value = (((hand_normal_[0] /2) + 0.5) * (2.61799 - 0.0100692) ) + 0.0100692 

#         # joint_val_3.value = (((hand_normal_[0] /2) + 0.5) * (5.02655 - 0.015708) ) - 5.02655

#         # joint_val_4.value = (((hand_normal_[0] /2) + 0.5) * (3.4292  - 0.0221239) ) + 0.0221239 

#         # joint_val_5.value = (((hand_normal_[0] /2) + 0.5) * (5.64159 - 0.110619) ) + 0.110619 

#         poison = Poison()

#         joint_pos.poisonStamp = poison

#         joint_pos.positions = [joint_val_1, joint_val_2, joint_val_3, joint_val_4, joint_val_5]

#         pub_youbotleaparm.publish(joint_pos)

#         # print "x_vel: %f m/s, y_vel: %f m/s, ang_vel: %f m/s" % (twist.linear.x , twist.linear.y , twist.angular.z  )
#         # print "pitch: %f m/s, yaw: %f m/s, roll: %f m/s" % (hand_pitch_ , hand_yaw_ , hand_roll_)
#         r.sleep()

if __name__ == '__main__':
    settings = termios.tcgetattr(sys.stdin)

    li = leap_interface.Runner()
    li.setDaemon(True)
    li.start()
    # pub     = rospy.Publisher('leapmotion/raw',leap)
    pub_youbotleaparm = rospy.Publisher('arm_1/arm_controller/position_command', JointPositions)
    rospy.init_node('leap_youbotarm_pub')
    # r = rospy.Rate(20)

    speed_x = -0.1
    speed_y = -0.1

    count = 0
    dummy = 0.12
    while not (rospy.is_shutdown() and count < 10):
        # hand_direction_   = li.get_hand_direction()
        hand_normal_      = li.get_hand_normal()
        # handsecond_normal_ = li.get_handsecond_normal()     
        # hand_palm_pos_    = li.get_hand_palmpos()
        # hand_pitch_       = li.get_hand_pitch()
        # hand_roll_        = li.get_hand_roll()
        # hand_yaw_         = li.get_hand_yaw()
        # msg = leapros()     
        # msg.direction.y = hand_direction_[1]
        # msg.direction.z = hand_direction_[2]
        # msg.normal.x = hand_normal_[0]
        # msg.normal.y = hand_normal_[1]
        # msg.normal.z = hand_normal_[2]
        # msg.palmpos.x = hand_palm_pos_[0]
        # msg.palmpos.y = hand_palm_pos_[1]
        # msg.palmpos.z = hand_palm_pos_[2]
        # msg.ypr.x = hand_yaw_
        # msg.ypr.y = hand_pitch_
        # msg.ypr.z = hand_roll_
        # We don't publish native data types, see ROS best practices
        # pub.publish(hand_direction=hand_direction_,hand_normal = hand_normal_, hand_palm_pos = hand_palm_pos_, hand_pitch = hand_pitch_, hand_roll = hand_roll_, hand_yaw = hand_yaw_)
        #pub_ros.publish(msg)
        # Save some CPU time, circa 100Hz publishing.
        
        joint_pos = JointPositions()
        joint_number = 0

        key = getKey()
        if key in moveBindings.keys():
            joint_number = moveBindings[key]

        print joint_number 

        default_joint_one = 0.0100692
        default_joint_two = 0.0100692
        default_joint_three = -5.02655
        default_joint_four = 0.0221239
        default_joint_five = 0.110619
    
        joint_val_1 = JointValue()
        joint_val_2 = JointValue()
        joint_val_3 = JointValue()
        joint_val_4 = JointValue()
        joint_val_5 = JointValue()

        # joint_val_1.value = default_joint_one
        # joint_val_2.value = default_joint_two
        # joint_val_3.value = default_joint_three
        # joint_val_4.value = default_joint_four
        # joint_val_5.value = default_joint_five
        
        # joint_val_1.value = default_joint_one
        # joint_val_2.value = default_joint_two
        # joint_val_3.value = default_joint_three
        # joint_val_4.value = 1.5 #default_joint_four
        # joint_val_5.value = default_joint_five
        

        joint_val_1.joint_uri = "arm_joint_1"
        joint_val_1.unit = "rad"
        joint_val_2.joint_uri = "arm_joint_2"
        joint_val_2.unit = "rad"
        joint_val_3.joint_uri = "arm_joint_3"
        joint_val_3.unit = "rad"
        joint_val_4.joint_uri = "arm_joint_4"
        joint_val_4.unit = "rad"
        joint_val_5.joint_uri = "arm_joint_5"
        joint_val_5.unit = "rad"

        if joint_number == 1:
            joint_val_1 = JointValue()
            joint_val_1.joint_uri = "arm_joint_1"
            joint_val_1.unit = "rad"
            default_joint_one = 0.0100692
            joint_val_1.value = (((hand_normal_[0] /2) + 0.5) * (5.84014 - 0.0100692) ) + 0.0100692
            count = count + 1
            # rospy.spin()

        elif joint_number == 2:
            joint_val_2 = JointValue()
            joint_val_2.joint_uri = "arm_joint_2"
            joint_val_2.unit = "rad"
            default_joint_two = 0.0100692
            joint_val_2.value = (((hand_normal_[0] /2) + 0.5) * (2.61799 - 0.0100692) ) + 0.0100692 
            count = count + 1
            # rospy.spin() 

        elif joint_number == 3:
            joint_val_3 = JointValue()
            joint_val_3.joint_uri = "arm_joint_3"
            joint_val_3.unit = "rad"
            default_joint_three = -5.02655
            joint_val_3.value = (((hand_normal_[0] /2) + 0.5) * (5.02655 - 0.015708) ) - 5.02655
            count = count + 1
            
        elif joint_number == 4:          
            joint_val_4 = JointValue()
            joint_val_4.joint_uri = "arm_joint_4"
            joint_val_4.unit = "rad"
            default_joint_four = 0.0221239
            joint_val_4.value = (((hand_normal_[0] /2) + 0.5) * (3.4292  - 0.0221239) ) + 0.0221239 
            count = count + 1
               
        elif joint_number == 5:
            joint_val_5 = JointValue()
            joint_val_5.joint_uri = "arm_joint_5"
            joint_val_5.unit = "rad"
            default_joint_five = 0.110619
            joint_val_5.value = default_joint_five + (count/10)
            joint_val_5.value = (((hand_normal_[0] /2) + 0.5) * (5.64159 - 0.110619) ) + 0.110619 
            count = count + 1

      


        # print "joint_val_5: %f " % (joint_val_5.value)
        # print hand_normal_[0]


 # joint arm_joint_1 valid range is between 0.0100692 and 5.84014 
 # joint arm_joint_2 valid range is between 0.0100692 and 2.61799 
 # joint arm_joint_3 valid range is between -5.02655 and -0.015708
 # joint arm_joint_4 valid range is between 0.0221239 and 3.4292 
 # joint arm_joint_5 valid range is between 0.110619 and 5.64159 
 
        # joint_val_1.value = (((hand_normal_[0] /2) + 0.5) * (5.84014 - 0.0100692) ) + 0.0100692

        # joint_val_2.value = (((hand_normal_[0] /2) + 0.5) * (2.61799 - 0.0100692) ) + 0.0100692 

        # joint_val_3.value = (((hand_normal_[0] /2) + 0.5) * (5.02655 - 0.015708) ) - 5.02655

        # joint_val_4.value = (((hand_normal_[0] /2) + 0.5) * (3.4292  - 0.0221239) ) + 0.0221239 

        # joint_val_5.value = (((hand_normal_[0] /2) + 0.5) * (5.64159 - 0.110619) ) + 0.110619 

        poison = Poison()

        joint_pos.poisonStamp = poison

        joint_pos.positions = [joint_val_1, joint_val_2, joint_val_3, joint_val_4, joint_val_5]

        pub_youbotleaparm.publish(joint_pos)

        # print "x_vel: %f m/s, y_vel: %f m/s, ang_vel: %f m/s" % (twist.linear.x , twist.linear.y , twist.angular.z  )
        # print "pitch: %f m/s, yaw: %f m/s, roll: %f m/s" % (hand_pitch_ , hand_yaw_ , hand_roll_)
        # r.sleep()
    # try:
    #     sender()
    # except rospy.ROSInterruptException:
    #     pass

    # termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
