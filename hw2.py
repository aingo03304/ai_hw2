# 2020S Artificial Intelligence HW 2
# 2020-90829 Minjae Kim

from enum import Enum

class Environment(object):
    def __init__(self, n_room, shape, dirt_placement):
        self.n_room = n_room # a number of rooms
        self.shape = shape # a type of shape, iterators and append method should be specified.
        self.dirt_placement = dirt_placement # dirt placement, a list of boolean
        self.current_status = self.shape()
        self.current_position = 0
        self.init_env(n_room, shape, dirt_placement)
            
    def init_env(self, n_room, shape, dirt_placement):
        for is_dirt in dirt_placement:
            self.current_status.append(is_dirt)
            
    def get_priori(self):
        return (self.n_room, self.shape) # Geography is a priori
    
    def move(self, n):
        self.current_position = n
        
    def clean(self, n):
        self.current_status[n] = False
        
    def get_current_position(self):
        return self.current_position
    
    def get_current_room_status(self):
        return self.current_status[self.current_position]
        
    def _throw_dirt(self, n):
        self.current_status[n] = True

class Sensor(object):
    def __init__(self, env):
        self.env = env
        
    def percept(self, env):
        raise NotImplementedError('This is base class, you have to implement with inheriting this class.')

class PositionSensor(Sensor):
    def percept(self):
        return self.env.get_current_position()

class DirtSensor(Sensor):
    def percept(self):
        return self.env.get_current_room_status()

class Action(Enum):
    LEFT = 0
    RIGHT = 1
    SUCK = 2

class Actuator(object):
    def __init__(self, env):
        self.env = env
        
    def action(self):
        raise NotImplementedError('This is base class, you have to implement with inheriting this class.')

class LeftMotor(Actuator):
    def action(self, position):
        if position - 1 >= 0:
            self.env.move(position - 1)
        
class RightMotor(Actuator):
    def action(self, position):
        if position + 1 < self.env.n_room:
            self.env.move(position + 1)
            
class Suction(Actuator):
    def action(self, position):
        self.env.clean(position)
    
class Agent(object):
    def __init__(self, sensors, actuators, actions_tabulation):
        self.sensors = sensors
        self.actuators = actuators
        self.percept_sequence = ()
        self.current_position = None
        self.actions_tabulation = actions_tabulation
        self.performance = 0
        
    def percept(self):
        self.current_position = self.sensors['position'].percept()
        self.percept_sequence += ((
            self.current_position, 
            self.sensors['dirt'].percept()
        ),)
    
    def action(self):
        result_action = self.actions_tabulation[self.percept_sequence]
        if result_action == Action.SUCK:
            self.performance += 1
        self.actuators[result_action].action(self.current_position)
    
    def get_performance(self):
        return self.performance
    
    def clean_percept_sequence(self):
        self.percept_sequence = ()
        
def display(env, agent):
    result_str = '[ '
    for i, is_dirt in enumerate(env.current_status):
        if i == env.current_position:
            result_str += 'O '
        if is_dirt:
            result_str += 'True '
        else:
            result_str += 'False '
    result_str += '] '
    result_str += str(agent.get_performance()) + ' '
    result_str += str(agent.percept_sequence) + ' => '
    result_str += str(agent.actions_tabulation[agent.percept_sequence])
    print(result_str)

lifetime = 1000
environment = Environment(
    n_room=2,
    shape=list,
    dirt_placement=[True, True]
)
vacuum_cleaner_agent = Agent(
    sensors={
        'position': PositionSensor(environment),
        'dirt': DirtSensor(environment)
    },
    actuators={
        Action.LEFT: LeftMotor(environment),
        Action.RIGHT: RightMotor(environment),
        Action.SUCK: Suction(environment)
    },
    actions_tabulation={
        ((0, False),): Action.RIGHT,
        ((0, True),): Action.SUCK,
        ((1, False),): Action.LEFT,
        ((1, True),): Action.SUCK,
        ((0, False), (0, False)): Action.RIGHT,
        ((0, False), (0, True)): Action.SUCK,
        ((0, True), (0, True)): Action.SUCK,
        ((1, False), (1, False)): Action.LEFT,
        ((1, False), (1, True)): Action.SUCK,
        ((1, True), (1, True)): Action.SUCK,
    }
)

for time in range(lifetime):
    vacuum_cleaner_agent.percept()
    vacuum_cleaner_agent.percept()
    vacuum_cleaner_agent.action()
    display(environment, vacuum_cleaner_agent)
    vacuum_cleaner_agent.clean_percept_sequence()
