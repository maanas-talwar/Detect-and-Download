'''
	Author : Maanas Talwar
	Purpose : Plugin to parse the check release url and find any new releases. If new releases are present update the json for available downloads.

'''

import sys
import os
import json
import datetime
from urllib import request
from bs4 import BeautifulSoup

sys.path.append('../')
import pluginBlueprint as abstractPlugin

def detect_releases(parse_tree) :
	# to detect the name of latest released versions

	# finding the column -> list with version data
	all_cols = list(parse_tree.find_all(class_ = 'col-lg-6 feature'))
	reqd_col = all_cols[0]
	for i in range(len(all_cols)) :
		if(all_cols[i].find(text ="Latest Releases")) :
			reqd_col = all_cols[i]

	versions_ul = list(reqd_col.find("ul"))

	# file with the data of latest available versions
	latest_versions = open('./latest_versions.txt', 'w')

	# feeding latest versions available in the file
	for i in range(len(versions_ul)) :
		cur_li = versions_ul[i]
		cur_version = cur_li.find("strong")
		if(cur_version != -1) :
			latest_versions.write(cur_version.text + '\n')
			# print(cur_version.text)
	latest_versions.close()

def download_release() :
	# to download the latest versions not already downloaded

	# file with the data of already downloaded versions
	downloaded_versions = open('./downloaded_versions.txt', 'a+')
	# file and list with the data of already downloaded versions in read mode
	downloaded_versions_read = open('./downloaded_versions.txt', 'r')
	downloaded_list = downloaded_versions_read.read().strip()
	# file with the data of latest versions
	latest_versions = open('./latest_versions.txt', 'r')
	# to determine if at all a file is downloaded
	is_downloaded = 0

	for vers in latest_versions :
		if vers.strip() not in downloaded_list :				#vers.strip() because of last element
			a = vers.strip()
			# url to download this(a) version
			cur_download = url_download + a + '/postgresql-' + a + '.tar.gz'
			down = request.urlopen(cur_download)
			print('Downloading to disk -> postgreSQL version : ' + a)
			filename = cur_download.split('/')[-1]

			# downloading the version
			f = open(filename, 'wb')
			down_data = down.read()
			f.write(down_data)
			f.close()

			downloaded_versions.write(vers)
			is_downloaded = 1
		else :
			print('Version ' + vers.strip() + ' is already downloaded.')

	if(is_downloaded == 0) :
		print('All latest versions are already downloaded.')

	latest_versions.close()
	downloaded_versions.close()
	downloaded_versions_read.close()

if __name__ == '__main__':
	print('***  Start Execution  ***')
	print('Date and Time : ' + str(datetime.datetime.now()))

	with open('postgresql.json') as f:
		data_json = json.load(f)

	# url to detect the latest released versions
	url_check_release = data_json['urls']['check_release']
	# url to download the latest released versions
	url_download = data_json['urls']['download']

	# making a bs4 object to parse to the latest release versions
	html_code = request.urlopen(url_check_release).read().decode('utf8')
	parse_tree = BeautifulSoup(html_code, 'html.parser')

	detect_releases(parse_tree)
	download_release()

	os.remove('latest_versions.txt')
	print('***  End Execution  ***')
