
from datetime import date

from edx_data_research.reporting.edx_base import EdX

class Stats(EdX):

    def __init__(self, args):
        super(self.__class__, self).__init__(args)

    def stats(self):
        """Return general stats for a given course """
        self.collections = ['auth_userprofile']
        self._age()

    def _age(self):
        current_year = date.today().year
        print current_year
        
