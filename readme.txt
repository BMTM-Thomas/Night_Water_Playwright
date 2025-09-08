# Brew Install
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Set Brew Path
echo >> /Users/automation/.zprofile
    echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> /Users/automation/.zprofile
    eval "$(/opt/homebrew/bin/brew shellenv)"

# Python install (Any Version)
https://www.python.org/downloads/

# Visual Studio Code
https://code.visualstudio.com

# Open Terminal install package
brew install git
pip3 install python-dotenv
pip3 install PyAutoGUI==0.9.52
pip3 install pytest-playwright
pip3 install playwright
pip3 install Pillow
pip install PyScreeze==1.0.0
pip3 install openai
playwright install

# Gmail API
pip3 install google-api-python-client google-auth google-auth-httplib2 google-auth-oauthlib

# MongoDB API
pip3 install pymongo

# Openai API
pip3 install openai

