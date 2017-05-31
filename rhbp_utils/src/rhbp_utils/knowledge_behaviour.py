'''
Created on 24.05.2017

@author: hrabia
'''
import rospy
from knowledge_base.knowledge_base_manager import KnowledgeBase
from behaviour_components.behaviours import BehaviourBase

from knowledge_base.knowledge_base_client import KnowledgeBaseClient


class KnowledgeUpdateBehaviour(BehaviourBase):
    '''
    Behaviour that updates knowledge after it is activated
    '''

    def __init__(self, name, pattern, new_tuple,knowledge_base_name=KnowledgeBase.DEFAULT_NAME, **kwargs):

        super(KnowledgeUpdateBehaviour, self) \
            .__init__(name=name,**kwargs)

        self.pattern = pattern
        self.new_tuple = new_tuple

        self._kb_client = KnowledgeBaseClient(knowledge_base_name=knowledge_base_name)

    def start(self):
        rospy.logdebug("Updating knowledge '%s' to '%s'", self.pattern, self.new_tuple)

        self._kb_client.update(self.pattern, self.new_tuple )

