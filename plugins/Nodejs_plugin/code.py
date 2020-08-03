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

class Nodejs(abstractPlugin.pluginBlueprint):

    # variable to store the url where the releases will be displayed
    url_check_release = "https://nodejs.org/en/about/releases/"

    # variable to store the basic url(adding version required in place of *, major version instead of !) for downloading
    url_download = "https://nodejs.org/download/release/latest-v!.x/node-v*.tar.gz"

    def check_which_released(self):
        # to detect the name of latest released versions and return the list to update_json

        # making a bs4 object to parse to the latest release versions
        html_code = request.urlopen(self.url_check_release).read().decode('utf8')
        parse_tree = BeautifulSoup(html_code, 'html.parser')

        # finding the table with version data
        table = parse_tree.find(class_='release-schedule').find_all('tr')
        # removing headings row
        del table[0]
        
        # list to store the major versions from url_check_release
        major_versions = []
        # list to store the data to store in json
        released_versions = []
        # list to store the release date to store in json
        released_dates = []
        
        for i in range(len(table)):
            if(table[i].find('a')):
                # remove v from 'v10' etc & first link is version
                major_versions.append(table[i].find('a').text[1:])
                # date is in 4th td
                released_dates.append(table[i].find_all('td')[3].text)
        
        # the whole release version is located at different url(version from table in place of !)
        total_release_url = 'https://nodejs.org/download/release/latest-v!.x/'
        
        for i in range(len(major_versions)):
            cur_release_url = total_release_url.replace('!', major_versions[i])
            # making a bs4 object to parse to the latest release versions
            html = request.urlopen(cur_release_url).read().decode('utf8')
            bs4_obj = BeautifulSoup(html, 'html.parser')
            
            # second last object is the one to be downloaded always
            version = bs4_obj.find_all('a')[-2].text
            # version contains : node-v'version'.tar,gz
            version = version[6:]
            version = version[:-7]
            released_versions.append(version)

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
            with open(cur_path + "/data/Nodejs.json", 'r+') as file:
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
