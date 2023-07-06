
# Remote Unit back-end

This repository is a Django server, which is the back-end of a ROS robotics support system, acting as the interface between the systems and the MongoDB database server.

# Database

The database that this Django server communicates with is a MongoDB server running on the same machine. By default, the address of the server is 127.0.0.1 on port 27017, without more settings.
* *If the server is at a different address or need more configurations, you'll need to modify the variable of the **Client** to suit the new address*
			`Client  =  MongoClient('mongodb://localhost:27017/')`
			

# URIs

In this server six URIs are available for interaction with the server. These are described below:

## /action
This uri communicates queries to the data collection **CeDRI_dashboard.action**. It has the following http methods available:

## /chart

This uri communicates queries to the data collection **CeDRI_dashboard.charts**. It has the following http methods available:

## /robot

This uri communicates queries to the data collection **CeDRI_dashboard.robot**. It has the following http methods available:

## /script

This uri communicates queries to the data collection **CeDRI_dashboard.script**. It has the following http methods available:

## /log

This uri communicates queries to the data collection **CeDRI_dashboard.log**. It has the following http methods available:




# Background processes

This server allows data analysis processes to be executed in the background. Being thought to act as an orchestrator of a robotic system. Creating processes based on python codes saved in a database. 

## Available commands

The customised commands available for implementation in the background processes are as follows:

### action

It is a command that aims to send an action to the robot that is being supervised to execute. This way, the command has the following structure when declared in the front-end application:

	action('action ID')

Where *action ID* is the BSON ID of the action you want to send to the robot to perform.

### 	command

This function must send an action whose content is not registered in the database, directly executing the command in an internal robot terminal. Where its structure in the front-end application has the following call format:

	command('bash instruction')

### log 

This function will create an item in the application log base. It has the following way of being called in the front-end application:

    log('the message', 'type of message')

This way it is possible to save a message of string type. And the message types that can be saved are as shown below:

 - info
 - warn
 - error
 - debug

When saving with another type, there will be no colour discrimination or icons in the front-end application.


# More information

This package was developed as part of the thesis for Master in Industrial Engineering with specialization in Electrical Engineering at Polytechnic Institute of Bragança (_IPB_), the work was developed at the Research Centre in Digitalization and Intelligent Robotics (_CeDRI_).
The project consists of three repositories with the links below:
	
>https://github.com/alf767443/node_monitoring

>https://github.com/alf767443/ros_monitoring

>https://github.com/alf767443/UGV-dashboard
