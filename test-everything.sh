#!/bin/sh -e
python -m unittest discover "$@"
mkdir -p demo-build
cd demo-build
../demo-project/configure
make
./hello
cd ..
rm -r demo-build
