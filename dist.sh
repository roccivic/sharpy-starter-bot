#!/bin/bash

rm -rf sharpy jsonpickle sc2 sc2pathlib
echo 0.0.0 > version.txt
python ./ladder_zip.py -n terran
