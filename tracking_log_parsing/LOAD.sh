DATABASE="edx"
COLLECTION="tracking"
DIRECTORY="CHEM181x_logs_decrypted"

FILES=$(find $DIRECTORY -type f -name *.log)

filelist=""

for f in $FILES"
do
filelist="$filelist $f"
done

python load_log_mongo.py $DATABASE $COLLECTION $filelist