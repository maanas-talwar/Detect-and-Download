'''
        Author: Maanas Talwar
        Purpose: The main driver program for the calling the plugins for the data i.e. abstract download url and the path where the downloads should reside. This program imports the available plugins at runtime and downloads the locally absent versions for each plugin.

'''

import os
import json
import importlib
from urllib import request

def download_releases(plugin_data, plugin_name):
# function to download the latest releases by reading data from the JSON

    # data for the plugin
    abstract_download_url = plugin_data['url_download']
    path_to_plugin_data = plugin_data['path_to_plugin_data']

    # supplying the path to the json file
    with open(path_to_plugin_data + "/" + plugin_name + ".json", 'r+') as file:
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
                    # major version instead of ! and minor version instead of *
                    actual_download_url = abstract_download_url.replace('*', minor_version_object['minorVersion'])
                    actual_download_url = actual_download_url.replace('!', minor_version_object['minorVersion'].split('.', 1)[0])
                    
                    # since in some cases last part is not filename when working with mirrors and extensions are: tar.gz tgz
                    break_url = actual_download_url.split('/')
                    possible_filename = [name for name in break_url if 'tar.gz' in name] + [name for name in break_url if 'tgz' in name]
                    filename = possible_filename[0]
                    print("Downloading to disk: " + filename)
                    data_on_url = request.urlopen(actual_download_url)
                    # downloading the file
                    with open(path_to_plugin_data + '/downloads/' + filename, 'wb') as download_file:
                        download_file.write(data_on_url.read())

                    # updating data as the file is downloaded
                    minor_version_object['isDownloaded'] = 'TRUE'

                # clear the contents before writing to avoid unwanted trailing data
                file.truncate(0)
                # taking file pointer to start as load gets it to end
                file.seek(0)
                # updating json for each iteration i.e. for each latest released version
                json.dump(cur_data, file, indent = 4)


if __name__ == '__main__':
    print('*****  Start Execution  *****')

    # list of all the files in plugins directory
    all_files = os.listdir("./plugins/")

    # list of all the plugins
    all_plugins = []

    for name in all_files:
        if(name.endswith('_plugin')):
            # get only the name of plugin without "_plugin"
            all_plugins.append(name[:-7])

    for module in all_plugins:
        # name of the plugin directory
        dir_name = module + '_plugin'
        # importing the code.py module
        cur_module = importlib.import_module("plugins." + dir_name + ".code")
        # using getattr to get the class from code.py i.e. cur_module else can't instantiate using string
        class_name = getattr(cur_module, module)
        a = class_name()
        # recieving the plugin data from the plugin call
        plugin_data = a.setup_call()
        
        # not downloading iso for os as only url is needed
        if(not module.endswith('_OS')):
            # passing the arguments to download the releases
            download_releases(plugin_data, module)
            

    print('*****  End Execution  *****')
