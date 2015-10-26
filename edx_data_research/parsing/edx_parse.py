import abc

from edx_data_research.edx_base import EdX

class EdXParse(EdX):
    __metaclass__ = abc.ABCMeta
    
    def __init__(self, args):
	super(EdXParse, self).__init__(args)

    @abc.abstractmethod
    def migrate(self):
        """Migrate data to database"""
	pass
