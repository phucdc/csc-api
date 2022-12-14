#!/bin/bash

python3 --version 2>&1 >/dev/null || ( echo "Missing package: python3" && exit )
pip3 --version 2>&1 >/dev/null || ( echo "Missing package: python-pip3" && exit )

echo "Enter SonarCloud's organization:"
read sc_organization
echo "Enter SonarCloud's token:"
read sc_token
export SC_ORGANIZATION=${sc_organization}
export SC_TOKEN=${sc_token}
env | grep SC_

echo "Installing requirements"
pip3 install -r requirements.txt &>>install.log

echo "Starting API at port 9000"
uvicorn app:app --host 0.0.0.0 --port 9000 --reload &>> api_log.log &

if [[ $? -ne 0 ]]; then
	echo "Failed, check the log file: $(pwd)/install.log & $(pwd)/api.log"
else
	echo "Serving process started successfully"
fi
