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

echo "Create neccessary dirs"
[ ! -d "data" ] && mkdir data
[ ! -d "logs" ] && mkdir logs

echo "Installing requirements"
pip3 install -r requirements.txt &>>logs/install.log

echo "Starting API at port 9000"
uvicorn app:app --host 0.0.0.0 --port 9000 --reload &>> logs/api_log.log &

if [[ $? -ne 0 ]]; then
	echo -e "Failed, check the log file: \n- logs/install.log\n- logs/api.log"
else
	echo "Serving process started successfully"
fi
