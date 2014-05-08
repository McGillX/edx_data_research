# mongod_to_csv

### Convert the .mongo discussion database from a hosted mongod to .csv for analysis

There are two different types of document structures. They differ by _type ``Comment`` or ``Comment_Thread``

See edX docs on .mongo format https://github.com/edx/edx-platform/blob/master/docs/en_us/data/source/internal_data_formats/discussion_data.rst

This command export a .csv file with all fields of both type of document.

Run this on a UNIX SHELL not the mongo shell
```mongoexport --host localhost --db edx --collection forum --csv --out data.csv --fields _id.oid,_type,abuse_flaggers,anonymous,anonymous_to_peers,at_position_list,author_id,author_username,title,body,comment_thread_id.oid,course_id,created_at.date,endorsed,historical_abuse_flaggers,parent_ids,sk,update_at.date,visible,votes.count,votes.up,votes.down,votes.up_count,votes.down_count,votes.point,comment_count,at_position_list,commentable_id,closed,last_activity_at.date```