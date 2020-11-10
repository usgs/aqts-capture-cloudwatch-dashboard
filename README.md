# aqts-capture-cloudwatch-dashboard
[![Build Status](https://travis-ci.com/usgs/aqts-capture-cloudwatch-dashboard.svg?branch=main)](https://travis-ci.com/usgs/aqts-capture-cloudwatch-dashboard)
[![codecov](https://codecov.io/gh/usgs/aqts-capture-cloudwatch-dashboard/branch/main/graph/badge.svg)](https://codecov.io/gh/usgs/aqts-capture-cloudwatch-dashboard)

This tool uses the AWS Python SDK (boto3) to create, update, and deploy a cloudwatch dashboard for the purpose of monitoring the aqts-capture etl assets.

### How it works
Using the Jenkins job runner, we build a docker container with python installed, then run the python entry-point script to begin creating a cloudwatch dashboard.

### Unit testing
Make sure you have python version 3.8 (or later), pip, and venv installed, then run:

```shell script
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
python -m unittest -v
```
