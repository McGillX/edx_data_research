DATABASE="edx"
COLLECTION="tracking"
DIRECTORY="CHEM181x_logs_decrypted"

FILES=$(find $DIRECTORY -type f -name *.log)

for f in $FILES
do
python load_log_mongo.py $DATABASE $COLLECTION $f
done