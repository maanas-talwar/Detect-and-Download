'''
        Author: Maanas Talwar
        Purpose: To create an abstract class blueprint for all the plugins to use.

'''

from abc import ABC, abstractmethod

class pluginBlueprint(ABC):
    @property
    @abstractmethod
    def url_download(self):
    # variable to store the basic url(adding version required) for downloading
        pass

    @abstractmethod
    def url_check_release(self):
    # variable to store the url where the releases will be displayed
        pass

    @abstractmethod
    def check_which_released(self):
    # function to check the latest releases from the website(url_check_release) and storing in a list
        pass

    @abstractmethod
    def update_json(self):
    # function to update the JSON file for availability of new version
        pass
