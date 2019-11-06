from conda_download import conda
import sys
if __name__=='__main__':
	real_channel=sys.argv[1]
	only_download_new=sys.argv[2]
	conda_new=conda(download_dir="./", channel=real_channel, only_download_new=only_download_new)
	download_list = conda_new.filter_download_list()
	conda_new.save_split(download_list)
	#print(packages_dict.keys())



	#conda_task.read_download_url_list()
