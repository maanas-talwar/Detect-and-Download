'''
    Author: Maanas Talwar
    Purpose: Plugin to parse the check release url and find any new releases. If new releases are present update the json for available downloads.

'''

import sys
import os
import json
import datetime
from urllib import request
from bs4 import BeautifulSoup

import plugins.pluginBlueprint.pluginBlueprint as abstractPlugin

class PHP(abstractPlugin.pluginBlueprint):

    # variable to store the url where the releases will be displayed
    url_check_release = "https://www.php.net/downloads"

    # variable to store the basic url(adding version required in place of *) for downloading
    url_download = "https://www.php.net/distributions/php-*.tar.gz"

    def check_which_released(self):
        # to detect the name of latest released versions and return the list to update_json

        # making a bs4 object to parse to the latest release versions
        html_code = request.urlopen(self.url_check_release).read().decode('utf8')
        parse_tree = BeautifulSoup(html_code, 'html.parser')

        # class objects newstitle contain version data
        all_content_boxes = list(parse_tree.find_all(class_='content-box'))

        # list to store the data to store in json
        released_versions = []
        # list to store the release date to store in json
        released_dates = []

        # updated the list to store in json
        for i in range(len(all_content_boxes)):
            # downloads available in different types(tar.gz required)
            cur_version_all_types = all_content_boxes[i].find_all('a')
            # storing dates for all formats of current version
            cur_version_all_types_dates = all_content_boxes[i].find_all('span')
            # removing unwanted stuff not relating to dates(odd indexed stuff)
            del cur_version_all_types_dates[1::2]
            # print(cur_version_all_types_dates, "\n")
            
            j = 0
            # cur_version traverses through all types(tar.gz, tar.bz2 ...) of versions
            for cur_version in cur_version_all_types:
                
                # taking only tar.gz files
                if(cur_version.text.endswith('tar.gz')):
                    # required_version takes only tar.gz versions
                    
                    # removing starting php string
                    required_version = cur_version.text.split('-', 1)[1]
                    # removing tar.gz extension
                    required_version = required_version[:-7]
                    
                    # storing release date for current version
                    date = cur_version_all_types_dates[j].text
                    # adding release date to list
                    released_dates.append(date)
                    # adding released version to list
                    released_versions.append(required_version)
                    
                j+=1
        
        return released_versions,released_dates

    def update_json(self):
        # function that recieves the list of released versions from check_which_released and updates the json file

        # path to the current file's directory
        cur_path = os.path.dirname(__file__)
        # list of released versions
        new_releases, released_dates = self.check_which_released()

        # traversing over new_releases
        for i in range(len(new_releases)):
            major_version = new_releases[i].rsplit('.', 1)[0] + '.X'
            minor_version = new_releases[i]

            # supplying the path to the json file
            with open(cur_path + "/data/PHP.json", 'r+') as file:
                cur_data = json.load(file)
                # if the major version is already present add data to the minor versions list else make a separate major versions list element

                # major version is present(add data to the minor versions list)
                isMajorPresent = 0
                for i in range(len(cur_data['majorVersions'])):
                    major_version_object = cur_data['majorVersions'][i]

                    if(major_version_object['majorVersion'] == major_version):
                        isMajorPresent = 1
                        isMinorPresent = 0
                        new_data = {
                            "minorVersion": minor_version,
                            "releaseDate": released_dates[i],
                            "isDownloaded": "FALSE",
                            # "endOfUse": "FALSE",
                            # "colourCode": "GREEN",
                            # "remark": "Recommended Version"
                        }
                        # check if minor version present just skip to the next version in new_releases
                        for j in range(len(major_version_object['minorVersions'])):
                            minor_version_object = major_version_object['minorVersions'][j]
                            if(minor_version_object['minorVersion'] == minor_version):
                                isMinorPresent = 1
                                break

                        # inserting data in major_version_object -> minorVersions only if the minot version is not present
                        if(isMinorPresent == 0):
                            major_version_object['minorVersions'].insert(0, new_data)

                        break

                # major version is absent(make a separate major versions list element)
                if(isMajorPresent == 0):
                    new_data = {"majorVersion": major_version,
                                "minorVersions": [{
                                    "minorVersion": minor_version,
                                    "releaseDate": released_dates[i],
                                    "isDownloaded": "FALSE",
                                    # "endOfUse": "FALSE",
                                    # "colourCode": "GREEN",
                                    # "remark": "Recommended Version"
                                },]}
                    cur_data['majorVersions'].insert(0, new_data)
                # clear the contents before writing
                file.truncate(0)
                # taking file pointer to start as load gets it to end
                file.seek(0)
                # updating json for each iteration i.e. for each latest released version
                json.dump(cur_data, file, indent = 4)

    def setup_call(self):
        # function to invoke other functions and return the path and abstract_download_url to driver program

        self.update_json()
        # path to the current file's directory
        cur_path = os.path.dirname(__file__)
        # dictionary to contain data to be returned
        plugin_data = {'url_download': self.url_download, 'path_to_plugin_data': cur_path + '/data'}

        return plugin_data
