# MRS Security in ROS

Welcome to the MRS_security repository by the C5I center at George Mason.

The C5I center at GMU has partnered with the National Science Foundation to research Robot Operating System security on Multi Robotic Systems.  
This repository is our collection of past and present research and will continue to be updated with continued experimentation.  
Our goal of this repository is to enable the reproduction of our research so that others can learn from and build off the work done by the students in the C5I center.

## Hardware/Software Requirements

- 2 or more TurtleBot3 Burger Robots (each with a Pi 3B+ running ROS Kinetic)

- Ubuntu 16.04 machine (ROS server)

- Ubuntu 20.04 machine (Attacker)  

- Python 2/3

## Environment Setup

Follow the quick start setup guide on the Robotis e-manual website https://emanual.robotis.com/docs/en/platform/turtlebot3/quick-start/.

This guide includes instructions to install ROS Kinetic on both the Turtlebot3 and your Ubuntu 16.04 machine.  
After the setup is complete, verify by running the Teleoperation command in section 3.6.1.1 Keyboard under the Basic Operation section.  
<br />
*** **make sure you keep track of each robot ip_address' and your ROS server ip_address and they are setup properly in the ~/.bashrc files according to the setup guide (don't forget to source the ~/.bashrc file after modifications).  
If this is not properly setup, you will not be able to connect to the robots** ***  

On your Ubuntu 20.04 machine, install the graphical version of Ettercap.
```
[user@attacker-machine]$ sudo apt install ettercap-graphical
```

## Repository Installation

After ROS installation on each robot and the computer, install our github repository in the home directory of the Turtlebot3 robots.
```
[pi@pi-host]$ cd ~/
[pi@pi-host]$ git clone https://github.com/SPIRE-GMU/MRS_Security.git
```

## MRS Startup

Before starting up the MRS, make sure both computers and the robots are on the same network (this network does not need to be connected to the internet).  

On your ROS host machine, startup roscore.
```
[user@ROS-host]$ roscore
```

Open new terminal sessions and SSH into each robot and run bringup commands.
```
[pi@pi-host]$ ssh pi@IP_IP_ADDRESS
# password: turtlebot

[pi@pi-host]$ roslaunch turtlebot3_bringup turtlebot3_robot.launch
```

On the host machine, open a new terminal and start the MRS using the modified teleop command.  
This will connect the leader robot in the MRS to the host machine.
```
[user@ROS-host]$ ROS_NAMESPACE=tb3_0 roslaunch turtlebot3_teloep turtlebot_teleop_key.launch
```

In order to connect the remaining robots to the MRS, open new terminals and SSH into the remaining listener robots and run the follow command.
```
[pi@pi-host]$  rosrun mrs_package mrs_teleop.py
```

Now you should be able to move the MRS using the ASDWX keys on your host machine.

## ARP Posioning Exploit

To exploit the MRS using ARP poisoning first startup Ettercap on the attacker machine.
```
[user@attacker-machine]$ sudo ettercap -G
```

Enable sniffing at startup and choose a primary interface. Then, click the box with the checkmark.  

Navigate to hosts and choose `scan for hosts`. Once Ettercap is done scanning, go to host list. Right click on the listener machine you want to attack and click `Add to Target 1`.  

Finally, go to `Current targets` to confirm the host you want to exploit has been added to the targets list. Then, click on the globe button and click `ARP poisoning` with the `sniff remote connections` option enabled.

If done correctly, the robot you have attacked should no longer be connected to the MRS and it should no longer recieve teleoperation updates.
To confirm you have ran the exploit successfully, use Wireshark and filter by ARP packets to see Ettercap flooding the device with spoofed ARP packets.