# Downloading Repo
```
git clone https://github.com/GinoP123/ByteCanteen-Bot.git
cd ByteCanteen-Bot
unzip scripts.zip
```

# Installing Homebrew
```
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
(echo; echo 'eval "$(/opt/homebrew/bin/brew shellenv)"') >> ~/.zprofile
eval "$(/opt/homebrew/bin/brew shellenv)"
```

# Installing git (if not installed)
```
brew install git
```

# Installing Node
```
brew install node
```

# Installing Ollama
```
brew install ollama
brew services start ollama
./llm.sh hi
```

# Installing miniconda
```
brew install --cask miniconda
```

# Installing ttab
```
brew tap mklement0/ttab https://github.com/mklement0/ttab.git
brew install mklement0/ttab/ttab
```

# Install Sublime
https://www.sublimetext.com/download

# Adding to Crontab
```
crontab crontab.txt
```

## Checking Installation
```
./check_token.sh
./place_orders.py
crontab -l
```
