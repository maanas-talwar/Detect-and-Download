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

class Python(abstractPlugin.pluginBlueprint):

    # variable to store the url where the releases will be displayed
    url_check_release = "https://www.python.org/"

    # variable to store the basic url(adding version required in place of *) for downloading
    url_download = "https://www.python.org/ftp/python/*/Python-*.tgz"

    def check_which_released(self):
    # to detect the name of latest released versions and return the list to update_json

        # making a bs4 object to parse to the latest release versions
        html_code = request.urlopen(self.url_check_release).read().decode('utf8')
        parse_tree = BeautifulSoup(html_code, 'html.parser')

        # list to store the data to store in json
        released_versions = []
        # list to store the release date to store in json
        released_dates = []
        
        # finding the latest release class
        latest_release_field = parse_tree.find(class_='small-widget download-widget')
        all_releases = latest_release_field.find_all('a')
        for i in range(len(all_releases)):
            released_versions.append(all_releases[i].text[7:])
        
        # The released dates are on a different url
        check_date_url = "https://www.python.org/downloads/"
        
        # making a bs4 object to parse to the latest release dates
        html_date_code = request.urlopen(check_date_url).read().decode('utf8')
        parse_date_tree = BeautifulSoup(html_date_code, 'html.parser')
        
        # finding the released date table
        all_releases_data = parse_date_tree.find(class_='row download-list-widget')
        all_releases_numbers = all_releases_data.find_all(class_='release-number')
        all_releases_dates = all_releases_data.find_all(class_='release-date')
        
        # list of all the released versions
        all_versions = []
        # list of all the dates for released versions
        all_dates = []
    
        for i in range(len(all_releases_data)):
            if(all_releases_numbers[i].find('a')):
                all_versions.append(all_releases_numbers[i].find('a').text[7:])
                all_dates.append(all_releases_dates[i].text)
                
        for i in range(len(released_versions)):
            reqd_index = all_versions.index(released_versions[i])
            released_dates.append(all_dates[reqd_index])
            
        return released_versions, released_dates

    def update_json(self):
        # function that recieves the list of released versions from check_which_released and updates the json file

        # path to the current file's directory
        cur_path = os.path.dirname(__file__)
        # list of released versions
        new_releases, released_dates = self.check_which_released()

        # traversing over new_releases
        for i in range(len(new_releases)):
            major_version = new_releases[i].split('.', 1)[0] + '.X'
            minor_version = new_releases[i]

            # supplying the path to the json file
            with open(cur_path + "/data/Python.json", 'r+') as file:
                cur_data = json.load(file)
                # if the major version is already present add data to the minor versions list else make a separate major versions list element

                # major version is present(add data to the minor versions list)
                isMajorPresent = 0
                for k in range(len(cur_data['majorVersions'])):
                    major_version_object = cur_data['majorVersions'][k]

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
