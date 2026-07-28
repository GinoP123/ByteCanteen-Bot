#!/bin/bash

: "
	

	Reminder To Update Lark Token!!!


"


export PATH="/opt/homebrew/bin:/opt/homebrew/Caskroom/miniconda/base/bin:$PATH"

directory="$(dirname "$0")"
if [[ "$directory" == "." ]]; then
	ttab $(realpath "$directory/update_token.sh")
	exit 0
fi

cd "$directory"

python3 scripts/setup.py

