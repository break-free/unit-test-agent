#!/bin/bash

# TODO: Need to pass a variable to this script rather than hard wire it.
cd "fineract" || exit
./gradlew clean test --warning-mode=none
