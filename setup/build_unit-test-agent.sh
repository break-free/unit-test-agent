#!/bin/bash

# Check that OpenAI API Key is passed as an argument.
if [ $# -ne 1 ] 
  then
    echo "This script requires one argument: <OPENAI_API_KEY>. A key can be"
    echo "from the OpenAI website, https://openai.com/"
    exit 1
fi

# Create container
NAME=unit-test-agent
RUN="toolbox run --container $NAME"
toolbox rm --force $NAME || true
toolbox create --container $NAME

# Install applications
APPLICATIONS=" python3-pandas python3-javalang cmake gcc-c++ "

## Install applications
$RUN sudo dnf install -y $APPLICATIONS;

## Install Python packages
$RUN sudo pip install --upgrade -r setup/requirements.txt

## Add API secrets to profile.d directory
$RUN sudo bash -c 'echo -e "\
export OPENAI_API_KEY='$1' "\
> /etc/profile.d/api_secrets.sh'
