'''
    Author: Maanas Talwar
    Purpose: Plugin to parse the check release url and find any new releases. If new releases are present update the json for available downloads.

'''

import pluginBlueprint.pluginBlueprint as abstractPlugin
import sys
import os
import json
import datetime
from urllib import request
from bs4 import BeautifulSoup

sys.path.append('../')


class postgresql(abstractPlugin.pluginBlueprint):

    # variable to store the url where the releases will be displayed
    url_check_release = "https://www.postgresql.org/"

    # variable to store the basic url(adding version required) for downloading
    url_download = "https://ftp.postgresql.org/pub/source/v*/postgresql-*.tar.gz"

    def check_which_released(self):
        # to detect the name of latest released versions and return the list to update_json

        # making a bs4 object to parse to the latest release versions
        html_code = request.urlopen(
            self.url_check_release).read().decode('utf8')
        parse_tree = BeautifulSoup(html_code, 'html.parser')

        # finding the column and then list with version data
        all_cols = list(parse_tree.find_all(class_='col-lg-6 feature'))
        reqd_col = all_cols[0]
        for i in range(len(all_cols)):
            if(all_cols[i].find(text="Latest Releases")):
                reqd_col = all_cols[i]

        # list for storing the html code for list items of unordered list
        versions_ul = list(reqd_col.find("ul"))
        # dictionary to store the data to store in json
        released_versions = []

        # updated the dictionary to store in json
        for i in range(len(versions_ul)):
            # returns the text with the strong tag
            cur_version = str(versions_ul[i].find("strong"))
            cur_version = cur_version[8:]								# removed opening strong tag
            # removed closing strong tag
            cur_version = cur_version.split("<", 1)[0]
            # cur_version is now only the text of version
            if(cur_version != ""):
                # since "" is returned for \n(removed strong therfore empty string)
                released_versions.append(cur_version)
        return released_versions

    def update_json(self):
        # function that recieves the list of released versions from check_which_released and updates the json file

        # list of released versions
        new_releases = self.check_which_released()

        # traversing over new_releases
        for i in range(len(new_releases)):
            major_version = new_releases[i].split('.', 1)[0] + '.X'
            minor_version = new_releases[i]

            with open("postgresql.json", 'r+') as file:
                cur_data = json.load(file)
                # if the major version is already present add data to the minor versions list else make a separate major versions list element

                # major version is present(add data to the minor versions list)
                isMajorPresent = 0
                for i in range(len(cur_data['majorVersions'])):
                    major_version_object = cur_data['majorVersions'][i]

                    if(major_version_object['majorVersion'] == major_version):
                        new_data = {
                            "minorVersion": minor_version,
                            # "releaseDate": "2020-02-13",
                            "isNew": "TRUE",
                            # "endOfUse": "FALSE",
                            # "colourCode": "GREEN",
                            # "remark": "Recommended Version"
                        }
                        # inserting data in major_version_object -> minorVersions
                        # add a check if minor version present
                        cur_data['majorVersions'][i]['minorVersions'].insert(0, new_data)
                        isMajorPresent = 1

                # major version is absent(make a separate major versions list element)
                if(isMajorPresent == 0):
                    new_data = {"majorVersion": major_version,
                                "minorVersions": [{
                                    "minorVersion": minor_version,
                                    # "releaseDate": "2020-02-13",
                                    "isNew": "TRUE",
                                    # "endOfUse": "FALSE",
                                    # "colourCode": "GREEN",
                                    # "remark": "Recommended Version"
                                },]}
                    cur_data['majorVersions'].insert(0, new_data)
                # taking file pointer to start as load gets it to end
                file.seek(0)
                # updsating json for each iteration i.e. for each latest released version
                json.dump(cur_data, file, indent = 4)
