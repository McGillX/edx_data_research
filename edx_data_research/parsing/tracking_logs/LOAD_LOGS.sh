DATABASE="tracking_logs"
COLLECTION="tracking"
DIRECTORY="/data/tracking"

FILES=$(find $DIRECTORY -type f -name *.log)

filelist=""

for f in $FILES
do
filelist="$filelist $f"
done

python edx_data_research/parsing/tracking_logs/load_log_mongod.py $DATABASE $COLLECTION $filelist >> output.txt
