'''
        Author: Maanas Talwar
        Purpose: To create an abstract class blueprint for all the plugins to use.

'''

import abc

class abstractPlugin(ABC):
    @property
    def url_download:
    # variable to store the basic url(adding version required) for downloading
        raise NotImplementedError
    def url_check_release:
    # variable to store the url where the releases will be displayed
        raise NotImplementedError

    def check_which_released(self):
    # function to check the latest releases from the website(url_check_release) and storing in a list
        pass
    def update_json(self):
    # function to update the json file for availability of new version
        pass
    
