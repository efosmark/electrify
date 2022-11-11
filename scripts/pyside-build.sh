#!/bin/bash

RED='\033[0;31m'
NC='\033[0m'

fail() {
    printf "${RED}\n\n%s\n${NC}" "$1" >&2
    printf "Exiting.\n" >&2
    exit 1
}

printf "Running pyside6-project build commands...\n\n"

source ./env/bin/activate
pushd electrify_ui/qt_screens/ > /dev/null
printf "pyside6-project\n"
pyside6-project build || fail "Unable to run pyside6-project build command."
printf "pyside6-rcc\n"
pyside6-rcc icons.qrc -o icons_rc.py || fail "Unable to bundle icons using pyside6-rcc."
popd > /dev/null

printf "rc-post-fix\n"
./env/bin/python scripts/rc-post-fix.py electrify_ui/qt_screens || fail "Unable to post-fix the import statements for rc files."

printf "\nDone.\n\n"
