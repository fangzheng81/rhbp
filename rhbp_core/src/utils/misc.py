"""
This module contains various general helper functions

moduleauthor:: hrabia
"""

class FinalInitCaller(type):
    """
    This decorator allows to implement an after __init__ hook
    This allows to guarantee the execution of special initialisation
    code after the full object (full class hierarchy) was constructed
    and is ready to use

    Just implement final_init() in the (base_)class and
    set metaclass like below
    __metaclass__ = FinalInitCaller
    """
    def __call__(cls, *args, **kwargs):
        """Called when you call MyNewClass() """
        obj = type.__call__(cls, *args, **kwargs)
        obj.final_init()
        return obj