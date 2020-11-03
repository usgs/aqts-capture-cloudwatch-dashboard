# aqts-capture-cloudwatch-dashboard
[![Build Status](https://travis-ci.org/usgs/aqts-capture-cloudwatch-dashboard.svg?branch=main)](https://travis-ci.org/usgs/aqts-capture-cloudwatch-dashboard)
[![codecov](https://codecov.io/gh/usgs/aqts-capture-cloudwatch-dashboard/branch/main/graph/badge.svg)](https://codecov.io/gh/usgs/aqts-capture-cloudwatch-dashboard)

This tool uses the AWS Python SDK (boto3) to create, update, and deploy a cloudwatch dashboard for the purpose of monitoring the aqts-capture etl assets.

### Unit testing
Make sure you have python version 3.8 (or later) and pip installed, then run:

```shell script
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
python -m unittest -v
```
