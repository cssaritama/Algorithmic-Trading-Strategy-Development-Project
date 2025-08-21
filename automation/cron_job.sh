#**Author:** Carlos Stalin Saritama Atopo  
#**Email:** cssaritama@gmail.com  
#**Area of Specialization:** Analytics, Advanced Analytics, and Artificial Intelligence  
#**Date:** August 2025 



#!/bin/bash
# To install: crontab -e  -> add: 0 2 * * * /path/to/repo/automation/cron_job.sh >> /path/to/repo/logs/cron.log 2>&1

cd /path/to/repo
source ./venv/bin/activate || true
python scripts/run_pipeline.py --use-sample