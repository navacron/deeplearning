import argparse
import torchvision.utils as vutils
import torch.nn as nn
import torch
import torch.nn.parallel
from torch.autograd import Variable


parser = argparse.ArgumentParser()

parser.add_argument('--netG', required=True, default='', help="path to netG (to continue training)")
parser.add_argument('--num_class', type=int, default=3, help="class to generate")
parser.add_argument('--total_class', type=int, default=4, help="class to generate")
parser.add_argument('--nc', type=int, default=3, help='input depth')
parser.add_argument('--ngf', type=int, default=64)
parser.add_argument('--ndf', type=int, default=64)
parser.add_argument('--batchSize', type=int, default=64, help='input batch size')
parser.add_argument('--nz', type=int, default=100, help='size of the latent z vector')
parser.add_argument('--outf', default='.', help='folder to output images and model checkpoints')
parser.add_argument('--ngpu', type=int, default=1, help='number of GPUs to use')



opt = parser.parse_args()
print(opt)
num_classes = opt.total_class
ngpu = int(opt.ngpu)

ngf = int(opt.ngf)
ndf = int(opt.ndf)

nc = int(opt.nc)
nz = int(opt.nz)

ncc = nc + num_classes
nzc = nz + num_classes


class _netG(nn.Module):
    def __init__(self, ngpu):
        super(_netG, self).__init__()
        self.ngpu = ngpu
        self.main = nn.Sequential(
            # input is Z, going into a convolution
            nn.ConvTranspose2d(     nzc, ngf * 8, 4, 1, 0, bias=False),
            nn.BatchNorm2d(ngf * 8),
            nn.ReLU(True),
            # state size. (ngf*8) x 4 x 4
            nn.ConvTranspose2d(ngf * 8, ngf * 4, 4, 2, 1, bias=False),
            nn.BatchNorm2d(ngf * 4),
            nn.ReLU(True),
            # state size. (ngf*4) x 8 x 8
            nn.ConvTranspose2d(ngf * 4, ngf * 2, 4, 2, 1, bias=False),
            nn.BatchNorm2d(ngf * 2),
            nn.ReLU(True),
            # state size. (ngf*2) x 16 x 16
            nn.ConvTranspose2d(ngf * 2,     ngf, 4, 2, 1, bias=False),
            nn.BatchNorm2d(ngf),
            nn.ReLU(True),
            # state size. (ngf) x 32 x 32
            nn.ConvTranspose2d(    ngf,      ncc, 4, 2, 1, bias=False),
            nn.Tanh()
            # state size. (ncc) x 64 x 64
        )

    def forward(self, input):
        if isinstance(input.data, torch.cuda.FloatTensor) and self.ngpu > 1:
            output = nn.parallel.data_parallel(self.main, input, range(self.ngpu))
        else:
            output = self.main(input)
        return output

netG = _netG(ngpu)

netG.load_state_dict(torch.load(opt.netG))

def one_hot(target):
    # One hot encoding buffer that you create out of the loop and just keep reusing
    target_onehot = torch.FloatTensor(target.size(0), num_classes)
    
    #target_onehot = torch.FloatTensor(opt.batchSize, num_classes)
    # In your for loop
    target_onehot.zero_()
    target_onehot.scatter_(1, target, 1)
    return target_onehot    

fixed_noise = torch.FloatTensor(opt.batchSize, nz, 1, 1).normal_(0, 1)

ones = torch.ones(opt.batchSize,1)
fixed_class_vec = torch.mul(ones,opt.num_class)
class_onehot = one_hot(fixed_class_vec.long())
class_onehot.unsqueeze_(2).unsqueeze_(3)
fixed_noise = torch.cat([fixed_noise,class_onehot],1)
fixed_noise = Variable(fixed_noise)

fake = netG(fixed_noise)
fake2 = fake.data
fake2 = fake.data[:,0:opt.nc,:,:]
if opt.nc == 1:
    fake2 = fake2.unsqueeze(1)
vutils.save_image(fake2,
        '%s/final_samples_epoch_%03d.png' % (opt.outf, opt.num_class),
        normalize=True)
