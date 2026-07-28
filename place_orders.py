#!/opt/homebrew/Caskroom/miniconda/base/bin/python3

import json
import sys
import os, glob
import subprocess as sp
import random
import ast
from datetime import datetime, timedelta
from tqdm import tqdm

if __name__ == "__main__":
    directory = os.path.dirname(sys.argv[0])
    os.chdir(directory)

import settings

curr_date = datetime.now()
curr_date += timedelta(weeks=1)

for _ in range(7):
    date = curr_date.strftime(settings.date_format)
    print(date)
    curr_date += timedelta(days=1)

    command = f"cd '{directory}'; node scripts/foodtruck.mjs list '{date}' {settings.meal_type} {settings.location}"
    dishes_day = sp.run(command, capture_output=True, shell=True).stdout.decode()
    dishes_day = json.loads(dishes_day)

    date = dishes_day['mealDate']
    if dishes_day['lifecycleStage'] != 'BOOKING':
        print(f"{dishes_day['lifecycleStage']}\n")
        continue
    elif dishes_day['hadOrdered'] == True:
        print("Exiting Early, Already Ordered\n")
        continue

    booking_options = []
    for dish in dishes_day['items']:
        if dish['currentStock'] == 0:
            continue
        elif dish['description'] == '':
            dish['description'] = 'Missing'
        booking_options.append((dish['name'], dish['description']))

    if booking_options:
        choice = str(random.randint(1, len(booking_options)))
        prompt = f"{settings.preferences}\n\nHere are the choices: \n"
        for i, (booking_option, booking_description) in enumerate(booking_options, start=1):
            prompt += f"{i}.) {booking_option}\n\tDescription: {booking_description}\n\n"
        prompt += f"Please output only the choice number between {1} and {len(booking_options)} with no explanation and no formatting."

        output = sp.run(f"{settings.llm_path} '''{prompt}'''", 
            capture_output=True, shell=True).stdout.decode().strip()
        output = output.replace(')', '').replace('(', '').replace('.', '')

        if output.isnumeric() and 1 <= ast.literal_eval(output) <= len(booking_options):
            choice = output
        else:
            print("ERROR: MODEL OUTPUT FAILED", output)

        choice = booking_options[ast.literal_eval(choice)-1][0]

        command = f"cd '{directory}'; node scripts/foodtruck.mjs order --date {date} --meal {settings.meal_type} --select '{choice}' --building {settings.location}"
        output = sp.run(command, capture_output=True, shell=True).stdout.decode()
        print(f"Submitted {choice} on {date}\n")
    else:
        print("No Booking Options\n")


