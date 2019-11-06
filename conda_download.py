import json
import os
import datetime
import shutil
#import requests
#from bs4 import BeautifulSoup
import re

class conda:
	def __init__(self, download_dir, channel, conda_web_url = "https://conda.anaconda.org/",
				 only_download_new=False, conda_type = "linux-64/", conda_local_url = "http://192.168.30.67:8080/"):
		self.dir = download_dir
		self.channel = channel
		## old == local; new == web
		self.prefix = ["old_", "new_"]
		self.conda_type = conda_type
		self.conda_home_url = [conda_local_url, conda_web_url]
		self.json_file = "repodata.json.bz2"
		self.only_download_new=only_download_new

		self.head_url = [ head_url+channel+"/"+conda_type for head_url in self.conda_home_url ]
		self.json_dir = [ download_dir + prefix + channel + "/" for prefix in self.prefix ]
		self.json_path= [ json_dir + "repodata.json" for json_dir in self.json_dir ]

		self.info = dict(zip(self.prefix, zip(self.head_url, self.json_dir, self.json_path)))

		self.packages_dict = self.download_read_json()
		self.download_list_dir = self.dir + self.channel + datetime.datetime.now().strftime("%Y-%m-%d") + "/"

	def download_read_json(self):
		packages = {}
		if self.only_download_new:
			old_and_new = [self.prefix[1],]
		else:
			old_and_new = self.prefix
		for prefix in old_and_new:
			info = self.info[prefix]
			json_download_url=info[0]+self.json_file
			print(json_download_url)
			os.system("wget {0} && mkdir {1} && mv {2} {1} && cd {1} && bunzip2 {2}".format(json_download_url, info[1], self.json_file))
			print(json_download_url)
			with open(info[2], 'r') as load_f:
				new_dict = json.load(load_f)
			json_package = list(new_dict["packages"].keys())
			os.system("rm -rf {}".format(info[1]))
			packages[prefix] = json_package
		return packages

#	def read_json_packages_list(self, json_path):
#		with open(json_path, 'r') as load_f:
#			new_dict = json.load(load_f)
#		packages = list(new_dict["packages"].keys())
#		os.system("rm -rf {}".format(self.json_dir))
#		return packages

	def read_download_url_list(self, download_url_list):
		with open(download_url_list, "r") as url_list:
			download_url_list = url_list.readlines()
			return download_url_list

	def add_url(self, conda_packages_list):
		n = len(conda_packages_list)
		for i in range(0, n):
			conda_packages_list[i] = self.head_url + conda_packages_list[i] + "\n"
		return conda_packages_list

	def filter_download_list(self, head_url=True):
		new_list = self.packages_dict[self.prefix[1]]
		if self.only_download_new:
			download_list=new_list
			print("only download new packages:", len(download_list))
		else:
			old_list = self.packages_dict[self.prefix[0]]
			download_list = [x for x in new_list if x not in old_list]
			print("old_nu:", len(old_list), "\nnew_nu:", len(
				new_list), "\ndiff_nu:", len(download_list))
		if head_url:
			n = len(download_list)
			for i in range(0, n):
				download_list[i] = self.head_url[1] + download_list[i] + "\n"
		else:
			print("Not add head_url")

		return download_list


	def save_split(self, download_list):
		if os.path.exists(self.download_list_dir):
			#os.rmdir(self.download_list_dir)
			shutil.rmtree(self.download_list_dir)
			print("remove already exist dir:", self.download_list_dir)
		os.mkdir(self.download_list_dir)
		print("make new dir:", self.download_list_dir)
		download_list_file_name="new_download_list_" + self.channel
		download_list_file_path=self.download_list_dir + download_list_file_name
		with open(download_list_file_path, "w") as download_list_file:
			download_list_file.writelines(download_list)
			print("conda update packages list is: ", download_list_file_path)
		os.system("cd {0} && split -l 1000 {1}".format(self.download_list_dir, download_list_file_name))


#old_url_list = read_download_url_list(old_list_path)
#new_packages = get_json_packages_list(new_json_path)
#new_url_list = add_url(new_packages)
#download_file_name = download_dir_name + ".list"
#os.makedirs(download_dir_name)
#os.chdir(download_dir_name)
#with open(download_file_name, "w") as download:
#	download.writelines(download_url_list)
#os.system("split -l 1000 " + download_file_name)