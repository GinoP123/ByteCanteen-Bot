import os

config_path = "config.json"
session_path = ".session.json"
preferences_path = "preferences.md"
commands_run_path = "commands_run.sh"

with open(preferences_path) as infile:
    preferences = f"{infile.read()}".replace("'", '').replace('"', '')

llm_path = './llm.sh'
open_path = "/Applications/Sublime Text.app/Contents/SharedSupport/bin/subl"
node_path = "/opt/homebrew/bin/node"

#### FIX
meal_type = 'lunch'
location = "1199Coleman"
date_format = '%Y-%m-%d'
valid_days_threshold = 0
nano_per_micro_second = int(1e6)
micro_per_second = int(1e3)

### Warnings for Session Status

ttlDays = 7
warnDays = 2
DAY_MS = 86400000
