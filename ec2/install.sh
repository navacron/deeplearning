#!/bin/bash
sudo yum update

my_dir="$(dirname "$0")"

echo "export PATH=\$HOME/src/anaconda2/bin:\$PATH" >> ~/.bash_profile
source ~/.bash_profile

conda install -y pytorch torchvision -c soumith

"$my_dir/installjupyter.sh"

#Add Custom TCP Rule Add port 8888 to secrity rule

nohup "$my_dir/jupyterserver.sh" &
