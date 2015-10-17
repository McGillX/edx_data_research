from collections import defaultdict
from datetime import date

from edx_data_research.reporting.edx_base import EdX

class Stats(EdX):

    def __init__(self, args):
        super(self.__class__, self).__init__(args)
        self.csv = args.csv
        self.number_of_students = 0

    def stats(self):
        """Return general stats for a given course """
        self.collections = ['auth_userprofile', 'certificates_generatedcertificate']
        self.number_of_students = self.collections['auth_userprofile'].count()
        age_stats = self._age()
        gender_stats = self._gender()
        certificate_stats = self._certificate()
        result = age_stats + gender_stats + certificate_stats
        if self.csv:
            report_name = self.report_name(self.db, 'stats')
            headers = ['Name', 'Stat']
            self.generate_csv(result, headers, report_name)

    def _age(self):
        age_breakdown = defaultdict(int)
        current_year = date.today().year
        cursor = self.collections['auth_userprofile'].find()
	for item in cursor:
	    year_of_birth = item['year_of_birth']
            if year_of_birth != 'NULL':
                age = current_year - int(year_of_birth)
		if age < 20:
		    age_breakdown['Age - Under 20'] += 1
		elif 20 <= age <= 29:
		    age_breakdown['Age - 20-29'] += 1
 		elif 30 <= age <= 39:
		    age_breakdown['Age - 30-39'] += 1
		elif 40 <= age <= 49:
		    age_breakdown['Age - 40-49'] += 1
		elif 50 <= age <= 69:
		    age_breakdown['Age - 50-69'] += 1
		elif age >= 70:
		    age_breakdown['Age - 70+'] += 1
	    else:
	        age_breakdown['Age - None'] += 1
        order = ['Age - Under 20', 'Age - 20-29', 'Age - 30-39', 'Age - 40-49',
                 'Age - 50-69', 'Age - 70+', 'Age - None']
        return [(key, age_breakdown[key]) for key in order]

    def _gender(self):
        gender_breakdown = defaultdict(int)
        cursor = self.collections['auth_userprofile'].find()
 	for item in cursor:
	    gender = item['gender']
	    if gender == 'm':
                gender_breakdown['Gender - Male'] += 1
	    elif gender == 'f':
                gender_breakdown['Gender - Female'] += 1
	    elif gender == 'o':
                gender_breakdown['Gender - Other'] += 1
            else:
                gender_breakdown['Gender - None'] += 1
        gender_breakdown = {key: value * 100.0 / self.number_of_students
                            for key, value in gender_breakdown.iteritems()}
        order = ['Gender - Male', 'Gender - Female', 'Gender - Other',
                 'Gender - None']
        return [(key, gender_breakdown[key]) for key in order]

    def _certificate(self):
        certificate_breakdown = defaultdict(int)
        cursor = self.collections['certificates_generatedcertificate'].find()
        for item in cursor:
            status = item['status']
            if status == 'notpassing':
                certificate_breakdown['Certificate - No'] += 1
            elif status == 'downloadable':
                certificate_breakdown['Certificate - Yes'] += 1
        certificate_breakdown = {key: value * 100.0 / self.number_of_students
                                 for key, value in certificate_breakdown.iteritems()}
        order = ['Certificate - Yes', 'Certificate - No']
        return [(key, certificate_breakdown[key]) for key in order]

