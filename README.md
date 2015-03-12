youbot_leapmotionteleop
=======================

A ROS package for teleoperating a youBot(or any other holonomic base which is subscribed to the 'cmd_vel' topic.

There are three python scripts in thescripts folder, one each for the base, arm and gripper.

This package builds on http://github.com/warp1337/rosleapmotion

1. roslaunch youbot_driver_ros_interface youbot_driver.launch 
2. rosrun youbot_leap <node_name>.py


Find it on youbot-store community!
http://www.youbot-store.com/detail/index/sArticle/118/sCategory/37


Video:

 https://www.youtube.com/watch?v=Ztvy0X4-qIM&list=UUaZtZjYZYnnL8-3lAkoShdQ

Short Description:

The Leap Motion application is used to remotely control the KUKA youBot via the Leap Motion sensor. You can control the youBot base as well as the youBot arm and gripper. This application builds on the Leap Motion API's ROS wrapper to obtain the hand’s normal, direction, roll-pitch-yaw vectors and position. The vectors are published to the cmd_vel topic to which the youBot driver subscribes.

Installation 

1. If you don't already have a catkin workspace, please follow these instructions before starting with 2.: http://ros.org/wiki/catkin/Tutorials/create_a_workspace  
2. cd ~/catkin_ws/src  
3. git clone https://github.com/madratman/youbot_leapmotionteleop.git
4. cd ~catkin_ws && catkin_make
5. Start a roscore (another shell) and leapd (another shell)
6. You need to append the location of your LeapSDK (especially /lib and /lib/x64 or x86) to your PYTHONPATH, e.g., export PYTHONPATH=$PYTHONPATH:/path/to/SDK/lib:/path/to/SDK/x64. Remember that you will need to have your path set at least in the “sender” shell. If you want to set it every time, you can also alter the leapinterface.py file.
USAGE

Before you start the application, you may want to make a configuration in the code where you can change publish rate (default 20Hz) or speed. The speed can be changed by adjusting the multipliers of geometry_msgs.linear.x/y and geometry_msgs.angular.z.

Keyboard control is also implemented in the code where you can change the controlled joint via keys.

To launch the app:

roslaunch youbot_driver_ros_interface youbot_driver.launch
rosrun youbot_leap node_name.py
