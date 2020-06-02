'''
        Author: Maanas Talwar
        Purpose: The main driver program for the detextion of new releases and downloading them.

'''


# if __name__ == '__main__':
#     print('*****  Start Execution  *****')
#
#
#     print('*****  End Execution  *****')


# POSTGRESQL EXAMPLE
# def download_release():
# 	# to download the latest versions not already downloaded
#
# 	# file with the data of already downloaded versions
# 	downloaded_versions = open('./downloaded_versions.txt', 'a+')
# 	# file and list with the data of already downloaded versions in read mode
# 	downloaded_versions_read = open('./downloaded_versions.txt', 'r')
# 	downloaded_list = downloaded_versions_read.read().strip()
# 	# file with the data of latest versions
# 	latest_versions = open('./latest_versions.txt', 'r')
# 	# to determine if at all a file is downloaded
# 	is_downloaded = 0
#
# 	for vers in latest_versions:
# 		if vers.strip() not in downloaded_list:				#vers.strip() because of last element
# 			a = vers.strip()
# 			# url to download this(a) version
# 			cur_download = url_download + a + '/postgresql-' + a + '.tar.gz'
# 			down = request.urlopen(cur_download)
# 			print('Downloading to disk -> postgreSQL version: ' + a)
# 			filename = cur_download.split('/')[-1]
#
# 			# downloading the version
# 			f = open(filename, 'wb')
# 			down_data = down.read()
# 			f.write(down_data)
# 			f.close()
#
# 			downloaded_versions.write(vers)
# 			is_downloaded = 1
# 		else:
# 			print('Version ' + vers.strip() + ' is already downloaded.')
#
# 	if(is_downloaded == 0):
# 		print('All latest versions are already downloaded.')
#
# 	latest_versions.close()
# 	downloaded_versions.close()
# 	downloaded_versions_read.close()
