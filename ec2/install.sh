sudo yum update

git clone https://github.com/navacron/deeplearning.git

echo "export PATH=\$HOME/src/anaconda3/bin:\$PATH" >> ~/.bash_profile
source ~/.bash_profile

conda install -y pytorch torchvision -c soumith

./jupyter.sh 


#Add Custom TCP Rule Add port 8888 to secrity rule

~/src/anaconda3/bin/jupyter notebook

