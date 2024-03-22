#!/usr/bin/env bash

# Install required apt packages
sudo apt-get update -y && sudo apt-get upgrade -y
sudo apt-get install -y python3-pip python3-dev mysql-server libmysqlclient-dev nginx pkg-config

# Install required python packages
pip3 install --upgrade pip
pip3 install -r requirements.txt

#install nodejs
sudo apt-get update && sudo apt-get install -y ca-certificates curl gnupg
curl -fsSL https://deb.nodesource.com/gpgkey/nodesource-repo.gpg.key | sudo gpg --dearmor -o /etc/apt/keyrings/nodesource.gpg
NODE_MAJOR=20
echo "deb [signed-by=/etc/apt/keyrings/nodesource.gpg] https://deb.nodesource.com/node_$NODE_MAJOR.x nodistro main" | sudo tee /etc/apt/sources.list.d/nodesource.list
sudo apt-get update && sudo apt-get install nodejs -y

# Install required node packages
sudo npm install tailwindcss @tailwindcss/forms @tailwindcss/typography postcss autoprefixer
sudo rm -rf node_modules
npm run create-css
