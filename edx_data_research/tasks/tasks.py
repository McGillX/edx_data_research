import abc


class Tasks(object):
    __metaclass__ = abc.ABCMeta
    
    @abc.abstractmethod
    def do(self):
        """Run a task"""
        pass
