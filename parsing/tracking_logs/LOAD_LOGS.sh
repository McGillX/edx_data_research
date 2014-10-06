DATABASE="atoc185x"
COLLECTION="tracking_atoc185x_before_may_27"
DIRECTORY="/data/tracking_logs_before_may_27"

FILES=$(find $DIRECTORY -type f -name *.log)

filelist=""

for f in $FILES
do
filelist="$filelist $f"
done

python load_log_mongod.py $DATABASE $COLLECTION $filelist
