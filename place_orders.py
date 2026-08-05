#!/opt/homebrew/Caskroom/miniconda/base/bin/python3

import json
import sys
import os, glob
import subprocess as sp
import random
import ast
from datetime import datetime, timedelta
from tqdm import tqdm
import time

if __name__ == "__main__":
    directory = os.path.realpath(os.path.dirname(sys.argv[0]))
    os.chdir(directory)

import settings


curr_date = datetime.now()
curr_date += timedelta(weeks=1)

### Waiting For Cached Dishes To Run Quickly
if os.path.exists(settings.commands_run_path) and datetime.fromtimestamp(os.path.getmtime(settings.commands_run_path)).date() == datetime.now().date():
    cached_dishes = int(sp.run(f"wc -l '{settings.commands_run_path}'", shell=True, capture_output=True).stdout.decode().strip().split()[0])
    if cached_dishes > 2:
        time.sleep(30)

preparing_dishes_file = open(settings.commands_run_path, 'w')
preparing_dishes_file.write('#!/bin/bash\n')


updates = open(settings.updates_path, 'w')
updates.write(f'# {str(datetime.now().date())}\n\n')


for _ in range(7):
    date = curr_date.strftime(settings.date_format)
    curr_date += timedelta(days=1)

    if not os.path.exists(settings.session_path):
        updates.write(f"### {date}: ERROR: No Lark Session Found, Please Update Lark Token\n\n")
        continue

    command = f"cd '{directory}'; {settings.node_path} scripts/foodtruck.mjs list '{date}' {settings.meal_type} {settings.location}"
    dishes_day = sp.run(command, capture_output=True, shell=True).stdout.decode()
    dishes_day = json.loads(dishes_day)

    date = dishes_day['mealDate']
    if dishes_day['lifecycleStage'] != 'BOOKING' and not dishes_day['items']:
        updates.write(f"### {date}: {dishes_day['lifecycleStage']}\n\n")
        continue
    elif dishes_day['hadOrdered'] == True:
        updates.write(f"### {date}: Already Ordered {dishes_day['bookedOrderInfo']['foodName']}\n\n")
        continue

    booking_options = []
    for dish in dishes_day['items']:
        if dish['currentStock'] == 0:
            continue
        elif dish['description'] == '':
            dish['description'] = 'Missing'
        booking_options.append((dish['name'], dish['truck'], dish['description']))

    if booking_options:
        choice = str(random.randint(1, len(booking_options)))
        prompt = f"{settings.preferences}\n\nHere are the choices: \n"
        for i, (booking_option, booking_truck, booking_description) in enumerate(booking_options, start=1):
            prompt += f"{i}.) {booking_option}\n\tTruck: {booking_truck}\n\tDescription: {booking_description}\n\n"
        prompt += f"Please output only the choice number between {1} and {len(booking_options)} with no explanation and no formatting."
        prompt = prompt.replace('"', '').replace("'", '')
        
        output = sp.run(f"{settings.llm_path} '''{prompt}'''", 
            capture_output=True, shell=True).stdout.decode().strip()
        output = output.replace(')', '').replace('(', '').replace('.', '').strip()

        if output.isnumeric() and 1 <= ast.literal_eval(output) <= len(booking_options):
            choice = output
        else:
            updates.write(f"### {date}: ERROR MODEL OUTPUT FAILED\n", output)

        choice = booking_options[ast.literal_eval(choice)-1][0]

        command = f"cd '{directory}'; {settings.node_path} scripts/foodtruck.mjs order --date {date} --meal {settings.meal_type} --select '{choice}' --building {settings.location}"

        if dishes_day['lifecycleStage'] == 'BOOKING':
            output = sp.run(command, capture_output=True, shell=True).stdout.decode()
            updates.write(f'### {date}: Submitted {choice} on {date}\n\n')
        else:
            preparing_dishes_file.write(f"{command}\n\n")
            updates.write(f"### {date}: Cached {choice}; Will Submit in ~5 min\n\n")
    else:
        updates.write(f"### {date}: No Booking Options\n\n")


preparing_dishes_file.close()
updates.close()

sp.run(f"cd '{directory}'; '{settings.open_path}' '{settings.updates_path}'", shell=True)


