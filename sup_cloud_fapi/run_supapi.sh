#!/bin/bash

# Activate your virtual environment if necessary
source /var/virtualEnvs/supAPIEnv/bin/activate

# Run Gunicorn with your FastAPI app
#/var/virtualEnvs/ixgptAPIEnv/bin/gunicorn -c /var/ixgpt/ix_gpt/ixgptFastAPI/gunicorn_conf.py  main:app --bind 0.0.0.0:18001 --workers 4 --preload
python /var/LIVEIXGPT/IXGPT/main.py
