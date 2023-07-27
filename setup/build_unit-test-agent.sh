#!/bin/bash

# Check that OpenAI API Key is passed as an argument.
if [ $# -ne 1 ] 
  then
    echo "This script requires one argument: <OPENAI_API_KEY>. A key can be from the OpenAI "
    echo "website, https://openai.com/"
    exit 1
fi

# Create container
NAME=unit-test-agent
RUN="toolbox run --container $NAME"
toolbox rm --force $NAME || true
toolbox create --container $NAME

# Install applications
APPLICATIONS="cmake gcc-c++ java-11-openjdk-devel java-17-openjdk-src python3-pandas \
              python3-javalang unzip"

## Install applications
$RUN sudo dnf install -y $APPLICATIONS;

## Install Gradle 7.5.1

$RUN curl -O https://downloads.gradle.org/distributions/gradle-7.5.1-all.zip
$RUN sudo mkdir /opt/gradle
$RUN sudo unzip -d /opt/gradle gradle-7.5.1-all.zip
$RUN sudo bash -c ' echo \
    "export PATH='$PATH':/opt/gradle/gradle-7.5.1/bin" \
    > /etc/profile.d/gradle.sh'

## Install Python packages
$RUN pip install --upgrade -r setup/requirements.txt

## Add API secrets to profile.d directory
$RUN sudo bash -c 'echo -e "\
export OPENAI_API_KEY='$1' "\
> /etc/profile.d/api_secrets.sh'

## Provide linked command outside of the toolbox for podman/docker

$RUN sudo bash -c 'echo -e "\
alias docker='\''flatpak-spawn --host /usr/bin/podman'\'' \n\
alias podman='\''flatpak-spawn --host /usr/bin/podman'\'' "\
> /etc/profile.d/docker.sh'
