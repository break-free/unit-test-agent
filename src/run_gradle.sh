#!/bin/bash

cd "$HOME/Projects/fineract" || exit
./gradlew clean test
