'''
Created on 05.01.2017

@author: rieger
'''

from .activators import Activator, BooleanActivator, Condition, GreedyActivator
from .behaviours import BehaviourBase
from .goals import OfflineGoal
from .managers import Manager


class NetworkBehavior(BehaviourBase):
    """
    Behavior, which encapsulates an additional manager and behaviors.
    This allows to build hierarchies of hybrid behaviour planners.
    It must be in separate file, because of circular dependencies (depends on manager, but manager depends on Behavior)
    """

    MANAGER_POSTFIX = "/Manager"

    def __init__(self, effects, name, requires_execution_steps=False,
                 only_running_for_deciding_interruptible=Manager.USE_ONLY_RUNNING_BEHAVIOURS_FOR_INTERRUPTIBLE_DEFAULT_VALUE,
                 **kwargs):
        """
        :param effects: tuple <sensor,Effect>
        :param name: name of the behaviour that is also used to create the sub manager name together with the NetworkBehavior.MANAGER_POSTFIX
        :param requires_execution_steps: whether the execution steps should be caused from the parent manager or not.
                If not, the step method must be called manually
        :param kwargs: args for the manager, except the prefix arg
        """
        super(NetworkBehavior, self).__init__(name=name, requires_execution_steps=requires_execution_steps, **kwargs)
        self.requires_execution_steps = requires_execution_steps
        manager_args = {}
        manager_args.update(kwargs)
        manager_args['prefix'] = name + NetworkBehavior.MANAGER_POSTFIX
        self.__manager = Manager(activated=False,
                                 use_only_running_behaviors_for_interRuptible=only_running_for_deciding_interruptible,
                                 **manager_args)

        self.__goal_name_prefix = name + "/Goals/"
        self.__goal_counter = 0

        #Generate goals for effect
        correlations = []
        for effect in effects:
            correlations.append(effect[1])
            goal_name = self.__generate_goal_name(effect[1])
            activator_name = self._restore_condition_name_from_pddl_function_name(effect[1].sensorName, effect[0].name)
            goal = self._create_goal(sensor=effect[0], effect=effect[1], goal_name=goal_name,
                                     activator_name=activator_name)
            self.__manager.add_goal(goal)
        self.correlations = correlations

    def _restore_condition_name_from_pddl_function_name(self, pddl_function_name, sensor_name):
        return Activator.restore_condition_name_from_pddl_function_name(pddl_function_name=pddl_function_name,
                                                                        sensor_name=sensor_name)

    def __generate_goal_name(self, effect):
        """
        :param effect: instance of type  Effect
        :return: unique name for goal
        """
        # x as seperator between counter an sensor names, to prevent conflict, caused by unusual names
        name = self.__goal_name_prefix + str(self.__goal_counter) + 'X' + effect.sensorName
        self.__goal_counter += 1
        return name

    def _create_goal(self, sensor, effect, goal_name, activator_name):
        """
        Generate goals, which made the manager trying to work infinitely on the given effect,
         until the network is stopped. Therefore the goal shouldn't reachable (except the goal for boolean effects)
        :param sensor: instance of type Sensor
        :param effect: instance of type  Effect
        :param goal_name: unique name for the goal
        :return: a goal, which causes the manager to work on the effect during the whole time
        """
        if (effect.sensorType == bool):
            desired_value = True if effect.indicator > 0 else False
            activator = BooleanActivator(name=activator_name, desiredValue=desired_value)
            condition = Condition(activator=activator, sensor=sensor)
            return OfflineGoal(goal_name, permanent=True, conditions={condition})
        if (effect.sensorType == int or effect.sensorType == float):
            activator = GreedyActivator(maximize=effect.indicator > 0, step_size=effect.realWorldImpact,
                                        name=activator_name)
            condition = Condition(activator=activator, sensor=sensor)
            return OfflineGoal(goal_name, permanent=True, conditions={condition})
        raise RuntimeError(msg='Cant create goal for effect type \'' + str(
            effect.sensorType) + '\'. Overwrite the method _create_goal for handle the type')

    def _add_additional_goal(self, goal):
        """
        Adds the given goal to nested manager
        :param goal: AbstractGoalRepresentation
        """
        self.__manager.add_goal(goal)

    def do_step(self):
        self.__manager.step()

    def start(self):
        self.__manager.activate()

    def stop(self):
        self.__manager.deactivate()

    def _is_interruptible(self):
        return self.__manager.is_interruptible()
