# Load SQL files to mongoDB

### Use

```
mongoimport -d DATABASE -c COLLECTION --type tsv --file SQL_FILENAME --headerline
```
Options:

    -d <database>: Specifies the name of the database on which to run mongoimport

    -c <collection>: Specifies the collection to import

    --type <json|csv|tsv> : Specifies the file type to import. The default format is json

    --file <filename> : Specifies the location and name of a file containing data to import

    --headerline : If using --type csv or --type tsv, uses the first line as field names. Otherwise, `mongoimport` will import the first line as a distinct document
    
For more options, refer to: <http://docs.mongodb.org/manual/reference/program/mongoimport/>

#### Commands for importing SQL data to mongoDB provided by edX for CHEM181x:

```
mongoimport -d edx -c auth_userprofile --type tsv --file McGillX-CHEM181x-1T2014-auth_userprofile-prod-analytics.sql --headerline

mongoimport -d edx -c certificates_generatedcertificate --type tsv --file McGillX-CHEM181x-1T2014-certificates_generatedcertificate-prod-analytics.sql --headerline

mongoimport -d edx -c student_courseenrollment --type tsv --file McGillX-CHEM181x-1T2014-student_courseenrollment-prod-analytics.sql --headerline

mongoimport -d edx -c auth_user --type tsv --file McGillX-CHEM181x-1T2014-auth_user-prod-analytics.sql --headerline

mongoimport -d edx -c courseware_studentmodule --type tsv --file McGillX-CHEM181x-1T2014-courseware_studentmodule-prod-analytics.sql --headerline

```
