'''
@author: hrabia
'''

import unittest

from behaviour_components.pddl import create_valid_pddl_name

class PDDLTestDuite(unittest.TestCase):
    """Testing pddl"""


    def test_pddl_name(self):
        self.assertEqual('MyNetworkManager', create_valid_pddl_name('MyNetwork/Manager'))

if __name__ == '__main__':
    unittest.main()