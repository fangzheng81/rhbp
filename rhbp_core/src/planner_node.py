#! /usr/bin/env python2
'''
Created on 13.04.2015

@author: stephan, hrabia
'''
import rospy
from behaviour_components.managers import Manager
from rhbp_core.srv import SetStepping, SetSteppingResponse
from std_srvs.srv import Empty, EmptyResponse

class ManagerNode(object):
    """
    ROS node wrapper for the rhbp manager/planner
    """

    def __init__(self):
        rospy.init_node('behaviourPlannerManager', log_level=rospy.WARN)
        prefix = rospy.get_param("~prefix", "")
        self._manager = Manager(prefix=prefix)
        self.rate = rospy.Rate(rospy.get_param("~frequency", 1))

        self.automatic_stepping = rospy.get_param("~automatic_stepping", True)

        if not self.automatic_stepping:
            rospy.logwarn("Started in manual stepping mode")

        self._set_automatic_stepping_service= rospy.Service(prefix + '/' +'set_automatic_stepping', SetStepping, self._set_stepping_callback)

        self._stepping_service = rospy.Service(prefix + '/' + 'step', Empty, self._step_callback)

    def _set_stepping_callback(self, request):
        """
        Callback service for enabling or disabling automatic stepping in the given frequency
        :param request:
        """
        self.automatic_stepping = request.automatic_stepping

        return  SetSteppingResponse()

    def _step_callback(self, request):
        """
        Service callback for manual planning/manager steps
        :param request:
        """
        if not self.automatic_stepping:
            self._manager.step()
        else:
            rospy.logwarn("No manual stepping if automatic stepping is enabled")
        return EmptyResponse()

    def run(self):
        """
        Executing the node after initialization
        """
        while (not rospy.is_shutdown()):
            if self.automatic_stepping:
                self._manager.step()
            self.rate.sleep()

if __name__ == '__main__':
    node = ManagerNode()
    node.run()

