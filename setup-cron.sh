#!/bin/bash

(crontab -l 2>/dev/null; echo "*/10 * * * * cd /Users/nlarusso/Personal/trello-dashboard && ./run.sh > dashboard.log") | crontab -