import abc

from edx_data_research.base import Base

class Parse(Base):
    __metaclass__ = abc.ABCMeta
    
    def __init__(self, args):
	super(Parse, self).__init__(args)

    @abc.abstractmethod
    def migrate(self):
        """Migrate data to database"""
	pass
