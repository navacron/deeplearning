# Amazon EC2 with PyTorch

## Installation
Instructions to setup a deep learning enviornment with pytorch. 

1. Deep Learning AMI  - https://aws.amazon.com/marketplace/pp/B01M0AXXQB. 
2. Setup a KeyPair if not already. Can name is anything. This will be used in the ssh command. Create an instance
3. To test start with micro instance. The g2 and p2 have GPU's, and should choose if want to run with GPU (note the hourly rates)
4. Go to Security Groups Section on the EC2 console and Add Custom TCP Rule add port 8888
5. ssh to server using your pem file and the public host name from ec2 console

	```
	ssh -i Navacron.pem ec2-user@ec2-52-90-230-235.compute-1.amazonaws.com  (replace with your own pem, and hostname)
	```

6. On the terminal type the following
	
	```
	git clone https://github.com/navacron/deeplearning.git
	```

	```
    ./deeplearning/ec2/install.sh  #this will update the vm, install pytorch, setup ipython notebook on port 8888, default password is deeplearning
    ```
7. The jupyter server can be run manually
    
    ```
    nohup ./deeplearning/ec2/jupyterserver.sh & 
    ```

