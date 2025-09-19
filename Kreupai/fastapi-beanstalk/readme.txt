Requirement.txt
has all the modules to be install

Procfile tells EB how to start fastapi which host and port

Installing EB CLI on Bash

git clone https://github.com/aws/aws-elastic-beanstalk-cli-setup.git
cd aws-elastic-beanstalk-cli-setup
python3 scripts/ebcli_installer.py
echo 'export PATH=$PATH:$HOME/.ebcli-virtual-env/executables' >> ~/.bashrc
source ~/.bashrc


Changing to file directory
cd /mnt/e/KreupAI/DAta/fastapi-beanstalk

describing application name,platform and region
eb init -p python-3.11 fastapi-beanstalk --region ap-south-1

Create environment
eb create fastapi-env --instance_type t3.micro

eb open

setting environment variables
eb setenv DB_HOST=url.endpoint DB_USER=user DB_PASS=pass DB_NAME=mydb DB_PORT=3306

eb deploy



