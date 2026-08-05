#!/bin/bash

cd "$(dirname "$0")"
export PATH="/opt/homebrew/bin:/opt/homebrew/Caskroom/miniconda/base/bin:$PATH"

threshold="$(python3 -c "import settings; print(settings.valid_days_threshold)")"
open_path="$(python3 -c "import settings; print(settings.open_path)")"
cmd="import json; import sys; print(json.load(sys.stdin)['daysLeft'] <= $threshold)"

needs_update=$(node scripts/session_status.mjs | python3 -c "$cmd" 2> /dev/null)

if [[ "$needs_update" != "False" ]]; then
	"$open_path" update_token.sh
fi

