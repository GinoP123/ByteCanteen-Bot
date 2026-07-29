#!/bin/bash

sed -i "" "s,<PATH_TO_REPO>,$PWD,g" crontab.txt
crontab crontab.txt
./check_token.sh 2> /dev/null > /dev/null
crontab -l
