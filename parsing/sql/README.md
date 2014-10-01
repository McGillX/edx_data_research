# Load SQL files to mongoDB

### Run in UNIX terminal

```
mongoimport -d DATABASE -c COLLECTION --type tsv --file SQL_FILENAME --headerline
```

For instance,

```
mongoimport -d edx -c auth_userprofile --type tsv --file McGillX-CHEM181x-1T2014-auth_userprofile-prod-analytics.sql --headerline

mongoimport -d edx -c certificates_generatedcertificate --type tsv --file McGillX-CHEM181x-1T2014-certificates_generatedcertificate-prod-analytics.sql --headerline

mongoimport -d edx -c student_courseenrollment --type tsv --file McGillX-CHEM181x-1T2014-student_courseenrollment-prod-analytics.sql --headerline

mongoimport -d edx -c auth_user --type tsv --file McGillX-CHEM181x-1T2014-auth_user-prod-analytics.sql --headerline

mongoimport -d edx -c courseware_studentmodule --type tsv --file McGillX-CHEM181x-1T2014-courseware_studentmodule-prod-analytics.sql --headerline

```
