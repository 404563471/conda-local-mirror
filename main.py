#!/bin/env python
from conda_download import conda
import sys
import argparse

def str2bool(v):
    if isinstance(v, bool):
       return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')

parser = argparse.ArgumentParser()
parser.description = 'get conda packages download url'
parser.add_argument("-c","--channel", help="The channel name, like: conda-forge, main", type=str)
parser.add_argument("--update", help="if False, download total channal", type=str2bool, default=True)
parser.add_argument("-p", "--platform", help="linux-64 or noarch", type=str, default='linux-64')
args = parser.parse_args()

if __name__=='__main__':
	real_channel=args.channel
	only_download_new=not args.update
	channel_type=args.platform + "/"
#	if sys.argv[2]:
#		only_download_new=sys.argv[2]
#		if sys.argv[3]:
#			conda_type=sys.argv[3]+"/"
	conda_new=conda(download_dir="./", channel=real_channel, only_download_new=only_download_new, conda_type=channel_type)
	download_list = conda_new.filter_download_list()
	conda_new.save_split(download_list)
	#print(packages_dict.keys())



	#conda_task.read_download_url_list()
