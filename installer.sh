#!/bin/bash

sed -i "" "s,<PATH_TO_REPO>,$PWD,g" crontab.txt
crontab crontab.txt
crontab -l
