#!/bin/bash

# TODO: Need to pass a variable to this script rather than hard wire it.
cd "/var/home/chris/Projects/fineract" || exit
./gradlew clean test
