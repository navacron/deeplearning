!#/bin/bash
sudo yum update

echo "export PATH=\$HOME/src/anaconda3/bin:\$PATH" >> ~/.bash_profile
source ~/.bash_profile

conda install -y pytorch torchvision -c soumith

./installjupyter.sh 


#Add Custom TCP Rule Add port 8888 to secrity rule

nohup ./jupyterserver.sh &
