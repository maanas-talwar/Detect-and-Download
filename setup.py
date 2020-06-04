'''
        Author: Maanas Talwar
        Purpose: The main driver program for the detection of new releases and downloading them.

'''

from plugins.postgresql.code import postgresql
import os
import json
from urllib import request


# if __name__ == '__main__':
#     print('\n*****  Start Execution  *****')
#
#     # testing the functioning of plugins
#     a = postgresql()
#     a.update_json()
#
#     print('*****  End Execution  *****\n')

def download_releases(abstract_download_url, path_to_plugin_data):
    # function to download the latest releases by reading data from the JSON

    # supplying the path to the json file
    with open(path_to_plugin_data + "/postgresql.json", 'r+') as file:
        cur_data = json.load(file)

        # traverse the major versions list
        for i in range(len(cur_data['majorVersions'])):
            major_version_object = cur_data['majorVersions'][i]

            # traverse the minor versions list
            for j in range(len(major_version_object['minorVersions'])):
                minor_version_object = major_version_object['minorVersions'][j]

                # check if minor version is already downloaded
                if(minor_version_object['isDownloaded'] == 'FALSE'):
                    # converting abstract_download_url to actual_download_url(with version number)
                    actual_download_url = abstract_download_url.replace('*', minor_version_object['minorVersion'])
                    filename = actual_download_url.split('/')[-1]
                    print(filename)
                    data_on_url = request.urlopen(actual_download_url)
                    # downloading the file
                    with open(path_to_plugin_data + '/downloads/' + filename, 'wb') as download_file:
                        download_file.write(data_on_url.read())

                    minor_version_object['isDownloaded'] = 'TRUE'
                # clear the contents before writing
                file.truncate(0)
                # taking file pointer to start as load gets it to end
                file.seek(0)
                # updating json for each iteration i.e. for each latest released version
                json.dump(cur_data, file, indent = 4)


if __name__ == '__main__':
    print('*****  Start Execution  *****')
    # path to current working directory
    cur_path = os.getcwd()
    download_releases("https://ftp.postgresql.org/pub/source/v*/postgresql-*.tar.gz", cur_path + "/plugins/postgresql/data")

    print('*****  End Execution  *****')
