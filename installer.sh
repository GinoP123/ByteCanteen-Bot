#!/bin/bash

echo '#!/bin/bash' > "commands_run.sh"
chmod u+x "commands_run.sh"
mkdir -p cron_log
crontab crontab.txt
./check_token.sh 2> /dev/null > /dev/null
crontab -l
