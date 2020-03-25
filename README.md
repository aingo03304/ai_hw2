# Artificial Intelligence HW2
Homework Solution for Artificial Intelligence

# Problem
Implement a performance-measuring environment simulator for the vacuum-cleaner world depicked in Figure 2.2 and specified on page 38. Your implementation should be modular so that the sensors, actuators, and environment characteristics (size, shape, dirt placement, etc.) can be changed easily. (Note: for some choives of programming language and operating system there are already implementations in the online code repository.)

# Classes

## Environment
Environment class contains followings
- a number of rooms
- a shape of rooms
- dirt placement
- current status of rooms
- current position of the agent

and some methods are implemented like below
- get_priori
- move
- clean
- get_current_position
- get_current_room_status
- _throw_dirt

## Sensor
The base class of sensors is declared and contains environment as a member.  
and two inherited classes exist.

### PositionSensor
PositionSensor percepts the position of the agent.

### DirtSensor
DirtSensor percepts the dirt status of the position where agent is placed.

## Actuator
The base class of actuators is declared and contains environment as a member.  
and three inherited classes exist.

### LeftMotor
LeftMotor acts to move the agent left.

### RightMotor
RightMoter acts to move the agent right.

### Suction
Suction acts to suck the dirt on the place where agent is placed.

## Agent
Agent class has followings as members.
- a list of sensors
- a list of actuators
- a percept sequence
- a current position
- a tabulation of actions
- a performance

and has four kinds of methods.
- percept
- action
- get_performance
- clean_percept_sequence

