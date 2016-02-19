import abc


class Parse(object):
    __metaclass__ = abc.ABCMeta
    
    def __init__(self, args):
	super(Parse, self).__init__(args)

    @abc.abstractmethod
    def do(self):
        """Run a task"""
		pass