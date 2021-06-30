# mail_parser

The script is intended for parsing logs. The script receives, stores and filters data from the logs.

## Simple script call:

> python -u app.py

## Calling data to a sqlite database file.

> python -u app.py -S

> python -u app.py --save

## Call with the indication of the path to the log file or folder with log files.

#### path to single file "sample.log"

> python -u app.py -P logs/sample.log

> python -u app.py --path logs/sample.log

#### path to directory with log files "sample_directory"

> python -u app.py -P logs/sample_directory

> python -u app.py --path logs/sample_directory

#### show data with limited output lines

> python -u search.py -V -L 10

> python -u search.py --verbose --limit 10
