DATABASE="edx"
COLLECTION="tracking_before_jan22"
DIRECTORY="before_jan22"

FILES=$(find $DIRECTORY -type f -name *.log)

filelist=""

for f in $FILES
do
filelist="$filelist $f"
done

python load_log_mongod.py $DATABASE $COLLECTION $filelist