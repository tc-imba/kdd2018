#!/bin/bash

python3 api_get.py --city=beijing
python3 fix_data.py --city=beijing
python3 generate_submission.py --city=beijing

python3 api_get.py --city=london
python3 fix_data.py --city=london
python3 generate_submission.py --city=london
